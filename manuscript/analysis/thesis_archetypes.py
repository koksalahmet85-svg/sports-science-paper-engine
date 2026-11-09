"""Tezin arketiplerinin birebir yeniden üretimi (tezin gerçek EK KOD 1 + EK KOD 2 mantığı).

Tez çıktısıyla aynı sonuç: K1–K7 = 456, 74, 237, 192, 514, 196, 345; silhouette = 0,089.
Basılı tez metninden farklı olan ayrıntılar (OPEN_QUESTIONS #16):
- USG maç başınadır (40 dakikaya göre değil),
- 0/0 oranlar 0 değil örneklem ortalamasıyla doldurulur,
- toplulaştırma (Sezon, oyuncu kimliği, oyuncu adı) üzerinden ve bu sırayla yapılır, değerler 4 basamağa yuvarlanır.

    python manuscript/analysis/thesis_archetypes.py  →  data/processed/thesis_archetypes.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
DEG = ["PTS40", "TRB40", "AST40", "STL40", "BLK40", "USG", "FG3%", "FT%", "eFG%"]


def main() -> None:
    p = pd.read_csv(PROC / "player_game.csv.gz").rename(columns={"Player_ID": "PID"})
    agg = p.groupby(["Season", "PID", "Player"]).agg(
        G=("Gamecode", "nunique"), Min=("MIN", "sum"), PTS=("Points", "sum"),
        FG2M=("FieldGoalsMade2", "sum"), FG2A=("FieldGoalsAttempted2", "sum"),
        FG3M=("FieldGoalsMade3", "sum"), FG3A=("FieldGoalsAttempted3", "sum"),
        FTM=("FreeThrowsMade", "sum"), FTA=("FreeThrowsAttempted", "sum"),
        TRB=("TotalRebounds", "sum"), AST=("Assistances", "sum"), STL=("Steals", "sum"),
        TOV=("Turnovers", "sum"), BLK=("BlocksFavour", "sum")).reset_index()
    for c in ["PTS", "TRB", "AST", "STL", "BLK"]:
        agg[c + "40"] = agg[c] / agg["Min"] * 40
    fga = agg["FG2A"] + agg["FG3A"]
    agg["USG"] = (fga + 0.44 * agg["FTA"] + agg["TOV"]) / agg["G"]
    agg["eFG%"] = np.where(fga > 0, (agg["FG2M"] + 1.5 * agg["FG3M"]) / fga.where(fga > 0, 1), np.nan)
    agg["FG3%"] = np.where(agg["FG3A"] > 0, agg["FG3M"] / agg["FG3A"].where(agg["FG3A"] > 0, 1), np.nan)
    agg["FT%"] = np.where(agg["FTA"] > 0, agg["FTM"] / agg["FTA"].where(agg["FTA"] > 0, 1), np.nan)
    f = agg[(agg["G"] >= 10) & (agg["Min"] >= 90)].copy().round(4)
    z = StandardScaler().fit_transform(f[DEG].fillna(f[DEG].mean()))
    f["Arketip"] = fcluster(linkage(z, method="ward", metric="euclidean"), 7, criterion="maxclust")
    print(f"N = {len(f)} | boyutlar {np.bincount(f['Arketip'])[1:].tolist()} | "
          f"silhouette {silhouette_score(z, f['Arketip']):.3f}")
    f.rename(columns={"PID": "Player_ID"})[["Player_ID", "Player", "Season", "Arketip"]].to_csv(
        PROC / "thesis_archetypes.csv", index=False)


if __name__ == "__main__":
    main()
