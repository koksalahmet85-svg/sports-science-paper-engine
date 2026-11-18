"""Makale B: oyuncu değer ölçütlerinin rol yanlılığı → results.json["paper_b_values"].

Ölçütler (oyuncu düzeyi, 2016–2024 kariyer; ≥ 400 dakika):
  PIR40  : EuroLeague resmî Performance Index Rating (kutu skorundaki Valuation), 40 dakikaya
  VAL40  : tezdeki bileşik endeks (faul ve bloklanan şut hariç PIR benzeri), 40 dakikaya
  RAPM   : ridge düzenlileştirilmiş artı-eksi (lineup_model.py, λ çapraz doğrulamayla); duyarlılık için λ = 1000
Rol: oyuncunun en çok dakika oynadığı nihai rol (roles_final.py).
η² (rolün açıkladığı varyans payı), oyuncu düzeyi bootstrap %95 GA; rol ortalamaları (ölçütler arası z-skor).

    python manuscript/analysis/paper_b_values.py --B 1000
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from lineup_model import PROC, RESULTS, SEED, columns, load, player_matrix

MIN_CAREER = 400


def eta2(df: pd.DataFrame, col: str) -> float:
    g = df.groupby("rol")[col].transform("mean")
    return float(((g - df[col].mean()) ** 2).sum() / ((df[col] - df[col].mean()) ** 2).sum())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=1000)
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)
    res = json.loads(RESULTS.read_text())
    K = res["roles_final"]["K"]
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    roles = pd.read_csv(PROC / f"roles_final_K{K}.csv")[["Player_ID", "Season", "Arketip"]]

    st = load()
    cols = columns(st)
    lam_main = res[f"lineup_model_roles_final_K{K}"]["lambda"]
    rapm = {}
    for lam in (lam_main, 1000):
        m = Ridge(alpha=lam).fit(player_matrix(st, cols), st["y"], sample_weight=st["poss"])
        rapm[lam] = pd.Series(m.coef_[:-1], index=[p for p in cols if p != "__yedek__"])

    g = ps.groupby("Player_ID")
    pgv = pd.read_csv(PROC / "player_game.csv.gz").merge(ps[["Player_ID", "Season"]], on=["Player_ID", "Season"])
    pgv = pgv.groupby("Player_ID")[["Valuation", "MIN"]].sum()
    car = pd.DataFrame({"MIN": g["MIN"].sum(), "Player": g["Player"].first(),
                        "PIR40": pgv["Valuation"] / pgv["MIN"] * 40,
                        "VAL40": g["VAL"].sum() / g["MIN"].sum() * 40})
    main_role = (roles.merge(ps[["Player_ID", "Season", "MIN"]], on=["Player_ID", "Season"])
                 .groupby(["Player_ID", "Arketip"])["MIN"].sum().reset_index().sort_values("MIN")
                 .groupby("Player_ID").tail(1).set_index("Player_ID")["Arketip"])
    d = car.assign(rol=main_role, RAPM=rapm[lam_main], RAPM_l1000=rapm[1000]).dropna()
    d = d[d["MIN"] >= MIN_CAREER]
    metrics = ["PIR40", "VAL40", "RAPM", "RAPM_l1000"]

    est = {m: eta2(d, m) for m in metrics}
    boots = {m: [] for m in metrics}
    idx = np.arange(len(d))
    for _ in range(a.B):
        bd = d.iloc[rng.choice(idx, len(idx))]
        for m in metrics:
            boots[m].append(eta2(bd, m))
    z = (d[metrics] - d[metrics].mean()) / d[metrics].std()
    out = {"K": K, "oyuncu_N": int(len(d)), "asgari_dakika": MIN_CAREER, "B": a.B, "lambda_ana": lam_main,
           "eta2": {m: round(est[m], 3) for m in metrics},
           "eta2_GA95": {m: [round(float(x), 3) for x in np.percentile(boots[m], [2.5, 97.5])] for m in metrics},
           "rol_ortalamasi_z": z.groupby(d["rol"]).mean().round(2).to_dict(orient="index"),
           "rol_ortalamasi_ham": d.groupby("rol")[metrics].mean().round(2).to_dict(orient="index"),
           "rol_N": d["rol"].value_counts().sort_index().to_dict(),
           "korelasyon": d[metrics].corr().round(3).to_dict(),
           "rapm_sd": {"ana": round(float(d["RAPM"].std()), 2), "l1000": round(float(d["RAPM_l1000"].std()), 2)}}
    # (a) RAPM'e koşullu rol etkisi: PIR40 ~ RAPM + rol (kısmi η²); aynı RAPM düzeyinde roller arası PIR farkı
    def partial_eta(df, col):
        X0 = np.column_stack([np.ones(len(df)), df["RAPM"]])
        D = pd.get_dummies(df["rol"], drop_first=True).to_numpy(float)
        X1 = np.column_stack([X0, D])
        rss = lambda X: float(((df[col] - X @ np.linalg.lstsq(X, df[col], rcond=None)[0]) ** 2).sum())
        r0, r1 = rss(X0), rss(X1)
        beta = np.linalg.lstsq(X1, df[col], rcond=None)[0]
        return (r0 - r1) / r0, beta

    cond = {}
    roles_sorted = sorted(d["rol"].unique())
    for col in ("PIR40", "VAL40"):
        pe, beta = partial_eta(d, col)
        bs = [partial_eta(d.iloc[rng.choice(idx, len(idx))], col) for _ in range(a.B)]
        bb = np.array([b_[1][2:] for b_ in bs])
        adj = {str(int(roles_sorted[0])): 0.0, **{str(int(r)): round(float(b), 2) for r, b in zip(roles_sorted[1:], beta[2:])}}
        adj_ci = {str(int(r)): [round(float(x), 2) for x in np.percentile(bb[:, i], [2.5, 97.5])]
                  for i, r in enumerate(roles_sorted[1:])}
        cond[col] = {"kismi_eta2": round(pe, 3), "GA95": [round(float(x), 3) for x in np.percentile([b_[0] for b_ in bs], [2.5, 97.5])],
                     "rol_farki_RAPM_sabit": adj, "rol_farki_GA95": adj_ci}
    out["RAPM_kosullu"] = cond

    # (b) Yarı-yarıya güvenirlik (çift / tek maç kodu) ve güvenirliğe göre düzeltilmiş η²
    halves = {}
    pgall = pd.read_csv(PROC / "player_game.csv.gz")
    for h, mask in (("cift", st["Gamecode"] % 2 == 0), ("tek", st["Gamecode"] % 2 == 1)):
        sh = st[mask].reset_index(drop=True)
        ch = columns(sh)
        mh = Ridge(alpha=lam_main).fit(player_matrix(sh, ch), sh["y"], sample_weight=sh["poss"])
        rap = pd.Series(mh.coef_[:-1], index=[p for p in ch if p != "__yedek__"])
        gh = pgall[(pgall["Gamecode"] % 2 == (0 if h == "cift" else 1))].groupby("Player_ID")[["Valuation", "MIN"]].sum()
        halves[h] = pd.DataFrame({"RAPM": rap, "PIR40": gh["Valuation"] / gh["MIN"] * 40, "MIN": gh["MIN"]})
    j2 = halves["cift"].join(halves["tek"], lsuffix="_c", rsuffix="_t", how="inner")
    j2 = j2[(j2["MIN_c"] >= MIN_CAREER / 2) & (j2["MIN_t"] >= MIN_CAREER / 2)]
    rel = {}
    for col in ("PIR40", "RAPM"):
        r = float(j2[f"{col}_c"].corr(j2[f"{col}_t"]))
        rel[col] = {"r_yari": round(r, 3), "spearman_brown": round(2 * r / (1 + r), 3)}
    out["guvenirlik"] = {"oyuncu_N": int(len(j2)), **rel}
    # (b2) Ölçüm hatasına karşı denetim: iki aşamalı EKK — PIR40 (tüm maçlar) ~ rol + RAPM_çift, RAPM_tek araç değişken.
    #      Rol katsayıları "aynı gerçek RAPM düzeyinde" rol farklarıdır; oyuncu bootstrap %95 GA.
    # Sonuç ve araç farklı maç yarılarından: PIR40(çift) ~ rol + RAPM(çift), araç RAPM(tek); ve tersi
    j3 = j2.join(d[["rol"]], how="inner")
    def tsls(df, y, x, z):
        D = pd.get_dummies(df["rol"].astype(int)).reindex(columns=roles_sorted, fill_value=0).to_numpy(float)[:, 1:]
        Z = np.column_stack([np.ones(len(df)), df[z], D])
        xhat = Z @ np.linalg.lstsq(Z, df[x], rcond=None)[0]
        X = np.column_stack([np.ones(len(df)), xhat, D])
        b = np.linalg.lstsq(X, df[y], rcond=None)[0]
        return np.concatenate([b, [b[2:].max() - min(0.0, b[2:].min()) if len(b) > 2 else np.nan]])
    ii3 = np.arange(len(j3))
    iv = {}
    for name_, (y, x, z) in {"cift": ("PIR40_c", "RAPM_c", "RAPM_t"), "tek": ("PIR40_t", "RAPM_t", "RAPM_c")}.items():
        b_iv = tsls(j3, y, x, z)
        bs_iv = np.array([tsls(j3.iloc[rng.choice(ii3, len(ii3))], y, x, z) for _ in range(a.B)])
        q = lambda i: [round(float(v), 2) for v in np.percentile(bs_iv[:, i], [2.5, 97.5])]
        iv[name_] = {"RAPM_egimi": round(float(b_iv[1]), 2), "RAPM_egimi_GA95": q(1),
                     "rol_farki": {str(int(r)): round(float(b), 2) for r, b in zip(roles_sorted[1:], b_iv[2:-1])},
                     "rol_farki_GA95": {str(int(r)): q(2 + i) for i, r in enumerate(roles_sorted[1:])},
                     "en_buyuk_rol_araligi": round(float(b_iv[-1]), 2), "en_buyuk_rol_araligi_GA95": q(len(b_iv) - 1)}
    out["olcum_hatasi_denetimi"] = {"yontem": "2SLS: PIR40(yarı h) ~ rol + RAPM(yarı h), araç RAPM(diğer yarı); h = çift / tek",
                                    "oyuncu_N": int(len(j3)), **iv}

    out["eta2_duzeltilmis"] = {"PIR40": round(est["PIR40"] / rel["PIR40"]["spearman_brown"], 3),
                               "RAPM": round(est["RAPM"] / max(rel["RAPM"]["spearman_brown"], 1e-6), 3)}

    # (c) PIR bileşenlerini içermeyen roller (şut profili + asist ağı + kullanım + üçlük oranı)
    from roles_final import gmm, raw_features, zscore
    fit = (ps["MIN"] >= 400).to_numpy()
    f_alt = raw_features(ps, ("shot", "net")).join(
        ps[["Player_ID", "Season"]].merge(pd.read_csv(PROC / "advanced.csv.gz"), how="left",
                                          on=["Player_ID", "Season"])[["USG_pct", "3PAr"]].set_axis(ps.index))
    z_alt = zscore(f_alt, ps, fit)
    lab_alt = gmm(z_alt[fit].to_numpy(), K, res["roles_final"]["kovaryans"]).predict(z_alt.to_numpy()) + 1
    main_alt = (ps[["Player_ID", "MIN"]].assign(rol=lab_alt).groupby(["Player_ID", "rol"])["MIN"].sum().reset_index()
                .sort_values("MIN").groupby("Player_ID").tail(1).set_index("Player_ID")["rol"])
    d_alt = d.drop(columns="rol").join(main_alt)
    out["pir_bilesensiz_roller"] = {"degiskenler": list(f_alt.columns),
                                    "eta2": {m_: round(eta2(d_alt, m_), 3) for m_ in ("PIR40", "VAL40", "RAPM")}}
    # (c2) Daha katı: yalnızca şut yeri payları + asist ağı (kullanım, hızlı hücum, ikinci şans oranları da çıkarılır)
    f_s = f_alt.drop(columns=["USG_pct", "fastbreak_rate", "second_chance_rate"])
    z_s = zscore(f_s, ps, fit)
    lab_s = gmm(z_s[fit].to_numpy(), K, res["roles_final"]["kovaryans"]).predict(z_s.to_numpy()) + 1
    main_s = (ps[["Player_ID", "MIN"]].assign(rol=lab_s).groupby(["Player_ID", "rol"])["MIN"].sum().reset_index()
              .sort_values("MIN").groupby("Player_ID").tail(1).set_index("Player_ID")["rol"])
    d_s = d.drop(columns="rol").join(main_s)
    out["pir_bilesensiz_roller_kati"] = {"degiskenler": list(f_s.columns),
                                         "eta2": {m_: round(eta2(d_s, m_), 3) for m_ in ("PIR40", "VAL40", "RAPM")}}

    KA = 5 if K == 4 else 4
    ra = pd.read_csv(PROC / f"roles_final_K{KA}.csv")[["Player_ID", "Season", "Arketip"]]
    mr = (ra.merge(ps[["Player_ID", "Season", "MIN"]], on=["Player_ID", "Season"]).groupby(["Player_ID", "Arketip"])["MIN"]
          .sum().reset_index().sort_values("MIN").groupby("Player_ID").tail(1).set_index("Player_ID")["Arketip"])
    da = d.drop(columns="rol").join(mr.rename("rol")).dropna(subset=["rol"])
    pe_a, beta_a = partial_eta(da, "PIR40")
    bs_a = [partial_eta(da.iloc[rng.choice(np.arange(len(da)), len(da))], "PIR40")[0] for _ in range(a.B)]
    adj_a = np.concatenate([[0.0], beta_a[2:]])
    out["K_duyarliligi"] = {"K": KA, "eta2": {m_: round(eta2(da, m_), 3) for m_ in ("PIR40", "VAL40", "RAPM")},
                            "kismi_eta2_PIR40": round(pe_a, 3), "kismi_eta2_PIR40_GA95": [round(float(x), 3) for x in np.percentile(bs_a, [2.5, 97.5])],
                            "rol_araligi_RAPM_sabit_PIR40": round(float(adj_a.max() - adj_a.min()), 2)}
    adj_m = np.array(list(cond["PIR40"]["rol_farki_RAPM_sabit"].values()))
    out["RAPM_kosullu"]["PIR40"]["rol_araligi"] = round(float(adj_m.max() - adj_m.min()), 2)

    res = json.loads(RESULTS.read_text())
    res["paper_b_values"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out.items() if k not in ("korelasyon",)}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
