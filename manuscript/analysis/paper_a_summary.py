"""Makale A için veri özeti ve önceki 7 kümelik Ward çözümünün oyuncu düzeyi bootstrap kararlılığı → results.json["paper_a"].

    python manuscript/analysis/paper_a_summary.py
"""

import json

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage

from archetypes_v2 import PROC, RESULTS, SEED
from thesis_archetypes import build


def ward(z, k):
    return fcluster(linkage(z, method="ward"), k, criterion="maxclust") - 1


def player_boot_ward(z, players, k, B, rng):
    base = ward(z, k)
    up = np.unique(players)
    rows_of = {p: np.where(players == p)[0] for p in up}
    sc = np.zeros((B, k))
    for b in range(B):
        idx = np.concatenate([rows_of[p] for p in rng.choice(up, len(up))])
        lab = ward(z[idx], k)
        uniq, first = np.unique(idx, return_index=True)
        lb, lo = lab[first], base[uniq]
        sets_b = [set(np.where(lb == d)[0]) for d in range(k)]
        for c in range(k):
            a = set(np.where(lo == c)[0])
            sc[b, c] = max(len(a & s) / len(a | s) for s in sets_b)
    return sc.mean(axis=0)


def main() -> None:
    pg = pd.read_csv(PROC / "player_game.csv.gz")
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    st = pd.read_csv(PROC / "stints_corrected.csv.gz")
    full = st[st["full"] & (st["dur"] >= 10 / 60)]
    poss = (full["poss_A"] + full["poss_B"]) / 2
    f, z = build()
    jac = player_boot_ward(z, f["PID"].to_numpy(), 7, 200, np.random.default_rng(SEED))
    games = pg.groupby("Season")["Gamecode"].nunique()
    out = {"games": int(pg.groupby(["Season", "Gamecode"]).ngroups), "seasons": int(pg["Season"].nunique()),
           "games_per_season_min": int(games.min()), "games_per_season_max": int(games.max()),
           "player_games": int(len(pg)), "player_seasons": int(len(ps)), "players": int(ps["Player_ID"].nunique()),
           "fit_player_seasons": int((ps["MIN"] >= 400).sum()),
           "stints": int(len(full)), "stints_model": int((((st["poss_A"] + st["poss_B"]) / 2 >= 1) & st["full"]).sum()),  # lineup_model.load() ile aynı tanım
           "stint_minutes_covered": round(float(full["dur"].sum() / st["dur"].sum()), 3),
           "shots": int(pd.read_csv(PROC / "shot_profile.csv.gz")["shots"].sum()),
           "assist_edges": int(len(pd.read_csv(PROC / "assist_edges.csv.gz"))),
           "thesis_ward7_jaccard_mean": round(float(np.mean(jac)), 3),
           "thesis_ward7_jaccard_min": round(float(np.min(jac)), 3), "thesis_ward7_B": 200}
    res = json.loads(RESULTS.read_text())
    res["paper_a"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(out)


if __name__ == "__main__":
    main()
