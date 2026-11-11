"""Arketipler v2 — rol tabanlı, yeniden üretilebilir, kararlılığı sınanmış kümeleme.

Tezden farkları (OPEN_QUESTIONS #3, #16):
- Değişkenler oyuncunun NE yaptığını (rol) ölçer, ne kadar İYİ yaptığını (verimlilik) değil:
  şut profili, kullanım, asist, ribaund, blok, top çalma, top kaybı, faul. eFG, 3P%, FT% ve VAL40
  kümelemeye girmez; böylece arketip ile oyuncu değeri (VAL40, ILP girdisi) ayrı kalır.
- Sezon içi z-skor: ligdeki üçlük artışı gibi dönem eğilimleri kümelere dönem etiketi olarak sızmaz.
- K seçimi: silhouette + Calinski–Harabasz + Davies–Bouldin + bootstrap Jaccard kararlılığı
  (Hennig, 2007) + dönemler arası (2016–2019 / 2020–2024) kararlılık; Ward ve GMM karşılaştırılır.
- Model yeterli süre alan oyuncularla (≥ --fit-min dk) kurulur, kalanlar en yakın merkeze atanır.

Çıktılar: data/processed/archetypes_v2.csv, results.json["archetypes_v2"].

    python manuscript/analysis/archetypes_v2.py --K 6
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.metrics import adjusted_rand_score, calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.mixture import GaussianMixture

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
RESULTS = Path(__file__).with_name("results.json")
SEED = 20261109

COUNT40 = {"AST_40": "Assistances", "OREB_40": "OffensiveRebounds", "DREB_40": "DefensiveRebounds",
           "STL_40": "Steals", "BLK_40": "BlocksFavour", "TOV_40": "Turnovers",
           "FD_40": "FoulsReceived", "PF_40": "FoulsCommited"}
FEATURES = ["FG3A_rate", "FT_rate", "USG_proxy", *COUNT40]
SHOT = ["rim_rate", "paint_rate", "mid_rate", "c3_share", "fastbreak_rate", "second_chance_rate", "assisted_rate"]


ADV = ["3PAr", "FTr", "USG_pct", "AST_pct", "ORB_pct", "DRB_pct", "STL_pct", "BLK_pct", "TOV_pct", "FD_pct", "PF_pct"]
SQRT = ["AST_pct", "ORB_pct", "STL_pct", "BLK_pct"]  # sağa çarpık paylar


def features(ps: pd.DataFrame, extended: bool = False, advanced: bool = False, height: bool = False) -> pd.DataFrame:
    if advanced:  # ileri istatistikler (gerçek sahada paydalar; engine/data/advanced.py) + şut profili
        key = ps[["Player_ID", "Season"]]
        adv = key.merge(pd.read_csv(PROC / "advanced.csv.gz"), how="left", on=["Player_ID", "Season"])
        sp = key.merge(pd.read_csv(PROC / "shot_profile.csv.gz"), how="left", on=["Player_ID", "Season"])
        f = pd.concat([adv[ADV], sp[SHOT]], axis=1).fillna(0)
        f.index = ps.index
        if height:  # boy (engine/data/bio.py); eksikler resmî pozisyonun ortalamasıyla doldurulur
            bio = key.merge(pd.read_csv(PROC / "bio.csv.gz"), how="left", on=["Player_ID", "Season"])
            h = bio["height_cm"].fillna(bio.groupby("position")["height_cm"].transform("mean"))
            f["height_cm"] = h.fillna(h.mean()).values
        f[SQRT] = np.sqrt(f[SQRT].clip(lower=0))
        return f.groupby(ps["Season"]).transform(lambda c: (c - c.mean()) / c.std(ddof=0))
    fga = ps["FieldGoalsAttempted2"] + ps["FieldGoalsAttempted3"]
    f = pd.DataFrame(index=ps.index)
    f["FG3A_rate"] = np.where(fga > 0, ps["FieldGoalsAttempted3"] / fga.where(fga > 0, 1), 0.0)
    f["FT_rate"] = np.where(fga > 0, ps["FreeThrowsAttempted"] / fga.where(fga > 0, 1), 0.0)
    f["USG_proxy"] = ps["USG_proxy"]
    for k, col in COUNT40.items():
        f[k] = np.log1p(ps[col] / ps["MIN"] * 40)  # sağa çarpık sayım oranları
    if extended:  # şut profili: engine/data/shot_profile.py
        sp = pd.read_csv(PROC / "shot_profile.csv.gz")
        f[SHOT] = ps[["Player_ID", "Season"]].merge(sp, how="left", on=["Player_ID", "Season"])[SHOT].fillna(0).values
    # sezon içi standardizasyon
    return f.groupby(ps["Season"]).transform(lambda c: (c - c.mean()) / c.std(ddof=0))


def cluster(z: np.ndarray, k: int, method: str, seed: int = SEED) -> np.ndarray:
    if method == "ward":
        return fcluster(linkage(z, method="ward"), k, criterion="maxclust") - 1
    return GaussianMixture(k, covariance_type="full", n_init=5, random_state=seed, reg_covar=1e-3).fit_predict(z)


def jaccard_stability(z: np.ndarray, k: int, method: str, B: int, rng) -> list[float]:
    """Hennig (2007): her orijinal küme için bootstrap kümeleriyle en yüksek Jaccard'ın ortalaması."""
    base = cluster(z, k, method)
    scores = np.zeros((B, k))
    for b in range(B):
        idx = rng.choice(len(z), len(z), replace=True)
        boot = cluster(z[idx], k, method, seed=int(rng.integers(1e9)))
        uniq = np.unique(idx)
        first = {i: np.where(idx == i)[0][0] for i in uniq}
        lab_b = np.array([boot[first[i]] for i in uniq])
        lab_o = base[uniq]
        for c in range(k):
            a = set(np.where(lab_o == c)[0])
            scores[b, c] = max((len(a & s) / len(a | s) if a | s else 0)
                               for s in (set(np.where(lab_b == d)[0]) for d in range(k)))
    return scores.mean(axis=0).round(3).tolist()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, default=None, help="nihai küme sayısı (verilmezse yalnızca tarama)")
    ap.add_argument("--method", default="ward", choices=["ward", "gmm"])
    ap.add_argument("--kmin", type=int, default=4)
    ap.add_argument("--kmax", type=int, default=10)
    ap.add_argument("--fit-min", type=float, default=400, help="modeli kuran oyuncu-sezonlar için asgari dakika")
    ap.add_argument("--B", type=int, default=100, help="bootstrap tekrar sayısı")
    ap.add_argument("--features", default="base", choices=["base", "extended", "advanced", "advanced_height"])
    ap.add_argument("--macro-file", default="archetypes_v2.csv", help="--nested için ana rol dosyası (data/processed)")
    ap.add_argument("--nested", action="store_true",
                    help="archetypes_v2.csv'deki ana rollerin her birinde alt rol taraması (K = kmin..kmax)")
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)

    ps = pd.read_csv(PROC / "player_season.csv.gz")
    z_all = features(ps, a.features == "extended", a.features.startswith("advanced"), a.features == "advanced_height")
    if a.nested:
        macro = ps[["Player_ID", "Season"]].merge(pd.read_csv(PROC / a.macro_file), how="left",
                                                  on=["Player_ID", "Season"])["Arketip"].values
        nested = {}
        for m in sorted(set(macro)):
            sub = (macro == m) & (ps["MIN"] >= a.fit_min).to_numpy()
            zs = z_all[sub].to_numpy()
            for method in ("ward", "gmm"):
                for k in range(a.kmin, a.kmax + 1):
                    jac = jaccard_stability(zs, k, method, a.B, rng)
                    lab = cluster(zs, k, method)
                    nested[f"rol{m}_{method}_K{k}"] = {
                        "N": int(sub.sum()), "silhouette": round(float(silhouette_score(zs, lab)), 3),
                        "jaccard_ort": round(float(np.mean(jac)), 3), "jaccard_min": round(float(np.min(jac)), 3),
                        "en_kucuk_kume": int(np.bincount(lab).min())}
                    print(m, method, k, nested[f"rol{m}_{method}_K{k}"], flush=True)
        res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
        res[f"archetypes_v2_nested_{a.features}"] = nested
        RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
        return
    fit = ps["MIN"] >= a.fit_min
    z = z_all[fit].to_numpy()
    early = (ps.loc[fit, "Season"] <= 2019).to_numpy()

    scan = {}
    for method in ("ward", "gmm"):
        for k in range(a.kmin, a.kmax + 1):
            lab = cluster(z, k, method)
            # dönemler arası: erken dönemde kurulan modelin geç döneme uygulanması ile geç dönemde kurulan model
            le, ll = cluster(z[early], k, method), cluster(z[~early], k, method)
            cent_e = np.array([z[early][le == c].mean(axis=0) for c in range(k)])
            pred_l = ((z[~early][:, None, :] - cent_e[None]) ** 2).sum(-1).argmin(1)
            jac = jaccard_stability(z, k, method, a.B, rng)
            scan[f"{method}_K{k}"] = {
                "silhouette": round(float(silhouette_score(z, lab)), 3),
                "calinski_harabasz": round(float(calinski_harabasz_score(z, lab)), 1),
                "davies_bouldin": round(float(davies_bouldin_score(z, lab)), 3),
                "jaccard_ort": round(float(np.mean(jac)), 3),
                "jaccard_min": round(float(np.min(jac)), 3),
                "donemler_arasi_ARI": round(float(adjusted_rand_score(ll, pred_l)), 3),
                "en_kucuk_kume": int(np.bincount(lab).min()),
            }
            print(method, k, scan[f"{method}_K{k}"], flush=True)

    out = {"degiskenler": list(z_all.columns), "fit_asgari_dakika": a.fit_min, "fit_N": int(fit.sum()),
           "toplam_N": int(len(ps)), "B": a.B, "tarama": scan}

    if a.K:
        lab = cluster(z, a.K, a.method)
        cent = np.array([z[lab == c].mean(axis=0) for c in range(a.K)])
        assign = ((z_all.to_numpy()[:, None, :] - cent[None]) ** 2).sum(-1).argmin(1)
        assign[fit.to_numpy()] = lab
        ps["arketip_v2"] = assign + 1
        prof = (pd.concat([z_all, ps[["arketip_v2"]]], axis=1).groupby("arketip_v2")[list(z_all.columns)].mean().round(2))
        raw = ps.groupby("arketip_v2").agg(n=("Player_ID", "size"), VAL40=("VAL40", "mean"),
                                           MIN=("MIN", "mean"), eFG=("eFG", "mean")).round(2)
        out["nihai"] = {"yontem": a.method, "K": a.K, "profil_z": prof.to_dict(orient="index"),
                        "ozet": raw.to_dict(orient="index"),
                        "jaccard_kume": jaccard_stability(z, a.K, a.method, a.B, rng)}
        ps[["Player_ID", "Player", "Season", "Team", "MIN", "VAL40", "arketip_v2"]].rename(
            columns={"arketip_v2": "Arketip"}).to_csv(
            PROC / ("archetypes_v2.csv" if a.features == "base" else f"archetypes_v2_{a.features}.csv"), index=False)
        print(prof, "\n", raw)

    res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    res["archetypes_v2" if a.features == "base" else f"archetypes_v2_{a.features}"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
