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
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp
from sklearn.linear_model import Ridge

from lineup_model import PROC, RESULTS, SEED, columns, load, player_matrix

LAMBDA = 4000          # lineup_model.py'de çapraz doğrulamayla seçilen değer
ROSTER_MIN = 100       # ILP aday havuzu: ilk yarıda en az bu kadar dakika
# Rol kısıtları, nihai K'nın rol adlarından (role_names.json = K5, role_names_K4.json = K4) türetilir
_R = json.loads(RESULTS.read_text())
K_ROLES = _R["roles_final"]["K"]
_N = json.loads((Path(__file__).parent / ("role_names.json" if K_ROLES == 5 else f"role_names_K{K_ROLES}.json")).read_text())
BALLH = {int(k) for k, v in _N.items() if v == "Ball handler"}
RIMP = {int(k) for k, v in _N.items() if v == "Rim protector"}
BIGS = RIMP | {int(k) for k, v in _N.items() if v == "Interior big"}
METRICS = ["PIR40_sezon", "VAL40_sezon", "PIR40_havuz", "VAL40_havuz", "RAPM", "DAKIKA"]
COMMON = ["PIR40_havuz", "VAL40_havuz", "RAPM", "DAKIKA"]   # ortak alt küme: hepsinin tanımlı olduğu segmentler


def val40(d: pd.DataFrame) -> pd.Series:
    pos = d["Points"] + d["TotalRebounds"] + d["Assistances"] + d["Steals"] + d["BlocksFavour"]
    neg = ((d["FieldGoalsAttempted2"] - d["FieldGoalsMade2"]) + (d["FieldGoalsAttempted3"] - d["FieldGoalsMade3"])
           + (d["FreeThrowsAttempted"] - d["FreeThrowsMade"]) + d["Turnovers"])
    g = pd.DataFrame({"v": pos - neg, "m": d["MIN"], "p": d["Player_ID"]}).groupby("p").sum()
    return (g["v"] / g["m"] * 40).where(g["m"] >= 60)


def pir40(d: pd.DataFrame) -> pd.Series:
    """EuroLeague'in resmî Performance Index Rating'i (kutu skorundaki Valuation), 40 dakikaya."""
    g = d.groupby("Player_ID")[["Valuation", "MIN"]].sum()
    return (g["Valuation"] / g["MIN"] * 40).where(g["MIN"] >= 60)


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
    roles = pd.read_csv(PROC / f"roles_final_K{K_ROLES}.csv")
    role = dict(zip(zip(roles["Player_ID"], roles["Season"]), roles["Arketip"]))
    # İleriye bakmayı önlemek için kısıt rolleri: oyuncunun önceki sezonlardaki son rolü; yoksa (yeni oyuncu) o sezonun rolü
    srt = roles.sort_values("Season")
    prev_role, last_seen, n_cur, n_all = {}, {}, 0, 0
    for p_, s_, r_ in zip(srt["Player_ID"], srt["Season"], srt["Arketip"]):
        prev_role[(p_, s_)] = last_seen.get(p_, r_)
        last_seen[p_] = r_
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
        value = {"PIR40_sezon": pir40(pg_first).dropna().to_dict(), "PIR40_havuz": pir40(pg_pool).dropna().to_dict(), "VAL40_sezon": val40(pg_first).dropna().to_dict(), "VAL40_havuz": val40(pg_pool).dropna().to_dict(),
                 "RAPM": rapm, "DAKIKA": pg_first.groupby("Player_ID")["MIN"].sum().to_dict()}

        # Sınama 2: takım başına ILP beşlisi
        mins = pg_first.groupby(["Team", "Player_ID"])["MIN"].sum().reset_index()
        picks = {}
        for team, g in mins[mins["MIN"] >= ROSTER_MIN].groupby("Team"):
            ids = g["Player_ID"].tolist()
            rl = np.array([prev_role.get((p, s), 0) for p in ids])
            n_all += len(ids)
            n_cur += sum(1 for p in ids if (p, s) in prev_role and all(x[0] != p or x[1] >= s for x in ()) and
                         prev_role[(p, s)] == role.get((p, s)) and not any((p, s2) in role for s2 in range(2016, s)))
            for metric in ("PIR40_sezon", "VAL40_sezon", "RAPM", "DAKIKA"):  # DAKIKA: en çok süre alan beşli (taban)
                v = np.array([value[metric].get(p, np.nan) for p in ids])
                ok = ~np.isnan(v)
                for rule in ("yok", "tez", "dengeli"):
                    sel = ilp(v[ok], rl[ok], rule) if ok.sum() >= 5 else None
                    if sel is not None:
                        picks[(team, metric, rule)] = set(np.array(ids)[ok][sel])

        for (team, metric, rule), five in picks.items():
            coach = picks.get((team, "DAKIKA", rule))
            if coach is not None and metric != "DAKIKA":
                pick_rows.append({"metric": metric, "rule": rule, "overlap": len(five & coach)})

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

    out = {"K": K_ROLES, "kisit_rolu": "önceki sezon rolü (yeni oyuncularda o sezonun rolü)",
           "kisit_rolu_cari_sezondan_pay": round(n_cur / max(n_all, 1), 3),
           "segment_N": int(len(d)), "takim_sezon_N": int(len(clusters)), "B": a.B, "ev_sahibi_avantaji": round(home_adv, 2)}

    # Sınama 1
    def slopes(x, metrics=METRICS, common=False):
        res = []
        if common:
            x = x.dropna(subset=COMMON)
        for metric in metrics:
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
    # ortak alt kümede eğimler ve RAPM ile eşleştirilmiş farklar (aynı bootstrap örneklerinde)
    def common_and_diffs(x):
        e = slopes(x, COMMON, common=True)
        r = e[COMMON.index("RAPM")]
        return np.concatenate([e, [r - e[COMMON.index(m_)] for m_ in COMMON if m_ != "RAPM"]])
    est, lo, hi = boot(common_and_diffs)
    names = COMMON + [f"RAPM-{m_}" for m_ in COMMON if m_ != "RAPM"]
    out["ortak_alt_kume"] = {"segment_payi": round(float(d.dropna(subset=COMMON).shape[0] / len(d)), 3),
                             **{m_: {"egim": round(float(e), 2), "GA95": [round(float(l), 2), round(float(h), 2)]}
                                for m_, e, l, h in zip(names, est, lo, hi)}}
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

    def contrasts_and_diffs(x):
        c = contrasts(x)
        idx = {k_: i for i, k_ in enumerate(pcols)}
        diffs = [c[idx[k_]] - c[idx[f"pick_DAKIKA_{k_.rsplit('_', 1)[1]}"]] for k_ in pcols if "DAKIKA" not in k_]
        return np.concatenate([c, diffs])

    est_all, lo_all, hi_all = boot(contrasts_and_diffs)
    est, lo, hi = est_all[:len(pcols)], lo_all[:len(pcols)], hi_all[:len(pcols)]
    dnames = [k_[5:] for k_ in pcols if "DAKIKA" not in k_]
    out["ilp_antrenore_gore_fark"] = {k_: {"fark": round(float(e), 2), "GA95": [round(float(l), 2), round(float(h), 2)]}
                                     for k_, e, l, h in zip(dnames, est_all[len(pcols):], lo_all[len(pcols):], hi_all[len(pcols):])}
    # Doğrudan eşleştirilmiş karşılaştırma: aynı takım-sezonda yalnız ILP beşlisini içeren ve yalnız antrenör beşlisini
    # içeren segmentler (ikisini birden içerenler dışarıda); takım-sezon farkları iki grubun harmonik hücum ağırlığıyla ortalanır.
    def direct(x):
        res, meta = [], []
        for k_ in dnames:
            rule = k_.rsplit("_", 1)[1]
            fo = x[f"pick_{k_}"].fillna(False).astype(bool).values
            fc = x[f"pick_DAKIKA_{rule}"].fillna(False).astype(bool).values
            o, c = fo & ~fc, fc & ~fo
            g = pd.DataFrame({"ts": x["ts"].values, "yp": x["y_adj"].values * x["poss"].values, "p": x["poss"].values})
            go, gc = g[o].groupby("ts")[["yp", "p"]].sum(), g[c].groupby("ts")[["yp", "p"]].sum()
            j = go.join(gc, lsuffix="_o", rsuffix="_c", how="inner")
            if len(j) == 0:
                res.append(np.nan); meta.append((0, np.nan)); continue
            diff = j["yp_o"] / j["p_o"] - j["yp_c"] / j["p_c"]
            w = 1 / (1 / j["p_o"] + 1 / j["p_c"])
            res.append(float(np.average(diff, weights=w)))
            both = (fo & fc).sum() / max(fo.sum(), 1)
            meta.append((len(j), both))
        return np.array(res), meta

    def direct_est(x):
        return direct(x)[0]
    est_d, lo_d, hi_d = boot(direct_est)
    meta = direct(d)[1]
    out["dogrudan_eslestirilmis_fark"] = {k_: {"fark": round(float(e), 2), "GA95": [round(float(l), 2), round(float(h), 2)],
                                               "takim_sezon": int(mt[0]), "iki_gruba_da_giren_pay": round(float(mt[1]), 3)}
                                          for k_, e, l, h, mt in zip(dnames, est_d, lo_d, hi_d, meta)}
    pr = pd.DataFrame(pick_rows)
    out["antrenor_beslisiyle_ortak_oyuncu"] = pr.groupby(["metric", "rule"])["overlap"].mean().round(2).rename(
        lambda t: t, axis=0).to_dict() if len(pr) else {}
    out["antrenor_beslisiyle_ortak_oyuncu"] = {f"{a_}_{b_}": v for (a_, b_), v in out["antrenor_beslisiyle_ortak_oyuncu"].items()}
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
