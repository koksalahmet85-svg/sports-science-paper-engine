"""Makale A şekilleri → manuscript/figures/ (veriler results.json ve data/processed'dan).

Şekil 1: rol sayısına göre bootstrap kararlılığı (GMM, Ward) ve tezin Ward K = 7 çözümü.
Şekil 2: beş rolün değişken profili (sezon içi z-skor ortalamaları, seçili değişkenler).
Şekil 3: rol bileşiminin test R² kazancı — rol etiketleri karıştırıldığında elde edilen sıfır dağılımı ve gözlenen değer.

    python manuscript/analysis/figures_paper_a.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from archetypes_v2 import PROC, features

HERE = Path(__file__).parent
FIG = HERE.parent / "figures"
R = json.loads((HERE / "results.json").read_text())
ROLE = ["Ball handler", "Interior forward", "Stretch forward", "Rim protector", "Wing"]
SHOW = {"USG_pct": "Usage", "AST_pct": "Assist %", "creator_idx": "Creator index", "3PAr": "3-pt attempt rate",
        "c3_share": "Corner-3 share", "rim_rate": "Rim attempt share", "assisted3_rate": "Assisted 3-pt share",
        "ORB_pct": "Off. rebound %", "BLK_pct": "Block %", "FTr": "Free-throw rate", "height_cm": "Height"}


def fig1() -> None:
    scan, a = R["archetypes_v2_full"]["tarama"], R["paper_a"]
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    for m, lab, mk in (("gmm", "Gaussian mixture", "o"), ("ward", "Ward", "s")):
        ks = sorted(int(k.split("K")[1]) for k in scan if k.startswith(m))
        ax.plot(ks, [scan[f"{m}_K{k}"]["jaccard_ort"] for k in ks], marker=mk, label=lab)
    ax.scatter([7], [a["thesis_ward7_jaccard_mean"]], marker="x", s=60, color="k", zorder=3,
               label="Previous 7-cluster solution")
    ax.axhline(0.75, ls="--", lw=0.8, color="grey")
    ax.axhline(0.5, ls=":", lw=0.8, color="grey")
    ax.set_xticks(range(4, 9))
    ax.set_xlabel("Number of roles")
    ax.set_ylabel("Mean bootstrap Jaccard")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_stability.png", dpi=300)


def fig2() -> None:
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    z = features(ps, False, True, True, True)
    lab = ps[["Player_ID", "Season"]].merge(pd.read_csv(PROC / "archetypes_v2_full.csv"), how="left")["Arketip"].values
    prof = z[list(SHOW)].groupby(lab).mean().rename(columns=SHOW)
    prof.index = [ROLE[int(i) - 1] for i in prof.index]
    fig, ax = plt.subplots(figsize=(7, 3.4))
    im = ax.imshow(prof.values, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(prof.shape[1]), prof.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(prof.shape[0]), prof.index, fontsize=8)
    for i, j in np.ndindex(prof.shape):
        ax.text(j, i, f"{prof.values[i, j]:.1f}", ha="center", va="center", fontsize=6.5)
    fig.colorbar(im, ax=ax, label="Mean within-season z-score", shrink=0.8)
    fig.tight_layout()
    fig.savefig(FIG / "fig2_role_profiles.png", dpi=300)


def fig3() -> None:
    null = pd.read_csv(PROC / "lineup_null_K5.csv")["kazanc"] * 100
    obs = R["lineup_model_K5"]["rol_bilesimi"]["kazanc"] * 100
    fig, ax = plt.subplots(figsize=(5.5, 3.4))
    ax.hist(null, bins=40, color="0.75", edgecolor="white", label="Permuted role labels")
    ax.axvline(obs, color="C3", lw=2, label="Observed role labels")
    ax.set_xlabel("Gain in out-of-time R² over RAPM (percentage points)")
    ax.set_ylabel("Permutations")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_permutation.png", dpi=300)


if __name__ == "__main__":
    FIG.mkdir(exist_ok=True)
    fig1()
    fig2()
    fig3()
    print("→", sorted(p.name for p in FIG.glob("*.png")))
