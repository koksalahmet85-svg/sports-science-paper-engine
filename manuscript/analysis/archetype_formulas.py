"""OPEN_QUESTIONS #2 — "Başarılı formüllerde arketip dağılımı rastlantısal değil" iddiasının sınanması.

1. Tez EK-2.5'i aynen uygular: 9 değişken, z-skor, Ward, K = 7.
2. Kümeleri tez Tablo 3'teki arketiplere (OK, ÇYF, BAS, YHS, KŞ, SDAK, DKR) profil benzerliğiyle eşler.
3. Tezin formül testini tekrarlar: dizilim-maç gözlemleri → arketip formülü (5'li çoklu küme),
   N ≥ 10 formüllerde tek örneklem t-testi (H0: μ = 0), p < ,05 "anlamlı formül";
   anlamlı formüllerdeki arketip payları için χ² (gerçek beklenti: tüm segmentlerdeki dakika payı).
4. Bu seçim sürecinin tamamını, NRTG40'ı takım-sezon blokları içinde karıştırarak (permütasyon)
   B kez tekrarlar: çoklu testi, formül seçimini ve aynı formüldeki 5 gözlemin bağımlılığını hesaba katan
   doğru sıfır dağılımı.
5. Benjamini–Hochberg ile kaç formülün yanlış keşif düzeltmesinden sonra kaldığını raporlar.

Sonuçlar results.json içinde "formula_test" anahtarına yazılır.

    python manuscript/analysis/archetype_formulas.py --stints corrected --B 1000
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
RESULTS = Path(__file__).with_name("results.json")
SEED = 20261104

KDEG = ["Points_40", "TotalRebounds_40", "Assistances_40", "Steals_40", "BlocksFavour_40",
        "USG_proxy", "FG3_PCT", "FT_PCT", "eFG"]
# Tez Tablo 3: n, PTS/maç, REB/maç, AST/maç, BLK/maç, USG/maç, eFG, VAL40
THESIS = pd.DataFrame(
    [["OK", 456, 10.23, 2.27, 3.30, 0.09, 10.89, .507, 17.39],
     ["ÇYF", 74, 7.70, 4.52, 0.88, 0.61, 7.14, .612, 22.54],
     ["BAS", 237, 7.20, 4.00, 0.74, 0.63, 6.64, .614, 22.49],
     ["YHS", 192, 10.97, 4.42, 1.47, 0.28, 10.59, .558, 20.22],
     ["KŞ", 514, 6.54, 2.32, 1.14, 0.15, 6.19, .577, 16.13],
     ["SDAK", 196, 3.49, 2.34, 0.68, 0.23, 3.86, .515, 14.08],
     ["DKR", 345, 3.79, 1.62, 1.11, 0.08, 4.44, .468, 11.75]],
    columns=["arketip", "n", "PTS", "REB", "AST", "BLK", "USG", "eFG", "VAL40"]).set_index("arketip")


def archetypes(ps: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    z = StandardScaler().fit_transform(ps[KDEG])
    lab = fcluster(linkage(z, method="ward"), 7, criterion="maxclust")
    ps = ps.assign(kume=lab)
    g = ps["G"].where(ps["G"] > 0, 1)
    prof = pd.DataFrame({
        "n": ps.groupby("kume").size(),
        "PTS": (ps["Points"] / g).groupby(ps["kume"]).mean(),
        "REB": (ps["TotalRebounds"] / g).groupby(ps["kume"]).mean(),
        "AST": (ps["Assistances"] / g).groupby(ps["kume"]).mean(),
        "BLK": (ps["BlocksFavour"] / g).groupby(ps["kume"]).mean(),
        "USG": ((ps["FieldGoalsAttempted2"] + ps["FieldGoalsAttempted3"] + 0.44 * ps["FreeThrowsAttempted"]
                 + ps["Turnovers"]) / g).groupby(ps["kume"]).mean(),
        "eFG": ps.groupby("kume")["eFG"].mean(),
        "VAL40": ps.groupby("kume")["VAL40"].mean(),
    })
    cols = ["PTS", "REB", "AST", "BLK", "USG", "eFG", "VAL40"]
    sd = THESIS[cols].std()
    cost = np.array([[(((prof.loc[k, cols] - THESIS.loc[a, cols]) / sd) ** 2).sum() for a in THESIS.index]
                     for k in prof.index])
    rows, colsi = linear_sum_assignment(cost)
    mapping = {int(prof.index[r]): THESIS.index[c] for r, c in zip(rows, colsi)}
    ps["arketip"] = ps["kume"].map(mapping)
    prof.index = prof.index.map(mapping)
    info = {"silhouette_K7": round(float(silhouette_score(z, lab)), 3),
            "boyutlar": {a: int(prof.loc[a, "n"]) for a in THESIS.index},
            "tez_boyutlar": THESIS["n"].to_dict(),
            "eslesme_maliyeti": round(float(cost[rows, colsi].sum()), 2)}
    return ps, info


def lineup_games(st: pd.DataFrame, arch: dict) -> tuple[pd.DataFrame, pd.Series]:
    st = st[st["full"] & (st["dur"] >= 10 / 60)]
    recs = []
    for us, them in (("A", "B"), ("B", "A")):
        recs.append(pd.DataFrame({
            "Season": st["Season"], "Gamecode": st["Gamecode"], "team": st[f"team_{us}"],
            "lineup": st[f"lineup_{us}"], "dur": st["dur"],
            "pf": st[f"pts_{us}"], "pa": st[f"pts_{them}"]}))
    seg = pd.concat(recs, ignore_index=True)

    def formula(row):
        labs = [arch.get((pid, row.Season)) for pid in row.lineup.split("|")]
        return None if None in labs else "+".join(sorted(labs))

    seg["formula"] = [formula(r) for r in seg[["lineup", "Season"]].itertuples()]
    # Beklenti tabanı: arketiplerin tüm segmentlerdeki dakika payı (tezdeki "gerçek beklenti")
    slots = seg.dropna(subset=["formula"]).assign(a=lambda d: d["formula"].str.split("+")).explode("a")
    expected = slots.groupby("a")["dur"].sum()
    expected = expected / expected.sum()
    lg = (seg.dropna(subset=["formula"])
          .groupby(["Season", "Gamecode", "team", "lineup", "formula"], as_index=False)[["dur", "pf", "pa"]].sum())
    lg["NRTG40"] = (lg["pf"] - lg["pa"]) / lg["dur"] * 40
    return lg, expected


def select(lg: pd.DataFrame, y: np.ndarray, min_n: int = 10, alpha: float = .05):
    d = pd.DataFrame({"formula": lg["formula"].values, "y": y})
    g = d.groupby("formula")["y"]
    n, m, s = g.size(), g.mean(), g.std(ddof=1)
    keep = n >= min_n
    t = m[keep] / (s[keep] / np.sqrt(n[keep]))
    p = pd.Series(2 * stats.t.sf(np.abs(t), n[keep] - 1), index=t.index)
    return p, m[keep]


def composition(formulas, order) -> pd.Series:
    c = pd.Series([a for f in formulas for a in f.split("+")]).value_counts()
    return c.reindex(order, fill_value=0)


def chi2_stat(obs: pd.Series, exp_share: pd.Series) -> float:
    if obs.sum() == 0:
        return 0.0
    e = exp_share.reindex(obs.index) * obs.sum()
    return float(((obs - e) ** 2 / e).sum())


def bh(p: pd.Series, q: float = .05) -> int:
    ps = np.sort(p.values)
    ok = ps <= q * np.arange(1, len(ps) + 1) / len(ps)
    return int(ok.nonzero()[0].max() + 1) if ok.any() else 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stints", default="corrected", choices=["corrected", "thesis"])
    ap.add_argument("--B", type=int, default=1000)
    ap.add_argument("--arketip-dosyasi", type=Path,
                    help="tezin oyuncu_sezon_arketip.csv dosyası (Player_ID, Season, Arketip = 1..7); verilirse kümeleme atlanır")
    ap.add_argument("--min-dur", type=float, default=0.0,
                    help="dizilim-maç başına asgari dakika (duyarlılık; 0 = tezdeki gibi filtre yok)")
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)

    if a.arketip_dosyasi:
        # Tez Tablo 3: K1 = OK ... K7 = DKR
        ps = pd.read_csv(a.arketip_dosyasi)
        ps["Player_ID"] = ps["Player_ID"].astype(str).str.strip()
        ps["arketip"] = ps["Arketip"].map(dict(enumerate(THESIS.index, start=1)))
        cl = {"kaynak": str(a.arketip_dosyasi.name),
              "boyutlar": ps["arketip"].value_counts().reindex(THESIS.index).fillna(0).astype(int).to_dict()}
    else:
        ps, cl = archetypes(pd.read_csv(PROC / "player_season.csv.gz"))
    arch = dict(zip(zip(ps["Player_ID"], ps["Season"]), ps["arketip"]))
    lg, expected = lineup_games(pd.read_csv(PROC / f"stints_{a.stints}.csv.gz"), arch)
    lg = lg[lg["dur"] >= a.min_dur].reset_index(drop=True)
    order = list(THESIS.index)

    p, mean = select(lg, lg["NRTG40"].values)
    sig = p[p < .05].index
    obs = composition(sig, order)
    chi_obs = chi2_stat(obs, expected)
    chi_p_naive = float(stats.chi2.sf(chi_obs, len(order) - 1))
    resid = ((obs - expected.reindex(order) * obs.sum()) / np.sqrt(expected.reindex(order) * obs.sum())).round(2)
    dkr_share = float(obs["DKR"] / obs.sum()) if obs.sum() else 0.0

    # Permütasyon: NRTG40'ı takım-sezon blokları içinde karıştır, tüm seçim sürecini tekrarla
    blocks = lg.groupby(["Season", "team"]).indices.values()
    null_chi, null_dkr, null_nsig = [], [], []
    y = lg["NRTG40"].values
    for _ in range(a.B):
        yp = y.copy()
        for idx in blocks:
            yp[idx] = y[rng.permutation(idx)]
        pp, _ = select(lg, yp)
        sg = pp[pp < .05].index
        o = composition(sg, order)
        null_chi.append(chi2_stat(o, expected))
        null_dkr.append(o["DKR"] / o.sum() if o.sum() else 0.0)
        null_nsig.append(len(sg))
    null_chi, null_dkr, null_nsig = map(np.array, (null_chi, null_dkr, null_nsig))

    out = {
        "stint_modu": a.stints,
        "asgari_dakika": a.min_dur,
        "NRTG40_ort_agirliksiz": round(float(lg["NRTG40"].mean()), 2),
        "NRTG40_ort_dakika_agirlikli": round(float((lg["pf"] - lg["pa"]).sum() / lg["dur"].sum() * 40), 2),
        "kumeleme": cl,
        "dizilim_mac_N": int(len(lg)),
        "test_edilen_formul": int(len(p)),
        "anlamli_formul": int(len(sig)),
        "anlamli_formul_pozitif": int((mean[sig] > 0).sum()),
        "beklenen_yanlis_pozitif": round(.05 * len(p), 1),
        "bh_fdr_sonrasi_kalan": bh(p),
        "arketip_gozlem_N": int(obs.sum()),
        "chi2": round(chi_obs, 2),
        "chi2_p_naif": chi_p_naive,
        "standart_artik": resid.to_dict(),
        "DKR_payi": round(dkr_share, 3),
        "permutasyon": {
            "B": a.B,
            "chi2_p": round(float((1 + (null_chi >= chi_obs).sum()) / (1 + a.B)), 4),
            "DKR_payi_p": round(float((1 + (null_dkr >= dkr_share).sum()) / (1 + a.B)), 4),
            "anlamli_formul_sayisi_p": round(float((1 + (null_nsig >= len(sig)).sum()) / (1 + a.B)), 4),
            "null_anlamli_formul_ort": round(float(null_nsig.mean()), 1),
            "null_chi2_ort": round(float(null_chi.mean()), 2),
        },
    }
    res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    res.setdefault("status", "ok")
    tag = "_tezarketip" if a.arketip_dosyasi else ""
    res[f"formula_test_{a.stints}_min{a.min_dur:g}{tag}"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
