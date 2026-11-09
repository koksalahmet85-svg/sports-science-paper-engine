"""Şut koordinatları + play-by-play → oyuncu-sezon şut profili (data/processed/shot_profile.csv.gz).

Koordinatlar santimetre, orijin pota; Y sahanın uzunluğu boyunca. Bölgeler (tüm saha içi atış denemeleri içinde pay):
- rim   : ≤ 1,25 m      (EuroLeague bölge A)
- paint : 1,25–3,0 m    (bölge B–C)
- mid   : 3,0 m – üçlük çizgisi (bölge D–G)
- c3    : köşe üçlüğü (Y < 3,0 m), üçlük denemeleri içinde pay
Ayrıca hızlı hücum ve ikinci şans atışlarının payı ve isabetli saha içi atışların asistli payı
(play-by-play'de aynı takımın AS olayı isabetin hemen ardından gelir).

    python -m engine.data.shot_profile
"""

from __future__ import annotations

import gzip
import json
import math
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "euroleague"
OUT = ROOT / "data" / "processed"
FGA = {"2FGM", "2FGA", "2FGAB", "3FGM", "3FGA", "3FGAB"}
QUARTERS = ["FirstQuarter", "SecondQuarter", "ThirdQuarter", "ForthQuarter", "ExtraTime"]


def _load(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def main() -> None:
    acc = defaultdict(lambda: defaultdict(float))
    for f in sorted(RAW.glob("E*/*_pts.json.gz")):
        season = int(f.parent.name[1:])
        for r in _load(f).get("Rows") or []:
            if r["ID_ACTION"] not in FGA:
                continue
            a = acc[(r["ID_PLAYER"].strip(), season)]
            d = math.hypot(r["COORD_X"], r["COORD_Y"]) / 100
            a["fga"] += 1
            if r["ID_ACTION"].startswith("3"):
                a["fg3a"] += 1
                a["c3"] += r["COORD_Y"] < 300
            else:
                a["rim"] += d <= 1.25
                a["paint"] += 1.25 < d <= 3.0
                a["mid"] += d > 3.0
            a["fastbreak"] += r["FASTBREAK"] == "1"
            a["second"] += r["SECOND_CHANCE"] == "1"
    for f in sorted(RAW.glob("E*/*_pbp.json.gz")):
        season = int(f.parent.name[1:])
        pbp = _load(f)
        ev = [e for q in QUARTERS for e in (pbp.get(q) or [])]
        for i, e in enumerate(ev):
            if e["PLAYTYPE"] in ("2FGM", "3FGM"):
                a = acc[((e["PLAYER_ID"] or "").strip(), season)]
                a["fgm"] += 1
                nxt = ev[i + 1] if i + 1 < len(ev) else None
                a["ast_fgm"] += bool(nxt and nxt["PLAYTYPE"] == "AS" and nxt["CODETEAM"] == e["CODETEAM"])
    rows = []
    for (pid, season), a in acc.items():
        fga, fg3a, fg2a = a["fga"], a["fg3a"], a["fga"] - a["fg3a"]
        rows.append({"Player_ID": pid, "Season": season, "shots": fga,
                     "rim_rate": a["rim"] / fga if fga else 0, "paint_rate": a["paint"] / fga if fga else 0,
                     "mid_rate": a["mid"] / fga if fga else 0, "c3_share": a["c3"] / fg3a if fg3a else 0,
                     "fastbreak_rate": a["fastbreak"] / fga if fga else 0,
                     "second_chance_rate": a["second"] / fga if fga else 0,
                     "assisted_rate": a["ast_fgm"] / a["fgm"] if a["fgm"] else 0, "fg2a_shots": fg2a})
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "shot_profile.csv.gz", index=False)
    print(f"oyuncu-sezon: {len(df)} | şut: {int(df['shots'].sum())}")
    print(df[[c for c in df if c.endswith(("rate", "share"))]].describe().loc[["mean", "std"]].round(3))


if __name__ == "__main__":
    main()
