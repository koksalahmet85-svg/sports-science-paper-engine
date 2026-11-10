"""Rol (ileri istatistik arketipleri, K = 4) başına değer metrikleri → results.json["role_value"].

Amaç: VAL40'ın rol yanlılığını göstermek — kutu skoru tabanlı değer ile sahadaki etki (On−Off) rol başına
karşılaştırılır. ≥ 400 dakika oynayan oyuncu-sezonlar.

    python manuscript/analysis/role_value_summary.py
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
RESULTS = Path(__file__).with_name("results.json")


def main() -> None:
    roles = pd.read_csv(PROC / "archetypes_v2_advanced.csv")[["Player_ID", "Season", "Arketip"]]
    a = pd.read_csv(PROC / "advanced.csv.gz").merge(roles, on=["Player_ID", "Season"])
    a = a[a["MIN"] >= 400]
    s = a.groupby("Arketip").agg(n=("Player", "size"), VAL40=("VAL40", "mean"), TS=("TS_pct", "mean"),
                                 NetRtg_on=("NetRtg_on", "mean"), OnOff=("OnOff_net", "mean"),
                                 OnOff_sd=("OnOff_net", "std")).round(2)
    between = a.groupby("Arketip")[["VAL40", "OnOff_net"]].mean()
    # rol farkının toplam varyansa oranı (eta²): VAL40 ile On−Off'u rolün ne kadar açıkladığı
    eta = {c: round(float(((a.groupby("Arketip")[c].transform("mean") - a[c].mean()) ** 2).sum()
                          / ((a[c] - a[c].mean()) ** 2).sum()), 3) for c in ["VAL40", "OnOff_net"]}
    out = {"N": int(len(a)), "rol_ozet": s.to_dict(orient="index"), "eta2_rol": eta,
           "VAL40_rol_araligi": round(float(between["VAL40"].max() - between["VAL40"].min()), 2),
           "OnOff_rol_araligi": round(float(between["OnOff_net"].max() - between["OnOff_net"].min()), 2)}
    res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    res["role_value"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(s, "\neta² (rolün açıkladığı varyans):", eta)


if __name__ == "__main__":
    main()
