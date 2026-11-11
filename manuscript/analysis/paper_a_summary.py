"""Makale A için veri özeti ve tez çözümünün (Ward, K = 7) bootstrap kararlılığı → results.json["paper_a"].

    python manuscript/analysis/paper_a_summary.py
"""

import json

import numpy as np
import pandas as pd

from archetypes_v2 import PROC, RESULTS, SEED, jaccard_stability
from thesis_archetypes import build


def main() -> None:
    pg = pd.read_csv(PROC / "player_game.csv.gz")
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    st = pd.read_csv(PROC / "stints_corrected.csv.gz")
    full = st[st["full"] & (st["dur"] >= 10 / 60)]
    _, z = build()
    jac = jaccard_stability(z, 7, "ward", 100, np.random.default_rng(SEED))
    out = {"games": int(pg.groupby(["Season", "Gamecode"]).ngroups), "seasons": int(pg["Season"].nunique()),
           "player_games": int(len(pg)), "player_seasons": int(len(ps)), "players": int(ps["Player_ID"].nunique()),
           "fit_player_seasons": int((ps["MIN"] >= 400).sum()),
           "stints": int(len(full)), "stint_minutes_covered": round(float(full["dur"].sum() / st["dur"].sum()), 3),
           "shots": int(pd.read_csv(PROC / "shot_profile.csv.gz")["shots"].sum()),
           "assist_edges": int(len(pd.read_csv(PROC / "assist_edges.csv.gz"))),
           "thesis_ward7_jaccard_mean": round(float(np.mean(jac)), 3),
           "thesis_ward7_jaccard_min": round(float(np.min(jac)), 3)}
    res = json.loads(RESULTS.read_text())
    res["paper_a"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(out)


if __name__ == "__main__":
    main()
