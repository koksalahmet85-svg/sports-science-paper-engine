"""ILP kadro seçiminin örneklem dışı sınaması: VAL40 mı, RAPM mi? (OPEN_QUESTIONS #4, #22, #25)

Her sezon ikiye bölünür (maç koduna göre ilk yarı / ikinci yarı). Oyuncu değerleri yalnızca kesim noktasından
ÖNCEKİ bilgiyle hesaplanır; değerlendirme sezonun ikinci yarısındaki gerçek dizilim segmentlerinde yapılır.

Oyuncu değeri ölçütleri
  VAL40_sezon : sezonun ilk yarısındaki VAL40 (tezdeki ölçüt)
  VAL40_havuz : önceki sezonlar + ilk yarı, dakika ağırlıklı VAL40
  RAPM        : önceki sezonlar + ilk yarı segmentleriyle ridge RAPM
  DAKIKA      : ilk yarıda oynanan dakika (antrenörün kendi sıralaması; karşılaştırma tabanı)

Sınama 1 — amaç fonksiyonunun geçerliliği: ikinci yarıdaki her segmentte dizilimin "toplam değeri" (ILP'nin maksimize
  ettiği büyüklük), takım-sezon içinde z-skorlanır; segmentin 100 hücum başına net sayı farkı bu z'ye regrese edilir
  (rakip dizilimin RAPM toplamı ve ev sahipliği kontrol edilir; ağırlık = hücum). Eğim: toplam değer 1 SS arttığında
  net sayı farkı kaç sayı artıyor. GA: takım-sezon kümeli bootstrap.
Sınama 2 — ILP'nin seçtiği beşli: her takım-sezon için ilk yarı kadrosundan (≥ 100 dk) ILP ile en yüksek toplam
  değerli beşli seçilir (kısıtlar: yok / tezdeki gibi ≥ 1 Boyalı Alan Koruyucusu / dengeli: ≥ 1 Top Taşıyıcı ve
  1–2 uzun). İkinci yarıda bu beşliden ≥ 4 oyuncu içeren segmentlerin rakibe göre düzeltilmiş net sayı farkı,
  aynı takımın diğer segmentleriyle karşılaştırılır.

    python manuscript/analysis/ilp_validation.py --B 1000
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp
from sklearn.linear_model import Ridge

from lineup_model import PROC, RESULTS, SEED, columns, load, player_matrix

LAMBDA = 4000          # lineup_model.py'de çapraz doğrulamayla seçilen değer
ROSTER_MIN = 100       # ILP aday havuzu: ilk yarıda en az bu kadar dakika
BALLH, BIGS, RIMP = {1}, {2, 4}, {4}   # archetypes_v2_full.csv: 1 Top Taşıyıcı, 2 İç Saha F., 4 Boyalı Alan K.
METRICS = ["VAL40_sezon", "VAL40_havuz", "RAPM", "DAKIKA"]


def val40(d: pd.DataFrame) -> pd.Series:
    pos = d["Points"] + d["TotalRebounds"] + d["Assistances"] + d["Steals"] + d["BlocksFavour"]
    neg = ((d["FieldGoalsAttempted2"] - d["FieldGoalsMade2"]) + (d["FieldGoalsAttempted3"] - d["FieldGoalsMade3"])
           + (d["FreeThrowsAttempted"] - d["FreeThrowsMade"]) + d["Turnovers"])
    g = pd.DataFrame({"v": pos - neg, "m": d["MIN"], "p": d["Player_ID"]}).groupby("p").sum()
    return (g["v"] / g["m"] * 40).where(g["m"] >= 60)


def ilp(values: np.ndarray, roles: np.ndarray, rule: str) -> np.ndarray | None:
    cons = [LinearConstraint(np.ones(len(values)), 5, 5)]
    if rule == "tez":
        cons.append(LinearConstraint(np.isin(roles, list(RIMP)).astype(float), 1, 5))
    if rule == "dengeli":
        cons.append(LinearConstraint(np.isin(roles, list(BALLH)).astype(float), 1, 5))
        cons.append(LinearConstraint(np.isin(roles, list(BIGS)).astype(float), 1, 2))
    r = milp(-values, constraints=cons, integrality=np.ones(len(values)), bounds=Bounds(0, 1))
    return np.round(r.x).astype(bool) if r.success else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=1000)
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)
    st, pg = load(), pd.read_csv(PROC / "player_game.csv.gz")
    roles = pd.read_csv(PROC / "archetypes_v2_full.csv")
    role = dict(zip(zip(roles["Player_ID"], roles["Season"]), roles["Arketip"]))
    seg_rows, pick_rows = [], []

    for s in sorted(st["Season"].unique()):
        cut = st.loc[st["Season"] == s, "Gamecode"].median()
        tr = st[(st["Season"] < s) | ((st["Season"] == s) & (st["Gamecode"] <= cut))].reset_index(drop=True)
        te = st[(st["Season"] == s) & (st["Gamecode"] > cut)].reset_index(drop=True)
        pg_first = pg[(pg["Season"] == s) & (pg["Gamecode"] <= cut)]
        pg_pool = pg[(pg["Season"] < s) | ((pg["Season"] == s) & (pg["Gamecode"] <= cut))]
        cols = columns(tr)
        m = Ridge(alpha=LAMBDA).fit(player_matrix(tr, cols), tr["y"], sample_weight=tr["poss"])
        seen = set(tr["LA"].explode()) | set(tr["LB"].explode())
        rapm = {p: (m.coef_[cols.get(p, cols["__yedek__"])] if p in seen else 0.0)
                for p in set(te["LA"].explode()) | set(te["LB"].explode()) | set(pg_first["Player_ID"])}
        value = {"VAL40_sezon": val40(pg_first).dropna().to_dict(), "VAL40_havuz": val40(pg_pool).dropna().to_dict(),
                 "RAPM": rapm, "DAKIKA": pg_first.groupby("Player_ID")["MIN"].sum().to_dict()}

        # Sınama 2: takım başına ILP beşlisi
        mins = pg_first.groupby(["Team", "Player_ID"])["MIN"].sum().reset_index()
        picks = {}
        for team, g in mins[mins["MIN"] >= ROSTER_MIN].groupby("Team"):
            ids = g["Player_ID"].tolist()
            rl = np.array([role.get((p, s), 0) for p in ids])
            for metric in ("VAL40_sezon", "RAPM", "DAKIKA"):  # DAKIKA: en çok süre alan beşli (taban)
                v = np.array([value[metric].get(p, np.nan) for p in ids])
                ok = ~np.isnan(v)
                for rule in ("yok", "tez", "dengeli"):
                    sel = ilp(v[ok], rl[ok], rule) if ok.sum() >= 5 else None
                    if sel is not None:
                        picks[(team, metric, rule)] = set(np.array(ids)[ok][sel])

        for us, them, sign in (("A", "B", 1.0), ("B", "A", -1.0)):
            lu, opp = te[f"L{us}"], te[f"L{them}"]
            rec = pd.DataFrame({"Season": s, "team": te[f"team_{us}"], "y": sign * te["y"], "poss": te["poss"],
                                "home": float(us == "A"), "opp": [sum(rapm.get(p, 0.0) for p in o) for o in opp]})
            for metric in METRICS:
                rec[metric] = [sum(value[metric].get(p, np.nan) for p in l) for l in lu]
            for (team, metric, rule), five in picks.items():
                col = f"pick_{metric}_{rule}"
                hit = np.array([len(five & set(l)) >= 4 for l in lu]) & (rec["team"] == team).values
                rec[col] = rec.get(col, False) | hit
            seg_rows.append(rec)
        print(s, "eğitim", len(tr), "test", len(te), flush=True)

    d = pd.concat(seg_rows, ignore_index=True)
    d["ts"] = d["Season"].astype(str) + "_" + d["team"]
    home_adv = float(np.average(d.loc[d["home"] == 1, "y"], weights=d.loc[d["home"] == 1, "poss"]))
    d["y_adj"] = d["y"] + d["opp"] - home_adv * (2 * d["home"] - 1)
    clusters = d["ts"].unique()
    idx_of = {c: np.where(d["ts"].values == c)[0] for c in clusters}

    def boot(fn):
        est = fn(d)
        bs = [fn(d.iloc[np.concatenate([idx_of[c] for c in rng.choice(clusters, len(clusters))])])
              for _ in range(a.B)]
        lo, hi = np.nanpercentile(bs, [2.5, 97.5], axis=0)
        return est, lo, hi

    out = {"segment_N": int(len(d)), "takim_sezon_N": int(len(clusters)), "B": a.B, "ev_sahibi_avantaji": round(home_adv, 2)}

    # Sınama 1
    def slopes(x):
        res = []
        for metric in METRICS:
            q = x.dropna(subset=[metric])
            z = q.groupby("ts")[metric].transform(lambda c: (c - c.mean()) / (c.std(ddof=0) or np.nan))
            ok = z.notna().values
            X = np.column_stack([np.ones(ok.sum()), z[ok], q["opp"].values[ok], q["home"].values[ok]])
            w = q["poss"].values[ok]
            beta = np.linalg.lstsq(X * np.sqrt(w)[:, None], q["y"].values[ok] * np.sqrt(w), rcond=None)[0]
            res.append(beta[1])
        return np.array(res)

    est, lo, hi = boot(slopes)
    out["amac_fonksiyonu_egimi"] = {m_: {"egim": round(float(e), 2), "GA95": [round(float(l), 2), round(float(h), 2)]}
                                    for m_, e, l, h in zip(METRICS, est, lo, hi)}
    out["kapsam"] = {m_: round(float(d[m_].notna().mean()), 3) for m_ in METRICS}

    # Sınama 2
    pcols = [c for c in d.columns if c.startswith("pick_")]

    def contrasts(x):
        res = []
        for c in pcols:
            f = x[c].fillna(False).astype(bool).values
            teams_with = set(x.loc[f, "ts"])
            rest = (~f) & x["ts"].isin(teams_with).values
            if f.sum() == 0 or rest.sum() == 0:
                res.append(np.nan)
                continue
            res.append(np.average(x["y_adj"].values[f], weights=x["poss"].values[f])
                       - np.average(x["y_adj"].values[rest], weights=x["poss"].values[rest]))
        return np.array(res)

    est, lo, hi = boot(contrasts)
    out["ilp_beslisi"] = {}
    for c, e, l, h in zip(pcols, est, lo, hi):
        f = d[c].fillna(False).astype(bool)
        out["ilp_beslisi"][c[5:]] = {"fark": round(float(e), 2), "GA95": [round(float(l), 2), round(float(h), 2)],
                                     "hucum_payi": round(float(d.loc[f, "poss"].sum() / d["poss"].sum()), 3),
                                     "takim_sezon": int(d.loc[f, "ts"].nunique())}
    res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    res["ilp_validation"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
