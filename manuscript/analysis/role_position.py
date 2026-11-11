"""Roller × resmî pozisyon (Guard / Forward / Center): pozisyon-ötesi savının sınanması → results.json["role_position"].

Cramér V rol–pozisyon ilişkisinin gücünü, "baskın pozisyon payı" her rolün tek bir pozisyona ne kadar bağlı olduğunu verir.

    python manuscript/analysis/role_position.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
RESULTS = Path(__file__).with_name("results.json")
SETS = {"K4_ileri": "archetypes_v2_advanced.csv", "K5_ileri_boy": "archetypes_v2_advanced_height.csv",
        "K5_tam": "archetypes_v2_full.csv"}


def main() -> None:
    bio = pd.read_csv(PROC / "bio.csv.gz")
    out = {}
    for name, f in SETS.items():
        r = pd.read_csv(PROC / f).merge(bio, on=["Player_ID", "Season"], how="left")
        t = pd.crosstab(r["Arketip"], r["position"])
        v = float(np.sqrt(chi2_contingency(t)[0] / (t.values.sum() * (min(t.shape) - 1))))
        out[name] = {"cramers_v": round(v, 3), "tablo": t.to_dict(orient="index"),
                     "baskin_pozisyon_payi": (t.max(axis=1) / t.sum(axis=1)).round(2).to_dict(),
                     "ortalama_boy": r.groupby("Arketip")["height_cm"].mean().round(1).to_dict()}
        print(name, "Cramér V =", out[name]["cramers_v"], "\n", t)
    res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    res["role_position"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
