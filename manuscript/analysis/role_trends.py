"""Makale A ek analizi: rollerin 2016 → 2024 eğilimleri → results.json["role_trends"].

Roller sezon içinde standartlaştırılmış değişkenlerle tanımlandığından (roles_final.py), rol payları ligin
mutlak oyun tarzındaki değişimi değil, oyuncuların birbirine göre konumunun dağılımını yansıtır. Mutlak
değişim ayrıca ham (standartlaştırılmamış) değişkenlerin rol içi eğilimleriyle ölçülür.

  1. Sezon başına rol payları (dakika ağırlıklı) ve doğrusal eğilim (sezon başına yüzde puan);
     %95 GA oyuncu kümeli bootstrap ile.
  2. Sezon başına rol × kayıtlı pozisyon Cramér V ve eğilimi ("pozisyonsuzluk" göstergesi).
  3. Rol belirsizliği: en yüksek sonsal olasılığı < 0,7 olan oyuncu-sezon payı, sezon başına ve eğilimi.
  4. Ardışık sezonlarda aynı oyuncunun rol geçişleri: aynı rolde kalma oranı ve geçiş matrisi.
  5. Rol içi ham değişken eğilimleri (üçlük deneme oranı, pota altı payı, asist %).

    python manuscript/analysis/role_trends.py --B 1000
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd

from lineup_model import PROC, RESULTS, SEED
from roles_final import cramers_v, raw_features

RAW = ["3PAr", "rim_rate", "AST_pct", "USG_pct", "c3_share"]


def slope(x: np.ndarray, y: np.ndarray, w: np.ndarray | None = None) -> float:
    w = np.ones_like(y) if w is None else w
    xm = np.average(x, weights=w)
    return float(np.sum(w * (x - xm) * (y - np.average(y, weights=w))) / np.sum(w * (x - xm) ** 2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=1000)
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)
    res = json.loads(RESULTS.read_text())
    K = res["roles_final"]["K"]
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    out = {"K": K, "B": a.B}
    for k in sorted({K, 4, 5}):
        r = pd.read_csv(PROC / f"roles_final_K{k}.csv")
        d = ps[["Player_ID", "Season", "MIN"]].merge(r[["Player_ID", "Season", "Arketip", "p_max"]], on=["Player_ID", "Season"])
        d = d.merge(pd.read_csv(PROC / "bio.csv.gz")[["Player_ID", "Season", "position"]], on=["Player_ID", "Season"], how="left")
        seasons = np.array(sorted(d["Season"].unique()))
        roles = sorted(d["Arketip"].unique())

        def stats(x: pd.DataFrame) -> dict:
            tab = x.pivot_table(index="Season", columns="Arketip", values="MIN", aggfunc="sum").reindex(index=seasons, columns=roles).fillna(0)
            sh = tab.div(tab.sum(axis=1), axis=0)
            o = {f"pay_egilim_{rr}": 100 * slope(seasons.astype(float), sh[rr].to_numpy()) for rr in roles}
            cv = [cramers_v(pd.crosstab(g["Arketip"], g["position"])) for _, g in x.dropna(subset=["position"]).groupby("Season")]
            o["cramer_v_egilim"] = slope(seasons.astype(float), np.array(cv))
            amb = x.assign(b=(x["p_max"] < 0.7).astype(float)).groupby("Season")["b"].mean().reindex(seasons).to_numpy()
            o["belirsizlik_egilim"] = 100 * slope(seasons.astype(float), amb)
            return o, sh, cv, amb

        est, sh, cv, amb = stats(d)
        up = d["Player_ID"].unique()
        rows_of = d.groupby("Player_ID").indices
        boots = []
        for _ in range(a.B):
            idx = np.concatenate([rows_of[p] for p in rng.choice(up, len(up))])
            boots.append(stats(d.iloc[idx])[0])
        ci = {kk: [round(float(np.percentile([b[kk] for b in boots], q)), 3) for q in (2.5, 97.5)] for kk in est}

        # Rol geçişleri (ardışık sezonlar, aynı oyuncu)
        nx = d[["Player_ID", "Season", "Arketip"]].copy()
        nx["Season"] -= 1
        tr = d[["Player_ID", "Season", "Arketip"]].merge(nx, on=["Player_ID", "Season"], suffixes=("", "_sonraki"))
        mat = pd.crosstab(tr["Arketip"], tr["Arketip_sonraki"], normalize="index").round(3)
        stay = float((tr["Arketip"] == tr["Arketip_sonraki"]).mean())
        stay_by = tr.assign(s=(tr["Arketip"] == tr["Arketip_sonraki"]).astype(float)).groupby("Arketip")["s"].mean().round(3)

        out[f"K{k}"] = {
            "oyuncu_sezon_N": int(len(d)),
            "pay_sezon": {str(int(s_)): {str(int(rr)): round(float(sh.loc[s_, rr]), 3) for rr in roles} for s_ in seasons},
            "pay_egilim_yp_sezon": {str(int(rr)): {"egim": round(est[f"pay_egilim_{rr}"], 3), "GA95": ci[f"pay_egilim_{rr}"]} for rr in roles},
            "cramer_v_sezon": {str(int(s_)): round(float(v), 3) for s_, v in zip(seasons, cv)},
            "cramer_v_egilim": {"egim": round(est["cramer_v_egilim"], 4), "GA95": [round(x / 1, 4) for x in ci["cramer_v_egilim"]]},
            "belirsizlik_sezon": {str(int(s_)): round(float(v), 3) for s_, v in zip(seasons, amb)},
            "belirsizlik_egilim_yp": {"egim": round(est["belirsizlik_egilim"], 3), "GA95": ci["belirsizlik_egilim"]},
            "gecis_N": int(len(tr)), "ayni_rolde_kalma": round(stay, 3),
            "ayni_rolde_kalma_rol": {str(int(kk)): v for kk, v in stay_by.items()},
            "gecis_matrisi": {str(int(i)): {str(int(j)): float(mat.loc[i, j]) for j in mat.columns} for i in mat.index},
        }
        print(k, {kk: v for kk, v in out[f"K{k}"].items() if kk in ("pay_egilim_yp_sezon", "cramer_v_egilim", "belirsizlik_egilim_yp", "ayni_rolde_kalma")}, flush=True)

    # Rol içi ham değişken eğilimleri (ana K; ≥ 400 dakika; dakika ağırlıklı)
    r = pd.read_csv(PROC / f"roles_final_K{K}.csv")
    raw = raw_features(ps, ("adv", "shot")).assign(Player_ID=ps["Player_ID"], Season=ps["Season"], MIN=ps["MIN"])
    raw = raw[raw["MIN"] >= 400].merge(r[["Player_ID", "Season", "Arketip"]], on=["Player_ID", "Season"])
    raw["AST_pct"] = raw["AST_pct"] ** 2                     # raw_features karekök dönüşümünü geri al
    trend = {}
    for v in RAW:
        lig = raw.groupby("Season").apply(lambda g: np.average(g[v].fillna(g[v].mean()), weights=g["MIN"]), include_groups=False)
        rows_all = raw.groupby("Player_ID").indices
        pall = list(rows_all)
        lb = []
        for _ in range(500):
            rr_ = raw.iloc[np.concatenate([rows_all[p_] for p_ in rng.choice(pall, len(pall))])]
            ll = rr_.groupby("Season").apply(lambda g: np.average(g[v].fillna(g[v].mean()), weights=g["MIN"]), include_groups=False)
            lb.append(slope(ll.index.to_numpy(float), ll.to_numpy()))
        trend[v] = {"lig_2016": round(float(lig.iloc[0]), 3), "lig_son": round(float(lig.iloc[-1]), 3),
                    "lig_egim": round(slope(lig.index.to_numpy(float), lig.to_numpy()), 4),
                    "lig_egim_GA95": [round(float(x), 4) for x in np.percentile(lb, [2.5, 97.5])], "B_ham": 500,
                    "rol": {}}
        for rr, g in raw.groupby("Arketip"):
            m = g.groupby("Season").apply(lambda h: np.average(h[v].fillna(h[v].mean()), weights=h["MIN"]), include_groups=False)
            bs = []
            rows_g = g.groupby("Player_ID").indices
            pl = list(rows_g)
            for _ in range(500):
                gg = g.iloc[np.concatenate([rows_g[p_] for p_ in rng.choice(pl, len(pl))])]
                mm = gg.groupby("Season").apply(lambda h: np.average(h[v].fillna(h[v].mean()), weights=h["MIN"]), include_groups=False)
                bs.append(slope(mm.index.to_numpy(float), mm.to_numpy()))
            trend[v]["rol"][str(int(rr))] = {"ilk": round(float(m.iloc[0]), 3), "son": round(float(m.iloc[-1]), 3),
                                              "egim": round(slope(m.index.to_numpy(float), m.to_numpy()), 4),
                                              "egim_GA95": [round(float(x), 4) for x in np.percentile(bs, [2.5, 97.5])],
                                              "sezon": {str(int(k_)): round(float(x), 3) for k_, x in m.items()}}
        trend[v]["lig_sezon"] = {str(int(k_)): round(float(x), 3) for k_, x in lig.items()}
    out["ham_degisken_egilimi"] = trend
    print(json.dumps(trend, indent=1)[:1500])

    res = json.loads(RESULTS.read_text())
    res["role_trends"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
