"""Makale B, hakem turu 4 (C2): role göre düzeltilmiş PIR40 aynı RAPM düzeyindeki rol farklarını gideriyor mu?
→ results.json["paper_b_values"]["rol_duzeltilmis_kontrol"].

Kariyer düzeyi (≥ 400 dakika, paper_b_values ile aynı örneklem): PIR40, ana rol (nihai K), RAPM (lineup_model'in tüm veri
RAPM'i, rapm.csv). Düzeltilmiş PIR40 = PIR40 − rolün dakika ağırlıklı ortalama PIR40'ı. Raporlanan: düzeltilmiş PIR40'ın
RAPM'e koşullu kısmi η²'si ve en büyük rol farkı (oyuncu bootstrap %95 GA); düzeltilmiş ile düzeltilmemiş PIR40'ın oyuncu ve
dizilim toplamı (ev − deplasman) düzeyinde korelasyonu.
"""
import json
import numpy as np
import pandas as pd
from lineup_model import PROC, RESULTS, SEED, load

rng = np.random.default_rng(SEED)
res = json.loads(RESULTS.read_text())
K = res["roles_final"]["K"]
ps = pd.read_csv(PROC / "player_season.csv.gz")
pg = pd.read_csv(PROC / "player_game.csv.gz").merge(ps[["Player_ID", "Season"]], on=["Player_ID", "Season"])
g = pg.groupby("Player_ID")[["Valuation", "MIN"]].sum()
roles = pd.read_csv(PROC / f"roles_final_K{K}.csv")[["Player_ID", "Season", "Arketip"]]
main = (roles.merge(ps[["Player_ID", "Season", "MIN"]], on=["Player_ID", "Season"]).groupby(["Player_ID", "Arketip"])["MIN"]
        .sum().reset_index().sort_values("MIN").groupby("Player_ID").tail(1).set_index("Player_ID")["Arketip"])
rapm = pd.read_csv(PROC / "rapm.csv").set_index("Player_ID")["RAPM"]
d = pd.DataFrame({"PIR40": g["Valuation"] / g["MIN"] * 40, "MIN": ps.groupby("Player_ID")["MIN"].sum(), "rol": main, "RAPM": rapm}).dropna()
d = d[d["MIN"] >= 400]
rm = d.groupby("rol").apply(lambda x: np.average(x["PIR40"], weights=x["MIN"]), include_groups=False)
d["adj"] = d["PIR40"] - d["rol"].map(rm)
rs = sorted(d["rol"].unique())


def cond(df, col):
    X0 = np.column_stack([np.ones(len(df)), df["RAPM"]])
    D = pd.get_dummies(df["rol"].astype(int)).reindex(columns=rs, fill_value=0).to_numpy(float)[:, 1:]
    X1 = np.column_stack([X0, D])
    rss = lambda X: float(((df[col] - X @ np.linalg.lstsq(X, df[col], rcond=None)[0]) ** 2).sum())
    b = np.linalg.lstsq(X1, df[col], rcond=None)[0][2:]
    diffs = np.concatenate([[0.0], b])
    return (rss(X0) - rss(X1)) / rss(X0), float(diffs.max() - diffs.min())


out = {"oyuncu_N": int(len(d))}
for col in ("PIR40", "adj"):
    pe, rng_ = cond(d, col)
    bs = [cond(d.iloc[rng.choice(len(d), len(d))], col) for _ in range(1000)]
    out[col] = {"kismi_eta2": round(pe, 3), "kismi_eta2_GA95": [round(float(x), 3) for x in np.percentile([b[0] for b in bs], [2.5, 97.5])],
                "en_buyuk_rol_farki": round(rng_, 2), "en_buyuk_rol_farki_GA95": [round(float(x), 2) for x in np.percentile([b[1] for b in bs], [2.5, 97.5])]}
out["oyuncu_korelasyonu"] = round(float(d["PIR40"].corr(d["adj"])), 3)
st = load()
raw, adj = d["PIR40"].to_dict(), d["adj"].to_dict()
mr, ma = float(d["PIR40"].mean()), 0.0
sa = lambda m, dv: np.array([sum(m.get(p, dv) for p in a) - sum(m.get(p, dv) for p in b) for a, b in zip(st["LA"], st["LB"])])
out["dizilim_toplami_korelasyonu"] = round(float(np.corrcoef(sa(raw, mr), sa(adj, ma))[0, 1]), 3)
print(out)
res = json.loads(RESULTS.read_text())
res["paper_b_values"]["rol_duzeltilmis_kontrol"] = out
RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
