"""Makale A şekilleri → manuscript/figures/ (veriler results.json ve data/processed'dan).

Şekil 1: rol sayısına göre oyuncu düzeyi bootstrap kararlılığı (GMM tied / diag) ve tezin Ward K = 7 çözümü.
Şekil 2: beş rolün değişken profili — her rolün mutlak ortalaması en yüksek iki değişkeninin birleşimi.
Şekil 3: rol bileşiminin test R² kazancı — rol etiketleri karıştırıldığında sıfır dağılımı ve gözlenen değer.

    python manuscript/analysis/figures_paper_a.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
PROC = HERE.parents[1] / "data" / "processed"
FIG = HERE.parent / "figures"
R = json.loads((HERE / "results.json").read_text())
KM = R["roles_final"]["K"]
ROLE = json.loads((HERE / ("role_names.json" if KM == 5 else f"role_names_K{KM}.json")).read_text())
LABEL = {"3PAr": "3-pt attempt rate", "FTr": "Free-throw rate", "USG_pct": "Usage %", "AST_pct": "Assist %",
         "ORB_pct": "Off. rebound %", "DRB_pct": "Def. rebound %", "STL_pct": "Steal %", "BLK_pct": "Block %",
         "TOV_pct": "Turnover %", "FD_pct": "Fouls drawn", "PF_pct": "Fouls committed", "rim_rate": "Rim attempt share",
         "paint_rate": "Paint attempt share", "mid_rate": "Mid-range share", "c3_share": "Corner-3 share",
         "fastbreak_rate": "Fast-break share", "second_chance_rate": "Second-chance share",
         "ast3_share": "Assists to 3s", "ast_rim_share": "Assists to rim", "ast_to_C_share": "Assists to centres",
         "out_entropy": "Assist diversity", "assisted2_rate": "Assisted 2-pt makes", "assisted3_rate": "Assisted 3-pt makes",
         "fed_by_G_share": "Assists received from guards"}


def fig1() -> None:
    rf, a = R["roles_final"], R["paper_a"]
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    for cov, mk in (("tied", "o"), ("diag", "s")):
        ks = list(range(4, 9))
        ax.plot(ks, [rf["tarama"][f"{cov}_K{k}"]["jaccard_ort"] for k in ks], marker=mk,
                label=f"Gaussian mixture, {cov} covariance")
    ax.scatter([7], [a["thesis_ward7_jaccard_mean"]], marker="x", s=60, color="k", zorder=3,
               label="Previous 7-cluster Ward solution")
    ax.axhline(0.75, ls="--", lw=0.8, color="grey")
    ax.axhline(0.5, ls=":", lw=0.8, color="grey")
    ax.set_xticks(range(4, 9))
    ax.set_xlabel("Number of roles")
    ax.set_ylabel("Mean player-level bootstrap Jaccard")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_stability.png", dpi=300)


def fig2() -> None:
    prof = pd.DataFrame(R["roles_final"]["nihai"][f"K{KM}"]["profil_z"]).T
    prof.index = prof.index.astype(str)
    keep = []
    for r in prof.index:
        for v in prof.loc[r].abs().sort_values(ascending=False).index[:2]:
            if v not in keep:
                keep.append(v)
    p = prof[keep].rename(columns=LABEL)
    p.index = [ROLE[i] for i in p.index]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    im = ax.imshow(p.values, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(p.shape[1]), p.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(p.shape[0]), p.index, fontsize=8)
    for i, j in np.ndindex(p.shape):
        ax.text(j, i, f"{p.values[i, j]:.1f}", ha="center", va="center", fontsize=6.5)
    fig.colorbar(im, ax=ax, label="Mean within-season z-score", shrink=0.8)
    fig.tight_layout()
    fig.savefig(FIG / "fig2_role_profiles.png", dpi=300)


def fig3() -> None:
    null = pd.read_csv(PROC / f"lineup_null_roles_final_K{KM}.csv")["kazanc"] * 100
    obs = R[f"lineup_model_roles_final_K{KM}"]["rol_bilesimi"]["kazanc"] * 100
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
