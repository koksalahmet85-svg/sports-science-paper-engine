"""Dizilim modeli: oyuncu RAPM + rol bileşimi etkisi (OPEN_QUESTIONS #2, #4, #22).

Gözlem birimi: 5'e 5 segment (stint). y = 100 hücum başına net sayı farkı (A − B), ağırlık = ortalama hücum sayısı.
1. RAPM: ridge regresyon, sahadaki her oyuncu için +1 (A) / −1 (B); az hücumlu oyuncular tek "yedek" sütununda.
   λ, maç bazında gruplanmış çapraz doğrulamayla seçilir. Sabit terim ev sahibi avantajıdır (A = ev sahibi).
2. Zamansal doğrulama (eğitim 2016–2022, test 2023–2024): sabit / VAL40 toplamı / RAPM / RAPM + rol bileşimi
   modellerinin test segmentlerindeki ağırlıklı R²'si.
3. Rol bileşimi: RAPM artığı üzerinde ridge; öznitelikler rol sayıları ve rol çifti çarpımları (A − B farkı).
   Anlamlılık: rol etiketleri sezon içinde oyuncular arasında karıştırılarak (permütasyon) test R² kazancının
   sıfır dağılımı kurulur — "bileşim, bireysel kalitenin ötesinde bilgi taşıyor mu?"
4. Tüm veriyle nihai RAPM → data/processed/rapm.csv; rol başına RAPM ve VAL40 karşılaştırması.

    python manuscript/analysis/lineup_model.py --roles archetypes_v2_full.csv --B 500
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
RESULTS = Path(__file__).with_name("results.json")
SEED = 20261111
LAMBDAS = [500, 1000, 2000, 4000, 8000]
MIN_POSS = 300  # bunun altındaki oyuncular "yedek" sütununda toplanır


def load() -> pd.DataFrame:
    st = pd.read_csv(PROC / "stints_corrected.csv.gz")
    st = st[st["full"]].copy()
    st["poss"] = (st["poss_A"] + st["poss_B"]) / 2
    st = st[st["poss"] >= 1].reset_index(drop=True)
    st["y"] = 100 * (st["pts_A"] - st["pts_B"]) / st["poss"]
    st["game"] = st["Season"] * 1000 + st["Gamecode"]
    st["LA"] = st["lineup_A"].str.split("|")
    st["LB"] = st["lineup_B"].str.split("|")
    return st


def player_matrix(st: pd.DataFrame, cols: dict, seen: set | None = None) -> sparse.csr_matrix:
    """`seen` verilirse (test verisi) eğitimde hiç görülmemiş oyuncular 0 (lig ortalaması) sayılır;
    "yedek" katsayısı yalnızca eğitimde görülüp az hücum oynamış oyunculara uygulanır."""
    r, c, v = [], [], []
    rep = cols["__yedek__"]
    for i, (la, lb) in enumerate(zip(st["LA"], st["LB"])):
        for sign, lu in ((1.0, la), (-1.0, lb)):
            for p in lu:
                if seen is not None and p not in seen:
                    continue
                r.append(i), c.append(cols.get(p, rep)), v.append(sign)
    return sparse.csr_matrix((v, (r, c)), shape=(len(st), len(cols)))


def columns(st: pd.DataFrame) -> dict:
    poss = pd.concat([st[["LA", "poss"]].explode("LA").rename(columns={"LA": "p"}),
                      st[["LB", "poss"]].explode("LB").rename(columns={"LB": "p"})]).groupby("p")["poss"].sum()
    cols = {p: i for i, p in enumerate(poss[poss >= MIN_POSS].index)}
    cols["__yedek__"] = len(cols)
    return cols


def fit_rapm(st, lam, cols=None):
    cols = cols or columns(st)
    m = Ridge(alpha=lam, fit_intercept=True).fit(player_matrix(st, cols), st["y"], sample_weight=st["poss"])
    return m, cols


def wr2(y, pred, w):
    mu = np.average(y, weights=w)
    return 1 - np.sum(w * (y - pred) ** 2) / np.sum(w * (y - mu) ** 2)


def role_features(st: pd.DataFrame, role: dict, k: int) -> np.ndarray:
    """Rol sayıları (0 = rolü olmayan/az süreli) ve rol çifti çarpımları; A − B farkı."""
    pairs = list(combinations_with_replacement(range(1, k + 1), 2))

    def side(lineups, seasons):
        n = np.zeros((len(lineups), k + 1))
        for i, (lu, s) in enumerate(zip(lineups, seasons)):
            for p in lu:
                n[i, role.get((p, s), 0)] += 1
        inter = np.column_stack([n[:, a] * n[:, b] if a != b else n[:, a] * (n[:, a] - 1) / 2 for a, b in pairs])
        return np.hstack([n[:, 1:], inter])

    return side(st["LA"], st["Season"]) - side(st["LB"], st["Season"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roles", default="archetypes_v2_full.csv")
    ap.add_argument("--B", type=int, default=500)
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)
    st = load()
    roles = pd.read_csv(PROC / a.roles)
    k = int(roles["Arketip"].max())
    role = dict(zip(zip(roles["Player_ID"], roles["Season"]), roles["Arketip"]))
    tr, te = st[st["Season"] <= 2022].reset_index(drop=True), st[st["Season"] >= 2023].reset_index(drop=True)

    # 1. λ seçimi (eğitim dönemi, maç bazında gruplu 5 kat)
    cols_tr = columns(tr)
    xtr = player_matrix(tr, cols_tr)
    cv = {}
    for lam in LAMBDAS:
        pred = np.zeros(len(tr))
        for f_tr, f_te in GroupKFold(5).split(xtr, groups=tr["game"]):
            m = Ridge(alpha=lam).fit(xtr[f_tr], tr["y"].values[f_tr], sample_weight=tr["poss"].values[f_tr])
            pred[f_te] = m.predict(xtr[f_te])
        cv[lam] = round(float(wr2(tr["y"].values, pred, tr["poss"].values)), 5)
    lam = max(cv, key=cv.get)

    # 2. Zamansal doğrulama
    rapm_tr, _ = fit_rapm(tr, lam, cols_tr)
    seen = set(tr["LA"].explode()) | set(tr["LB"].explode())
    p_rapm_tr, p_rapm_te = rapm_tr.predict(xtr), rapm_tr.predict(player_matrix(te, cols_tr, seen))
    share_seen = float(np.mean([p in seen for lu in pd.concat([te["LA"], te["LB"]]) for p in lu]))
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    v = ps[ps["Season"] <= 2022].groupby("Player_ID").apply(lambda d: np.average(d["VAL40"], weights=d["MIN"]),
                                                            include_groups=False)
    vmean = float(v.mean())

    def valsum(d):
        s = lambda col: np.array([sum(v.get(p, vmean) for p in lu) for lu in d[col]])
        return (s("LA") - s("LB")).reshape(-1, 1)

    val = Ridge(alpha=1e-6).fit(valsum(tr), tr["y"], sample_weight=tr["poss"])
    yte, wte = te["y"].values, te["poss"].values
    base = float(np.average(tr["y"], weights=tr["poss"]))

    # 3. Rol bileşimi (RAPM artığı üzerinde) + permütasyon
    def comp_gain(role_map):
        ftr, fte = role_features(tr, role_map, k), role_features(te, role_map, k)
        m = Ridge(alpha=5000).fit(ftr, tr["y"].values - p_rapm_tr, sample_weight=tr["poss"].values)
        return wr2(yte, p_rapm_te + m.predict(fte), wte), m

    r2_comp, comp = comp_gain(role)
    r2_rapm = wr2(yte, p_rapm_te, wte)
    gain = r2_comp - r2_rapm
    null = []
    for _ in range(a.B):
        sh = roles.assign(Arketip=roles.groupby("Season")["Arketip"].transform(lambda s: rng.permutation(s.values)))
        null.append(comp_gain(dict(zip(zip(sh["Player_ID"], sh["Season"]), sh["Arketip"])))[0] - r2_rapm)
    null = np.array(null)

    pairs = list(combinations_with_replacement(range(1, k + 1), 2))
    names = [f"n{r}" for r in range(1, k + 1)] + [f"n{x}×n{y}" for x, y in pairs]
    coef = pd.Series(comp.coef_, index=names).round(3)

    # 4. Nihai RAPM (tüm veri)
    full, cols = fit_rapm(st, lam)
    rapm = pd.Series(full.coef_[:-1], index=[p for p in cols if p != "__yedek__"], name="RAPM")
    pd.DataFrame({"Player_ID": rapm.index, "RAPM": rapm.values}).to_csv(PROC / "rapm.csv", index=False)
    car = ps.groupby("Player_ID").apply(lambda d: pd.Series({
        "VAL40": np.average(d["VAL40"], weights=d["MIN"]), "MIN": d["MIN"].sum()}), include_groups=False)
    main_role = (roles.merge(ps[["Player_ID", "Season", "MIN"]], on=["Player_ID", "Season"], suffixes=("", "_ps"))
                 .groupby(["Player_ID", "Arketip"])["MIN_ps"].sum().reset_index()
                 .sort_values("MIN_ps").groupby("Player_ID").tail(1).set_index("Player_ID")["Arketip"])
    j = car.join(rapm, how="inner").join(main_role)

    def eta2(c):
        g = j.groupby("Arketip")[c]
        return float(((g.transform("mean") - j[c].mean()) ** 2).sum() / ((j[c] - j[c].mean()) ** 2).sum())

    out = {
        "roller": a.roles, "K": k, "segment_N": int(len(st)), "egitim_N": int(len(tr)), "test_N": int(len(te)),
        "lambda_cv": cv, "lambda": lam, "yedek_katsayisi": round(float(full.coef_[-1]), 2),
        "testte_egitimde_gorulen_oyuncu_payi": round(share_seen, 3), "ev_sahibi_avantaji": round(float(full.intercept_), 2),
        "rapm_oyuncu_N": int(len(rapm)), "rapm_sd": round(float(rapm.std()), 2),
        "test_R2": {"sabit": round(float(wr2(yte, np.full(len(te), base), wte)), 5),
                    "VAL40_toplami": round(float(wr2(yte, val.predict(valsum(te)), wte)), 5),
                    "RAPM": round(float(r2_rapm), 5), "RAPM_rol_bilesimi": round(float(r2_comp), 5)},
        "rol_bilesimi": {"kazanc": round(float(gain), 5), "B": a.B,
                         "null_ort": round(float(null.mean()), 5), "null_p95": round(float(np.quantile(null, .95)), 5),
                         "p": round(float((1 + (null >= gain).sum()) / (1 + a.B)), 4),
                         "en_buyuk_katsayilar": coef.reindex(coef.abs().sort_values(ascending=False).index).head(8).to_dict()},
        "korelasyon_RAPM_VAL40": round(float(j["RAPM"].corr(j["VAL40"])), 3),
        "eta2_rol": {"RAPM": round(eta2("RAPM"), 3), "VAL40": round(eta2("VAL40"), 3)},
        "rol_ortalamalari": j.groupby("Arketip")[["RAPM", "VAL40"]].mean().round(2).to_dict(orient="index"),
        "en_yuksek_RAPM": (j.join(ps.groupby("Player_ID")["Player"].first()).sort_values("RAPM", ascending=False)
                           .head(15)[["Player", "RAPM", "VAL40"]].round(2).values.tolist()),
    }
    res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    res[f"lineup_model_K{k}"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
