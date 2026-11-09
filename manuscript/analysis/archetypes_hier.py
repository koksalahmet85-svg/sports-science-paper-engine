"""İki düzeyli rol yapısı: 4 ana rol (archetypes_v2, temel değişkenler) → 6 alt rol.

Alt bölünmeler yalnızca iç içe kararlılık taramasında (archetypes_v2.py --nested --features extended)
öne çıkan iki ana rolde yapılır; şut profili değişkenleriyle GMM K = 2:
- Rol 3 (Çok Yönlü Forvet) → İç Saha Forveti / Stretch Forvet       (bootstrap Jaccard ≈ 0,77: kararlı)
- Rol 4 (Oyun Yöneticisi)  → Organizatör Oyun Kurucu / Yaratıcı Skorer (≈ 0,70: sınırda, keşifsel)
Alt rol etiketleri profil üzerinden atanır (kullanım oranı ve köşe üçlüğü payı), küme numarasına göre değil.

    python manuscript/analysis/archetypes_hier.py  →  data/processed/archetypes_hier.csv
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

from archetypes_v2 import PROC, RESULTS, cluster, features

MACRO = {1: "Boyalı Alan Koruyucusu", 2: "Kenar Şutörü", 3: "Çok Yönlü Forvet", 4: "Oyun Yöneticisi"}
FIT_MIN = 400


def split(z: pd.DataFrame, fit: np.ndarray, high: str, low: str, key: str) -> np.ndarray:
    """GMM K=2; `key` değişkeninde yüksek ortalamalı alt küme `high` adını alır. Kalanlar en yakın merkeze."""
    lab = cluster(z[fit].to_numpy(), 2, "gmm")
    cent = np.array([z[fit].to_numpy()[lab == c].mean(axis=0) for c in range(2)])
    allab = ((z.to_numpy()[:, None, :] - cent[None]) ** 2).sum(-1).argmin(1)
    allab[fit] = lab
    hi = int(np.argmax(cent[:, list(z.columns).index(key)]))
    return np.where(allab == hi, high, low)


def main() -> None:
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    z = features(ps, extended=True)
    macro = ps[["Player_ID", "Season"]].merge(pd.read_csv(PROC / "archetypes_v2.csv"), how="left",
                                              on=["Player_ID", "Season"])["Arketip"].to_numpy()
    micro = pd.Series(pd.Series(macro).map(MACRO).values, index=ps.index, dtype=object)
    for m, (high, low, key) in {3: ("İç Saha Forveti", "Stretch Forvet", "USG_proxy"),
                                4: ("Yaratıcı Skorer", "Organizatör Oyun Kurucu", "USG_proxy")}.items():
        idx = np.where(macro == m)[0]
        fit = (ps["MIN"].to_numpy()[idx] >= FIT_MIN)
        micro.iloc[idx] = split(z.iloc[idx], fit, high, low, key)
    out = ps[["Player_ID", "Player", "Season", "Team", "MIN", "VAL40"]].assign(
        ana_rol=pd.Series(macro).map(MACRO).values, alt_rol=micro.values)
    out.to_csv(PROC / "archetypes_hier.csv", index=False)
    summary = out.groupby(["ana_rol", "alt_rol"]).agg(n=("Player_ID", "size"), VAL40=("VAL40", "mean")).round(2)
    print(summary)
    res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    res["archetypes_hier"] = {f"{a} / {b}": v for (a, b), v in summary.to_dict(orient="index").items()}
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
