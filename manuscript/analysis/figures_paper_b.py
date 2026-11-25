"""Makale B şekilleri → manuscript_b/figures/ (yalnızca results.json'dan).

Şekil 1: rol başına değer ölçütlerinin ortalaması (oyuncular arası z-skor).
Şekil 2: dizilim toplam değerinin ikinci yarı net rating'ine eğimi (%95 GA), ölçüt başına.
Şekil 3: ILP beşlisi − antrenör beşlisi doğrudan farkları (%95 GA).
Şekil 4: aynı RAPM düzeyinde roller arası PIR40 farkı (EKK ve 2SLS, %95 GA).

    python manuscript/analysis/figures_paper_b.py            # İngilizce → manuscript_b/figures
    python manuscript/analysis/figures_paper_b.py --lang tr  # Türkçe → manuscript_b_tr/figures
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
R = json.loads((HERE / "results.json").read_text())
KM = R["roles_final"]["K"]
ROLE_NAMES = json.loads((HERE / ("role_names.json" if KM == 5 else f"role_names_K{KM}.json")).read_text())
METRIC = {"PIR40": "PIR per 40 min", "VAL40": "VAL per 40 min", "RAPM": "RAPM"}
SLOPE = {"PIR40_sezon": "PIR40 (first half)", "VAL40_sezon": "VAL40 (first half)", "PIR40_havuz": "PIR40 (all prior data)",
         "VAL40_havuz": "VAL40 (all prior data)", "PIR40_rol": "Role-adjusted PIR40 (all prior data)",
         "RAPM": "RAPM (all prior data)", "DAKIKA": "Minutes (first half)"}
RULE = {"yok": "no constraint", "tez": "≥ 1 rim protector", "dengeli": "balanced"}
SEL = {"DAKIKA": "Most-used players", "PIR40_sezon": "ILP on PIR40", "VAL40_sezon": "ILP on VAL40",
       "PIR40_rol": "ILP on role-adjusted PIR40", "RAPM": "ILP on RAPM"}
TR = {
    "PIR per 40 min": "40 dakikada PIR", "VAL per 40 min": "40 dakikada VAL",
    "PIR40 (first half)": "PIR40 (ilk yarı)", "VAL40 (first half)": "VAL40 (ilk yarı)",
    "PIR40 (all prior data)": "PIR40 (tüm önceki veri)", "VAL40 (all prior data)": "VAL40 (tüm önceki veri)",
    "RAPM (all prior data)": "RAPM (tüm önceki veri)", "Role-adjusted PIR40 (all prior data)": "Role göre düzeltilmiş PIR40 (tüm önceki veri)",
    "ILP on role-adjusted PIR40": "Role göre düzeltilmiş PIR40 ile ILP", "Minutes (first half)": "Dakika (ilk yarı)",
    "no constraint": "kısıtsız", "≥ 1 rim protector": "≥ 1 pota koruyucu", "balanced": "dengeli",
    "ILP on PIR40": "PIR40 ile ILP", "ILP on VAL40": "VAL40 ile ILP", "ILP on RAPM": "RAPM ile ILP",
    "Mean z-score across players": "Oyuncular arası ortalama z-skoru",
    "Second-half net rating per 1 SD of lineup value\n(points/100 possessions)": "Dizilim değerinde 1 SS artış başına ikinci yarı net rating\n(100 hücumda sayı)",
    "Optimised five minus coach benchmark\n(net rating, points/100 possessions)": "Optimize beşli − antrenör beşlisi\n(net rating, 100 hücumda sayı)",
    "PIR40 difference from {ref} at equal RAPM\n(points per 40 minutes)": "Aynı RAPM'de {ref} rolüne göre PIR40 farkı\n(40 dakikada puan)",
    "Regression on RAPM": "RAPM'e koşullu regresyon", "Instrumental variables (2SLS)": "Araç değişken (2SLS)",
    "Ball handler": "Top taşıyıcı", "Wing/forward": "Kanat/forvet", "Interior big": "İç uzun", "Rim protector": "Pota koruyucu",
    "Wing": "Kanat", "Stretch forward": "Açılan forvet",
}
LANG = "en"
FIG = HERE.parents[1] / "manuscript_b" / "figures"


def t(s: str) -> str:
    return TR.get(s, s) if LANG == "tr" else s


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
        ax.bar(np.arange(len(roles)) + (i - 1) * w, [v["rol_ortalamasi_z"][r][m] for r in roles], w, label=t(METRIC[m]))
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xticks(range(len(roles)), [t(ROLE_NAMES[r]) for r in roles], fontsize=8)
    ax.set_ylabel(t("Mean z-score across players"))
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_role_bias.png", dpi=300)
    plt.close(fig)

    s = R["ilp_validation"]["amac_fonksiyonu_egimi"]
    keys = list(SLOPE)
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    forest(ax, [t(SLOPE[k]) for k in keys], [s[k]["egim"] for k in keys],
           np.array([s[k]["GA95"][0] for k in keys]), np.array([s[k]["GA95"][1] for k in keys]))
    ax.set_xlabel(t("Second-half net rating per 1 SD of lineup value\n(points/100 possessions)"))
    fig.tight_layout()
    fig.savefig(FIG / "fig2_slopes.png", dpi=300)
    plt.close(fig)

    c = R["ilp_validation"]["dogrudan_eslestirilmis_fark"]
    keys = [f"{m}_{r}" for m in SEL if m != "DAKIKA" for r in RULE if f"{m}_{r}" in c]
    labels = [f"{t(SEL[k.rsplit('_', 1)[0]])}, {t(RULE[k.rsplit('_', 1)[1]])}" for k in keys]
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    forest(ax, labels, [c[k]["fark"] for k in keys], np.array([c[k]["GA95"][0] for k in keys]),
           np.array([c[k]["GA95"][1] for k in keys]))
    ax.set_xlabel(t("Optimised five minus coach benchmark\n(net rating, points/100 possessions)"))
    fig.tight_layout()
    fig.savefig(FIG / "fig3_ilp.png", dpi=300)
    plt.close(fig)

    # Şekil 4: aynı RAPM'de rol farkları — EKK ve 2SLS (çift yarı)
    cv, iv = v["RAPM_kosullu"]["PIR40"], v["olcum_hatasi_denetimi"]["cift"]
    rr = sorted(cv["rol_farki_GA95"], key=int)
    fig, ax = plt.subplots(figsize=(5.8, 2.8))
    y = np.arange(len(rr))[::-1]
    series = ((0.12, cv["rol_farki_RAPM_sabit"], cv["rol_farki_GA95"], "Regression on RAPM", "k"),
              (-0.12, iv["rol_farki"], iv["rol_farki_GA95"], "Instrumental variables (2SLS)", "C3"))
    for off, src, gaci, lab, col in series:
        est = np.array([src[r] for r in rr])
        lo, hi = np.array([gaci[r][0] for r in rr]), np.array([gaci[r][1] for r in rr])
        ax.errorbar(est, y + off, xerr=[est - lo, hi - est], fmt="o", color=col, capsize=3, label=t(lab))
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_yticks(y, [t(ROLE_NAMES[r]) for r in rr], fontsize=8)
    ref = t(ROLE_NAMES["1"]).lower()
    ax.set_xlabel(t("PIR40 difference from {ref} at equal RAPM\n(points per 40 minutes)").format(ref=ref))
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig4_conditional.png", dpi=300)
    plt.close(fig)
    print("→", sorted(p.name for p in FIG.glob("*.png")))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="en", choices=["en", "tr"])
    LANG = ap.parse_args().lang
    if LANG == "tr":
        FIG = HERE.parents[1] / "manuscript_b_tr" / "figures"
    main()
