"""Makale B şekilleri → manuscript_b/figures/ (yalnızca results.json'dan).

Şekil 1: rol başına değer ölçütlerinin ortalaması (oyuncular arası z-skor).
Şekil 2: dizilim toplam değerinin ikinci yarı net rating'ine eğimi (%95 GA), ölçüt başına.
Şekil 3: ILP / en çok süre alan beşli karşıtlıkları (%95 GA).

    python manuscript/analysis/figures_paper_b.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
FIG = HERE.parents[1] / "manuscript_b" / "figures"
R = json.loads((HERE / "results.json").read_text())
KM = R["roles_final"]["K"]
ROLE_NAMES = json.loads((HERE / ("role_names.json" if KM == 5 else f"role_names_K{KM}.json")).read_text())
METRIC = {"PIR40": "PIR per 40 min", "VAL40": "VAL per 40 min", "RAPM": "RAPM"}
SLOPE = {"PIR40_sezon": "PIR40 (first half)", "VAL40_sezon": "VAL40 (first half)", "PIR40_havuz": "PIR40 (all prior data)",
         "VAL40_havuz": "VAL40 (all prior data)", "RAPM": "RAPM (all prior data)", "DAKIKA": "Minutes (first half)"}
RULE = {"yok": "no constraint", "tez": "≥ 1 rim protector", "dengeli": "balanced"}
SEL = {"DAKIKA": "Most-used players", "PIR40_sezon": "ILP on PIR40", "VAL40_sezon": "ILP on VAL40", "RAPM": "ILP on RAPM"}


def forest(ax, labels, est, lo, hi, ref=None):
    y = np.arange(len(labels))[::-1]
    ax.errorbar(est, y, xerr=[np.array(est) - lo, np.array(hi) - est], fmt="o", color="k", capsize=3)
    ax.axvline(0, color="grey", lw=0.8)
    if ref is not None:
        ax.axvspan(*ref, color="C0", alpha=0.12, lw=0)
    ax.set_yticks(y, labels, fontsize=8)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    v = R["paper_b_values"]
    roles = sorted(v["rol_ortalamasi_z"], key=int)
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    w = 0.26
    for i, m in enumerate(METRIC):
        ax.bar(np.arange(len(roles)) + (i - 1) * w, [v["rol_ortalamasi_z"][r][m] for r in roles], w, label=METRIC[m])
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xticks(range(len(roles)), [ROLE_NAMES[r] for r in roles], fontsize=8)
    ax.set_ylabel("Mean z-score across players")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_role_bias.png", dpi=300)

    s = R["ilp_validation"]["amac_fonksiyonu_egimi"]
    keys = list(SLOPE)
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    forest(ax, [SLOPE[k] for k in keys], [s[k]["egim"] for k in keys],
           np.array([s[k]["GA95"][0] for k in keys]), np.array([s[k]["GA95"][1] for k in keys]))
    ax.set_xlabel("Second-half net rating per 1 SD of lineup value\n(points/100 possessions)")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_slopes.png", dpi=300)

    c = R["ilp_validation"]["dogrudan_eslestirilmis_fark"]
    keys = [f"{m}_{r}" for m in SEL if m != "DAKIKA" for r in RULE if f"{m}_{r}" in c]
    labels = [f"{SEL[k.rsplit('_', 1)[0]]}, {RULE[k.rsplit('_', 1)[1]]}" for k in keys]
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    forest(ax, labels, [c[k]["fark"] for k in keys], np.array([c[k]["GA95"][0] for k in keys]),
           np.array([c[k]["GA95"][1] for k in keys]))
    ax.set_xlabel("Optimised five minus coach benchmark\n(net rating, points/100 possessions)")
    fig.tight_layout()
    fig.savefig(FIG / "fig3_ilp.png", dpi=300)
    print("→", sorted(p.name for p in FIG.glob("*.png")))


if __name__ == "__main__":
    main()
