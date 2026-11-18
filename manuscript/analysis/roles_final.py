"""Nihai rol çözümü — hakem turu 1'in C1–C6 maddelerine göre (manuscript/reviews/round-1.md).

Değişiklikler (archetypes_v2.py'ye göre):
- Bootstrap OYUNCU düzeyinde (bir oyuncunun tüm sezonları birlikte çekilir; Hennig, 2007, küme bootstrap'i).
- GMM kovaryans yapısı kısıtlı ('diag' / 'tied'), BIC ile karşılaştırılır; tam kovaryans kullanılmaz.
- Değişkenler: rol payları (sahadaki gerçek paydalar) + şut profili + asist ağı. Boy rol tanımına GİRMEZ
  (rol–pozisyon analizinin döngüsel olmaması için); yakın eşdoğrusal ikiler çıkarıldı (assisted_rate, creator_idx).
- Eksik değerler: ham ölçekte NaN bırakılır, sezon içi z-skordan SONRA 0 (= sezon ortalaması) atanır; eksiklik raporlanır.
- Standardizasyon: sezon içi ortalama/SS yalnızca model örnekleminden (≥ 400 dk).
- Atama: tüm oyuncu-sezonlar modelin sonsal olasılığıyla (predict_proba).
- K karar kuralı (önceden): en küçük kümesinin Jaccard'ı ≥ 0,5 olan K'lar içinde ortalama Jaccard'ı en yüksek olan;
  fark ≤ 0,02 ise dönemler arası ARI'si yüksek olan.
- Dönemler arası uyum: 2016–2019 modeli 2020–2024'e uygulanır; yalnızca erken dönemde hiç görülmemiş oyuncularda ARI.
- Duyarlılık: diğer değişken setleriyle K = 4–5 ve nihai bölünmeyle ARI.
- Rol × resmî pozisyon: Cramér V, oyuncu düzeyi bootstrap GA.

Çıktılar: data/processed/roles_final_K{4,5}.csv, results.json["roles_final"].

    python manuscript/analysis/roles_final.py --B 200
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.mixture import GaussianMixture

from archetypes_v2 import ADV, COUNT40, NET, PROC, RESULTS, SEED, SHOT

FIT_MIN = 400
COV = ("diag", "tied")
DROP = {"assisted_rate", "creator_idx"}


def raw_features(ps: pd.DataFrame, sets: tuple[str, ...]) -> pd.DataFrame:
    key = ps[["Player_ID", "Season"]]
    parts = []
    if "box" in sets:
        fga = ps["FieldGoalsAttempted2"] + ps["FieldGoalsAttempted3"]
        b = pd.DataFrame({"FG3A_rate": ps["FieldGoalsAttempted3"] / fga.where(fga > 0),
                          "FT_rate": ps["FreeThrowsAttempted"] / fga.where(fga > 0), "USG_proxy": ps["USG_proxy"]})
        for k, col in COUNT40.items():
            b[k] = np.log1p(ps[col] / ps["MIN"] * 40)
        parts.append(b)
    if "adv" in sets:
        a = key.merge(pd.read_csv(PROC / "advanced.csv.gz"), how="left", on=["Player_ID", "Season"])[ADV]
        a[["AST_pct", "ORB_pct", "STL_pct", "BLK_pct"]] = np.sqrt(a[["AST_pct", "ORB_pct", "STL_pct", "BLK_pct"]].clip(lower=0))
        parts.append(a.set_axis(ps.index))
    if "shot" in sets:
        parts.append(key.merge(pd.read_csv(PROC / "shot_profile.csv.gz"), how="left",
                               on=["Player_ID", "Season"])[SHOT].set_axis(ps.index))
    if "net" in sets:
        parts.append(key.merge(pd.read_csv(PROC / "assist_net.csv.gz"), how="left",
                               on=["Player_ID", "Season"])[NET].set_axis(ps.index))
    if "height" in sets:
        parts.append(key.merge(pd.read_csv(PROC / "bio.csv.gz"), how="left",
                               on=["Player_ID", "Season"])[["height_cm"]].set_axis(ps.index))
    f = pd.concat(parts, axis=1)
    return f[[c for c in f.columns if c not in DROP]]


def zscore(f: pd.DataFrame, ps: pd.DataFrame, fit: np.ndarray) -> pd.DataFrame:
    ref = f[fit].groupby(ps.loc[fit, "Season"])
    mu, sd = ref.mean(), ref.std(ddof=0)
    z = (f - mu.reindex(ps["Season"]).values) / sd.reindex(ps["Season"]).values
    return z.fillna(0.0)


def gmm(z: np.ndarray, k: int, cov: str, seed: int = SEED) -> GaussianMixture:
    return GaussianMixture(k, covariance_type=cov, n_init=5, random_state=seed, reg_covar=1e-4).fit(z)


def player_boot_jaccard(z, players, k, cov, B, rng) -> np.ndarray:
    base = gmm(z, k, cov).predict(z)
    up = np.unique(players)
    rows_of = {p: np.where(players == p)[0] for p in up}
    scores = np.zeros((B, k))
    for b in range(B):
        draw = rng.choice(up, len(up), replace=True)
        idx = np.concatenate([rows_of[p] for p in draw])
        lab = gmm(z[idx], k, cov, seed=int(rng.integers(1e9))).predict(z[idx])
        uniq, first = np.unique(idx, return_index=True)
        lb, lo = lab[first], base[uniq]
        sets_b = [set(np.where(lb == d)[0]) for d in range(k)]
        for c in range(k):
            a = set(np.where(lo == c)[0])
            scores[b, c] = max((len(a & s) / len(a | s)) if (a | s) else 0 for s in sets_b)
    return scores.mean(axis=0)


def new_player_ari(z, players, seasons, k, cov) -> tuple[float, int]:
    early = seasons <= 2019
    seen = set(players[early])
    m_e, m_l = gmm(z[early], k, cov), gmm(z[~early], k, cov)
    new = (~early) & ~np.isin(players, list(seen))
    return float(adjusted_rand_score(m_l.predict(z[new]), m_e.predict(z[new]))), int(new.sum())


def cramers_v(t: pd.DataFrame) -> float:
    return float(np.sqrt(chi2_contingency(t)[0] / (t.values.sum() * (min(t.shape) - 1))))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=200)
    ap.add_argument("--Bscan", type=int, default=100)
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    fit = (ps["MIN"] >= FIT_MIN).to_numpy()
    players, seasons = ps["Player_ID"].to_numpy(), ps["Season"].to_numpy()

    raw = raw_features(ps, ("adv", "shot", "net"))
    missing = raw[fit].isna().mean().round(4)
    z_all = zscore(raw, ps, fit)
    z = z_all[fit].to_numpy()

    # 1. Tarama: kovaryans × K
    scan = {}
    for cov in COV:
        for k in range(4, 9):
            m = gmm(z, k, cov)
            lab = m.predict(z)
            jac = player_boot_jaccard(z, players[fit], k, cov, a.Bscan, rng)
            ari, n_new = new_player_ari(z, players[fit], seasons[fit], k, cov)
            scan[f"{cov}_K{k}"] = {"BIC": round(float(m.bic(z)), 1), "silhouette": round(float(silhouette_score(z, lab)), 3),
                                   "jaccard_ort": round(float(jac.mean()), 3), "jaccard_min": round(float(jac.min()), 3),
                                   "jaccard_kume": [round(float(x), 3) for x in jac],
                                   "yeni_oyuncu_ARI": round(ari, 3), "yeni_oyuncu_N": n_new,
                                   "en_kucuk_kume": int(np.bincount(lab, minlength=k).min())}
            print(cov, k, {kk: v for kk, v in scan[f"{cov}_K{k}"].items() if kk != "jaccard_kume"}, flush=True)
    cov = min(COV, key=lambda c: np.mean([scan[f"{c}_K{k}"]["BIC"] for k in range(4, 9)]))

    # 2. K karar kuralı
    ok = [k for k in range(4, 9) if scan[f"{cov}_K{k}"]["jaccard_min"] >= 0.5]
    cand = ok or list(range(4, 9))
    best = max(scan[f"{cov}_K{k}"]["jaccard_ort"] for k in cand)
    near = [k for k in cand if best - scan[f"{cov}_K{k}"]["jaccard_ort"] <= 0.02]
    K = max(near, key=lambda k: scan[f"{cov}_K{k}"]["yeni_oyuncu_ARI"])

    # 3. Nihai çözümler (K ve alternatif K), aynı tarama koşusundaki Jaccard değerleriyle
    bio = ps[["Player_ID", "Season"]].merge(pd.read_csv(PROC / "bio.csv.gz"), how="left", on=["Player_ID", "Season"])
    finals = {}
    for k in sorted({K, 4, 5}):
        m = gmm(z, k, cov)
        post = m.predict_proba(z_all.to_numpy())
        lab = post.argmax(1) + 1
        out = ps[["Player_ID", "Player", "Season", "Team", "MIN", "VAL40"]].assign(Arketip=lab, p_max=post.max(1))
        out.to_csv(PROC / f"roles_final_K{k}.csv", index=False)
        prof = z_all.groupby(lab).mean().round(2)
        t = pd.crosstab(lab, bio["position"])
        boot_v = []
        up = np.unique(players)
        rows_of = {p: np.where(players == p)[0] for p in up}
        for _ in range(a.B):
            idx = np.concatenate([rows_of[p] for p in rng.choice(up, len(up))])
            boot_v.append(cramers_v(pd.crosstab(lab[idx], bio["position"].to_numpy()[idx])))
        jac = player_boot_jaccard(z, players[fit], k, cov, a.B, rng)
        finals[f"K{k}"] = {
            "N": int(len(out)), "kume_N": {int(i): int(n) for i, n in zip(*np.unique(lab, return_counts=True))},
            "jaccard_kume": [round(float(x), 3) for x in jac], "jaccard_ort": round(float(jac.mean()), 3),
            "p_max_lt_07": round(float((out["p_max"] < 0.7).mean()), 3),
            "profil_z": prof.to_dict(orient="index"),
            "pozisyon": t.to_dict(orient="index"),
            "baskin_pozisyon_payi": (t.max(axis=1) / t.sum(axis=1)).round(2).to_dict(),
            "ortalama_boy": bio.groupby(lab)["height_cm"].mean().round(1).to_dict(),
            "cramers_v": round(cramers_v(t), 3),
            "cramers_v_GA95": [round(float(x), 3) for x in np.percentile(boot_v, [2.5, 97.5])],
        }
        print(f"K{k}", {kk: v for kk, v in finals[f"K{k}"].items() if kk not in ("profil_z", "pozisyon")}, flush=True)

    # 4. Duyarlılık: diğer değişken setleri
    base_lab = {k: pd.read_csv(PROC / f"roles_final_K{k}.csv")["Arketip"].to_numpy()[fit] for k in (4, 5)}
    sets = {"kutu_skoru": ("box",), "kutu_skoru+sut": ("box", "shot"), "paylar+sut": ("adv", "shot"),
            "paylar+sut+ag (nihai)": ("adv", "shot", "net"), "paylar+sut+ag+boy": ("adv", "shot", "net", "height")}
    robust = {}
    for name, s in sets.items():
        zz = zscore(raw_features(ps, s), ps, fit)[fit].to_numpy()
        for k in (4, 5):
            jac = player_boot_jaccard(zz, players[fit], k, cov, 50, rng)
            robust[f"{name}_K{k}"] = {"degisken_N": int(zz.shape[1]), "jaccard_ort": round(float(jac.mean()), 3),
                                      "jaccard_min": round(float(jac.min()), 3),
                                      "nihai_ile_ARI": round(float(adjusted_rand_score(base_lab[k], gmm(zz, k, cov).predict(zz))), 3)}
            print(name, k, robust[f"{name}_K{k}"], flush=True)

    res = json.loads(RESULTS.read_text())
    res["roles_final"] = {"kovaryans": cov, "K": K, "fit_N": int(fit.sum()), "fit_oyuncu_N": int(len(np.unique(players[fit]))),
                          "degiskenler": list(raw.columns), "eksik_pay": {c: float(v) for c, v in missing.items() if v > 0},
                          "B": a.B, "Bscan": a.Bscan, "tarama": scan, "nihai": finals, "duyarlilik": robust}
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
