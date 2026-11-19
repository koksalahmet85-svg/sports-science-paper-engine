"""Makale A şekilleri → manuscript/figures/ (veriler results.json ve data/processed'dan).

Şekil 1: rol sayısına göre oyuncu düzeyi bootstrap kararlılığı (GMM tied / diag) ve tezin Ward K = 7 çözümü.
Şekil 2: rollerin değişken profili — her rolün mutlak ortalaması en yüksek iki değişkeninin birleşimi.
Şekil 3: rol bileşiminin test R² kazancı — rol etiketleri karıştırıldığında sıfır dağılımı ve gözlenen değer.
Şekil 4: rol × kayıtlı pozisyon payları.
Şekil 5: rol sayılarının test R² kazancı (%95 GA) — sezona özgü roller ve üç sızıntı denetimi, üç rol çözümü.

    python manuscript/analysis/figures_paper_a.py            # İngilizce → manuscript/figures
    python manuscript/analysis/figures_paper_a.py --lang tr  # Türkçe → manuscript_tr/figures
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
PROC = HERE.parents[1] / "data" / "processed"
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
TR = {
    "3-pt attempt rate": "Üçlük deneme oranı", "Free-throw rate": "Serbest atış oranı", "Usage %": "Kullanım %",
    "Assist %": "Asist %", "Off. rebound %": "Hücum ribaundu %", "Def. rebound %": "Savunma ribaundu %",
    "Steal %": "Top çalma %", "Block %": "Blok %", "Turnover %": "Top kaybı %", "Fouls drawn": "Yaptırılan faul",
    "Fouls committed": "Yapılan faul", "Rim attempt share": "Pota altı deneme payı", "Paint attempt share": "Boyalı alan deneme payı",
    "Mid-range share": "Orta mesafe payı", "Corner-3 share": "Köşe üçlük payı", "Fast-break share": "Hızlı hücum payı",
    "Second-chance share": "İkinci şans payı", "Assists to 3s": "Üçlüğe asist", "Assists to rim": "Pota altına asist",
    "Assists to centres": "Pivota asist", "Assist diversity": "Asist çeşitliliği", "Assisted 2-pt makes": "Asistli ikilik isabet",
    "Assisted 3-pt makes": "Asistli üçlük isabet", "Assists received from guards": "Guardlardan alınan asist",
    "Ball handler": "Top taşıyıcı", "Wing/forward": "Kanat/forvet", "Interior big": "İç uzun", "Rim protector": "Pota koruyucu",
    "Wing": "Kanat", "Stretch forward": "Açılan forvet",
    "Gaussian mixture, tied covariance": "Gauss karışımı, ortak kovaryans",
    "Gaussian mixture, diag covariance": "Gauss karışımı, köşegen kovaryans",
    "Previous 7-cluster Ward solution": "Tezdeki 7 kümeli Ward çözümü", "Number of roles": "Rol sayısı",
    "Mean player-level bootstrap Jaccard": "Ortalama oyuncu düzeyi bootstrap Jaccard",
    "Mean within-season z-score": "Sezon içi ortalama z-skoru", "Permuted role labels": "Karıştırılmış rol etiketleri",
    "Observed role labels": "Gözlenen rol etiketleri",
    "Gain in out-of-time R² over RAPM (percentage points)": "RAPM'e göre örneklem dışı R² kazancı (yüzde puan)",
    "Permutations": "Permütasyon", "Guard": "Guard", "Forward": "Forvet", "Centre": "Pivot",
    "Share of player-seasons": "Oyuncu-sezon payı",
    "Season-specific roles": "Sezona özgü roller", "Training-period roles": "Eğitim dönemi rolleri",
    "New players without role": "Yeni oyuncular rolsüz", "All players seen in training": "Tüm oyuncular eğitimde görülmüş",
    "Gain from role counts in out-of-time R² (percentage points)": "Rol sayılarının örneklem dışı R² kazancı (yüzde puan)",
    "Thesis (7 clusters)": "Tez (7 küme)", "4 roles (main)": "4 rol (ana)", "5 roles": "5 rol",
}
LANG = "en"
FIG = HERE.parent / "figures"


def t(s: str) -> str:
    return TR.get(s, s) if LANG == "tr" else s


def fig1() -> None:
    rf, a = R["roles_final"], R["paper_a"]
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    for cov, mk in (("tied", "o"), ("diag", "s")):
        ks = list(range(4, 9))
        ax.plot(ks, [rf["tarama"][f"{cov}_K{k}"]["jaccard_ort"] for k in ks], marker=mk,
                label=t(f"Gaussian mixture, {cov} covariance"))
    ax.scatter([7], [a["thesis_ward7_jaccard_mean"]], marker="x", s=60, color="k", zorder=3,
               label=t("Previous 7-cluster Ward solution"))
    ax.axhline(0.75, ls="--", lw=0.8, color="grey")
    ax.axhline(0.5, ls=":", lw=0.8, color="grey")
    ax.set_xticks(range(4, 9))
    ax.set_xlabel(t("Number of roles"))
    ax.set_ylabel(t("Mean player-level bootstrap Jaccard"))
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_stability.png", dpi=300)
    plt.close(fig)


def fig2() -> None:
    prof = pd.DataFrame(R["roles_final"]["nihai"][f"K{KM}"]["profil_z"]).T
    prof.index = prof.index.astype(str)
    keep = []
    for r in prof.index:
        for v in prof.loc[r].abs().sort_values(ascending=False).index[:2]:
            if v not in keep:
                keep.append(v)
    p = prof[keep].rename(columns=lambda c: t(LABEL.get(c, c)))
    p.index = [t(ROLE[i]) for i in p.index]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    im = ax.imshow(p.values, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(p.shape[1]), p.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(p.shape[0]), p.index, fontsize=8)
    for i, j in np.ndindex(p.shape):
        ax.text(j, i, f"{p.values[i, j]:.1f}", ha="center", va="center", fontsize=6.5)
    fig.colorbar(im, ax=ax, label=t("Mean within-season z-score"), shrink=0.8)
    fig.tight_layout()
    fig.savefig(FIG / "fig2_role_profiles.png", dpi=300)
    plt.close(fig)


def fig3() -> None:
    null = pd.read_csv(PROC / f"lineup_null_roles_final_K{KM}.csv")["kazanc"] * 100
    obs = R[f"lineup_model_roles_final_K{KM}"]["rol_bilesimi"]["kazanc"] * 100
    fig, ax = plt.subplots(figsize=(5.5, 3.4))
    ax.hist(null, bins=40, color="0.75", edgecolor="white", label=t("Permuted role labels"))
    ax.axvline(obs, color="C3", lw=2, label=t("Observed role labels"))
    ax.set_xlabel(t("Gain in out-of-time R² over RAPM (percentage points)"))
    ax.set_ylabel(t("Permutations"))
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_permutation.png", dpi=300)
    plt.close(fig)


def fig4() -> None:
    pos = R["roles_final"]["nihai"][f"K{KM}"]["pozisyon"]
    roles = sorted(pos, key=int)
    cols = (("Guard", "Guard", "#4C78A8"), ("Forward", "Forward", "#F58518"), ("Center", "Centre", "#54A24B"))
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    left = np.zeros(len(roles))
    y = np.arange(len(roles))[::-1]
    for key, lab, colr in cols:
        sh = np.array([pos[r].get(key, 0) / sum(pos[r].values()) for r in roles])
        ax.barh(y, sh, left=left, color=colr, label=t(lab))
        for yi, l, s in zip(y, left, sh):
            if s >= 0.08:
                ax.text(l + s / 2, yi, f"{100 * s:.0f}%", ha="center", va="center", fontsize=7, color="white")
        left += sh
    ax.set_yticks(y, [t(ROLE[r]) for r in roles], fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_xlabel(t("Share of player-seasons"))
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
    fig.tight_layout()
    fig.savefig(FIG / "fig4_positions.png", dpi=300)
    plt.close(fig)


def fig5() -> None:
    sols = ((f"lineup_model_roles_final_K{KM}", f"{KM} roles (main)"),
            (f"lineup_model_roles_final_K{5 if KM == 4 else 4}", f"{5 if KM == 4 else 4} roles"),
            ("lineup_model_thesis_archetypes", "Thesis (7 clusters)"))
    checks = (("season", "Season-specific roles"), ("onceki_rol", "Training-period roles"),
              ("yeni_oyuncu_rolsuz", "New players without role"), ("hepsi_gorulmus", "All players seen in training"))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    labels, k = [], 0
    for si, (key, slab) in enumerate(sols):
        m = R[key]
        for ci_, (ck, clab) in enumerate(checks):
            if ck == "season":
                est, ci = m["ayristirma"]["sayilar_kazanc"], m["ayristirma"].get("sayilar_kazanc_GA95")
            else:
                d = m.get("sizinti_denetimi", {}).get(ck)
                if not d:
                    continue
                est, ci = d["sayilar_kazanc"], d.get("sayilar_kazanc_GA95")
            yv = -(k + si * 0.8)
            ax.plot(100 * est, yv, "o", color=f"C{ci_}", label=t(clab) if si == 0 else None)
            if ci:
                ax.hlines(yv, 100 * ci[0], 100 * ci[1], color=f"C{ci_}")
            labels.append((yv, f"{t(slab)}: {t(clab)}"))
            k += 1
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_yticks([l[0] for l in labels], [l[1] for l in labels], fontsize=7)
    ax.set_xlabel(t("Gain from role counts in out-of-time R² (percentage points)"))
    fig.tight_layout()
    fig.savefig(FIG / "fig5_leakage.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="en", choices=["en", "tr"])
    LANG = ap.parse_args().lang
    if LANG == "tr":
        FIG = HERE.parents[1] / "manuscript_tr" / "figures"
    FIG.mkdir(parents=True, exist_ok=True)
    for f in (fig1, fig2, fig3, fig4, fig5):
        f()
    print("→", sorted(p.name for p in FIG.glob("*.png")))
