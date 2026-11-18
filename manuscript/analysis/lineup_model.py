"""Dizilim modeli: oyuncu RAPM + rol bileşimi etkisi (OPEN_QUESTIONS #2, #4, #22).

Gözlem birimi: 5'e 5 segment (stint). y = 100 hücum başına net sayı farkı (A − B), ağırlık = ortalama hücum sayısı.
1. RAPM: ridge regresyon, sahadaki her oyuncu için +1 (A) / −1 (B); az hücumlu oyuncular tek "yedek" sütununda.
   λ, maç bazında gruplanmış çapraz doğrulamayla seçilir. Sabit terim ev sahibi avantajıdır (A = ev sahibi).
2. Zamansal doğrulama (eğitim 2016–2022, test 2023–2024): sabit / VAL40 toplamı / RAPM / RAPM + rol bileşimi
   modellerinin test segmentlerindeki ağırlıklı R²'si.
3. Rol bileşimi: RAPM artığı üzerinde ridge; öznitelikler rol sayıları ve rol çifti çarpımları (A − B farkı).
   Anlamlılık: rol etiketleri sezon içinde oyuncular arasında karıştırılarak (permütasyon) test R² kazancının
   sıfır dağılımı kurulur — "bileşim, bireysel kalitenin ötesinde bilgi taşıyor mu?"
4. Tüm veriyle nihai RAPM → data/processed/rapm.csv; rol başına RAPM ve VAL40 karşılaştırması.

    python manuscript/analysis/lineup_model.py --roles archetypes_v2_full.csv --B 500
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
RESULTS = Path(__file__).with_name("results.json")
SEED = 20261111
LAMBDAS = [500, 1000, 2000, 4000, 8000]
COMP_ALPHAS = [100, 1000, 5000, 20000, 100000]
POWER_DELTAS = [0.0, 0.5, 1.0, 2.0]   # 0 = birinci tür hata kontrolü
MIN_POSS = 300  # bunun altındaki oyuncular "yedek" sütununda toplanır


def load() -> pd.DataFrame:
    st = pd.read_csv(PROC / "stints_corrected.csv.gz")
    st = st[st["full"]].copy()
    st["poss"] = (st["poss_A"] + st["poss_B"]) / 2
    st = st[st["poss"] >= 1].reset_index(drop=True)
    st["y"] = 100 * (st["pts_A"] - st["pts_B"]) / st["poss"]
    st["game"] = st["Season"] * 1000 + st["Gamecode"]
    st["LA"] = st["lineup_A"].str.split("|")
    st["LB"] = st["lineup_B"].str.split("|")
    return st


def player_matrix(st: pd.DataFrame, cols: dict, seen: set | None = None) -> sparse.csr_matrix:
    """`seen` verilirse (test verisi) eğitimde hiç görülmemiş oyuncular 0 (lig ortalaması) sayılır;
    "yedek" katsayısı yalnızca eğitimde görülüp az hücum oynamış oyunculara uygulanır."""
    r, c, v = [], [], []
    rep = cols["__yedek__"]
    for i, (la, lb) in enumerate(zip(st["LA"], st["LB"])):
        for sign, lu in ((1.0, la), (-1.0, lb)):
            for p in lu:
                if seen is not None and p not in seen:
                    continue
                r.append(i), c.append(cols.get(p, rep)), v.append(sign)
    return sparse.csr_matrix((v, (r, c)), shape=(len(st), len(cols)))


def columns(st: pd.DataFrame) -> dict:
    poss = pd.concat([st[["LA", "poss"]].explode("LA").rename(columns={"LA": "p"}),
                      st[["LB", "poss"]].explode("LB").rename(columns={"LB": "p"})]).groupby("p")["poss"].sum()
    cols = {p: i for i, p in enumerate(poss[poss >= MIN_POSS].index)}
    cols["__yedek__"] = len(cols)
    return cols


def fit_rapm(st, lam, cols=None):
    cols = cols or columns(st)
    m = Ridge(alpha=lam, fit_intercept=True).fit(player_matrix(st, cols), st["y"], sample_weight=st["poss"])
    return m, cols


def wr2(y, pred, w):
    mu = np.average(y, weights=w)
    return 1 - np.sum(w * (y - pred) ** 2) / np.sum(w * (y - mu) ** 2)


def role_features(st: pd.DataFrame, role: dict, k: int) -> np.ndarray:
    """Rol sayıları (0 = rolü olmayan/az süreli) ve rol çifti çarpımları; A − B farkı."""
    pairs = list(combinations_with_replacement(range(1, k + 1), 2))

    def side(lineups, seasons):
        n = np.zeros((len(lineups), k + 1))
        for i, (lu, s) in enumerate(zip(lineups, seasons)):
            for p in lu:
                n[i, role.get((p, s), 0)] += 1
        inter = np.column_stack([n[:, a] * n[:, b] if a != b else n[:, a] * (n[:, a] - 1) / 2 for a, b in pairs])
        return np.hstack([n[:, 1:], inter])

    return side(st["LA"], st["Season"]) - side(st["LB"], st["Season"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roles", default="archetypes_v2_full.csv")
    ap.add_argument("--B", type=int, default=500)
    ap.add_argument("--power", type=int, default=0, help="güç simülasyonu tekrar sayısı (0 = yapma)")
    ap.add_argument("--power-B", type=int, default=100)
    a = ap.parse_args()
    tag = Path(a.roles).stem
    rng = np.random.default_rng(SEED)
    st = load()
    roles = pd.read_csv(PROC / a.roles)
    k = int(roles["Arketip"].max())
    role = dict(zip(zip(roles["Player_ID"], roles["Season"]), roles["Arketip"]))
    tr, te = st[st["Season"] <= 2022].reset_index(drop=True), st[st["Season"] >= 2023].reset_index(drop=True)

    # 1. λ seçimi (eğitim dönemi, maç bazında gruplu 5 kat)
    cols_tr = columns(tr)
    xtr = player_matrix(tr, cols_tr)
    cv = {}
    for lam in LAMBDAS:
        pred = np.zeros(len(tr))
        for f_tr, f_te in GroupKFold(5).split(xtr, groups=tr["game"]):
            m = Ridge(alpha=lam).fit(xtr[f_tr], tr["y"].values[f_tr], sample_weight=tr["poss"].values[f_tr])
            pred[f_te] = m.predict(xtr[f_te])
        cv[lam] = round(float(wr2(tr["y"].values, pred, tr["poss"].values)), 5)
    lam = max(cv, key=cv.get)

    # 2. Zamansal doğrulama
    rapm_tr, _ = fit_rapm(tr, lam, cols_tr)
    seen = set(tr["LA"].explode()) | set(tr["LB"].explode())
    p_rapm_tr, p_rapm_te = rapm_tr.predict(xtr), rapm_tr.predict(player_matrix(te, cols_tr, seen))
    share_seen = float(np.mean([p in seen for lu in pd.concat([te["LA"], te["LB"]]) for p in lu]))
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    v = ps[ps["Season"] <= 2022].groupby("Player_ID").apply(lambda d: np.average(d["VAL40"], weights=d["MIN"]),
                                                            include_groups=False)
    vmean = float(v.mean())

    def valsum(d):
        s = lambda col: np.array([sum(v.get(p, vmean) for p in lu) for lu in d[col]])
        return (s("LA") - s("LB")).reshape(-1, 1)

    val = Ridge(alpha=1e-6).fit(valsum(tr), tr["y"], sample_weight=tr["poss"])
    pg = pd.read_csv(PROC / "player_game.csv.gz")
    pg_tr = pg[pg["Season"] <= 2022].groupby("Player_ID")[["Valuation", "MIN"]].sum()
    pg_tr = pg_tr[pg_tr["MIN"] >= 90]
    pir = pg_tr["Valuation"] / pg_tr["MIN"] * 40
    pmean = float(pir.mean())

    def pirsum(d):
        s_ = lambda col: np.array([sum(pir.get(p, pmean) for p in lu) for lu in d[col]])
        return (s_("LA") - s_("LB")).reshape(-1, 1)

    pirm = Ridge(alpha=1e-6).fit(pirsum(tr), tr["y"], sample_weight=tr["poss"])
    yte, wte = te["y"].values, te["poss"].values
    base = float(np.average(tr["y"], weights=tr["poss"]))

    # 3. Rol bileşimi (RAPM artığı üzerinde) + permütasyon; ceza katsayısı eğitimde maç gruplu CV ile seçilir
    f_tr_obs = role_features(tr, role, k)
    resid = tr["y"].values - p_rapm_tr
    comp_cv = {}
    for al in COMP_ALPHAS:
        pred = np.zeros(len(tr))
        for f_tr, f_te in GroupKFold(5).split(f_tr_obs, groups=tr["game"]):
            mm = Ridge(alpha=al).fit(f_tr_obs[f_tr], resid[f_tr], sample_weight=tr["poss"].values[f_tr])
            pred[f_te] = mm.predict(f_tr_obs[f_te])
        comp_cv[al] = round(float(wr2(resid, pred, tr["poss"].values)), 6)
    comp_alpha = max(comp_cv, key=comp_cv.get)

    def comp_gain(role_map, y_tr=None, y_te=None, p_tr=None, p_te=None, cols_=None, mask=None):
        y_tr = tr["y"].values if y_tr is None else y_tr
        y_te_ = yte if y_te is None else y_te
        p_tr = p_rapm_tr if p_tr is None else p_tr
        p_te = p_rapm_te if p_te is None else p_te
        ftr, fte = role_features(tr, role_map, k), role_features(te, role_map, k)
        if cols_ is not None:
            ftr, fte = ftr[:, cols_], fte[:, cols_]
        m = Ridge(alpha=comp_alpha).fit(ftr, y_tr - p_tr, sample_weight=tr["poss"].values)
        mk = np.ones(len(y_te_), bool) if mask is None else mask
        q = p_te + m.predict(fte)
        comp_gain.last = (q, mk)
        return wr2(y_te_[mk], q[mk], wte[mk]) - wr2(y_te_[mk], p_te[mk], wte[mk]), m

    def permuted():
        sh = roles.assign(Arketip=roles.groupby("Season")["Arketip"].transform(lambda s: rng.permutation(s.values)))
        return dict(zip(zip(sh["Player_ID"], sh["Season"]), sh["Arketip"]))

    gain, comp = comp_gain(role)
    r2_comp = wr2(yte, p_rapm_te, wte) + gain
    comp_te = comp.predict(role_features(te, role, k))
    w_sd = lambda x: float(np.sqrt(np.average((x - np.average(x, weights=wte)) ** 2, weights=wte)))
    pred_sd = {"RAPM": round(w_sd(p_rapm_te), 2), "rol_bilesimi": round(w_sd(comp_te), 2)}
    r2_rapm = wr2(yte, p_rapm_te, wte)
    # Ayrıştırma: yalnızca rol sayıları (ana etkiler) vs sayılar + çiftler (sinerji); çift katkısının maç bootstrap GA'sı
    counts = list(range(k))
    gain_counts, m_counts = comp_gain(role, cols_=counts)
    null_counts = np.array([comp_gain(permuted(), cols_=counts)[0] for _ in range(min(a.B, 500))])
    f_te_all = role_features(te, role, k)
    pc, pf = p_rapm_te + m_counts.predict(f_te_all[:, counts]), p_rapm_te + comp.predict(f_te_all)
    g_idx0 = {g: np.where(te["game"].values == g)[0] for g in te["game"].unique()}
    games0 = np.array(list(g_idx0))
    inc = []
    for _ in range(500):
        ii = np.concatenate([g_idx0[g] for g in rng.choice(games0, len(games0))])
        inc.append(wr2(yte[ii], pf[ii], wte[ii]) - wr2(yte[ii], pc[ii], wte[ii]))
    decomp = {"sayilar_kazanc": round(float(gain_counts), 5), "sayilar_kazanc_GA95": None,
              "sayilar_p": round(float((1 + (null_counts >= gain_counts).sum()) / (1 + len(null_counts))), 4),
              "ciftler_ek_kazanc": round(float(gain - gain_counts), 5),
              "ciftler_ek_GA95": [round(float(x), 5) for x in np.percentile(inc, [2.5, 97.5])]}
    # test maçları yeniden örneklenerek R² farklarının %95 GA'sı
    preds = {"RAPM": p_rapm_te, "VAL40": val.predict(valsum(te)), "PIR40": pirm.predict(pirsum(te))}
    g_idx = {g: np.where(te["game"].values == g)[0] for g in te["game"].unique()}
    games = np.array(list(g_idx))
    boot = {kk: [] for kk in ("RAPM-VAL40", "RAPM-PIR40")}
    for _ in range(500):
        ii = np.concatenate([g_idx[g] for g in rng.choice(games, len(games))])
        r = {kk: wr2(yte[ii], v[ii], wte[ii]) for kk, v in preds.items()}
        boot["RAPM-VAL40"].append(r["RAPM"] - r["VAL40"])
        boot["RAPM-PIR40"].append(r["RAPM"] - r["PIR40"])
    r2_ci = {kk: [round(float(x), 5) for x in np.percentile(v, [2.5, 97.5])] for kk, v in boot.items()}
    null = np.array([comp_gain(permuted())[0] for _ in range(a.B)])
    pd.DataFrame({"kazanc": null}).to_csv(PROC / f"lineup_null_{tag}.csv", index=False)

    # 3a. Sızıntı denetimleri (hakem turu 2, N3):
    #  (i) test sezonlarında roller test verisinden değil, oyuncunun eğitim dönemindeki son rolünden alınır (yoksa 0);
    #  (ii) yalnızca 10 oyuncunun tamamı eğitimde görülmüş test segmentleri.
    last_role = (roles[roles["Season"] <= 2022].sort_values("Season").groupby("Player_ID")["Arketip"].last().to_dict())

    def prior_map(rmap):
        out_ = {kk: v for kk, v in rmap.items() if kk[1] <= 2022}
        last = {}
        for (p_, s_), v in sorted(((kk, v) for kk, v in rmap.items() if kk[1] <= 2022), key=lambda t: t[0][1]):
            last[p_] = v
        for lu, s_ in zip(pd.concat([te["LA"], te["LB"]]), pd.concat([te["Season"], te["Season"]])):
            for p_ in lu:
                if p_ in last:
                    out_[(p_, s_)] = last[p_]
        return out_

    role_prior = prior_map(role)
    all_seen = np.array([all(p_ in seen for p_ in la) and all(p_ in seen for p_ in lb) for la, lb in zip(te["LA"], te["LB"])])
    NB = min(a.B, 500)
    def split_map(rmap):
        """Eğitimde görülen oyunculara test sezonundaki rolleri, yeni oyunculara rol yok (0)."""
        return {kk: v for kk, v in rmap.items() if kk[1] <= 2022 or kk[0] in seen}

    def gain_ci(rmap_, cols_=None, mask=None):
        comp_gain(rmap_, cols_=cols_, mask=mask)
        q, mk = comp_gain.last
        idx_all = np.where(mk)[0]
        gi = {}
        for i_ in idx_all:
            gi.setdefault(te["game"].values[i_], []).append(i_)
        gl = list(gi)
        bs_ = []
        for _ in range(500):
            ii = np.concatenate([gi[gl[j]] for j in rng.choice(len(gl), len(gl))])
            bs_.append(wr2(yte[ii], q[ii], wte[ii]) - wr2(yte[ii], p_rapm_te[ii], wte[ii]))
        return [round(float(x), 5) for x in np.percentile(bs_, [2.5, 97.5])]

    leak = {}
    for name_, rmap_, mask_, mk_perm in (
            ("onceki_rol", role_prior, None, lambda: prior_map(permuted())),
            ("hepsi_gorulmus", role, all_seen, permuted),
            ("yeni_oyuncu_rolsuz", split_map(role), None, lambda: split_map(permuted()))):
        g_c = comp_gain(rmap_, cols_=counts, mask=mask_)[0]
        g_t = comp_gain(rmap_, mask=mask_)[0]
        nc, nt = [], []
        for _ in range(NB):
            pm = mk_perm()
            nc.append(comp_gain(pm, cols_=counts, mask=mask_)[0])
            nt.append(comp_gain(pm, mask=mask_)[0])
        leak[name_] = {"sayilar_kazanc": round(float(g_c), 5),
                       "sayilar_p": round(float((1 + (np.array(nc) >= g_c).sum()) / (1 + NB)), 4),
                       "toplam_kazanc": round(float(g_t), 5),
                       "toplam_p": round(float((1 + (np.array(nt) >= g_t).sum()) / (1 + NB)), 4),
                       "test_segment_payi": round(float(1.0 if mask_ is None else mask_.mean()), 3), "B": NB,
                       "sayilar_kazanc_GA95": gain_ci(rmap_, cols_=counts, mask=mask_)}
        print("sızıntı", name_, leak[name_], flush=True)

    decomp["sayilar_kazanc_GA95"] = gain_ci(role, cols_=counts)
    decomp["toplam_kazanc_GA95"] = gain_ci(role)

    # 3b. Güç simülasyonu: en sık görülen iki farklı rolün birlikteliğine δ puan/100 hücum sinerji eklenir
    power = {}
    if a.power:
        pairs_all = list(combinations_with_replacement(range(1, k + 1), 2))
        def presence(st_, pp):
            c = 0
            for col in ("LA", "LB"):
                for lu, s_ in zip(st_[col], st_["Season"]):
                    r_ = [role.get((p_, s_), 0) for p_ in lu]
                    c += (pp[0] in r_) and (pp[1] in r_)
            return c / (2 * len(st_))
        occ = {pp: presence(tr, pp) for pp in pairs_all if pp[0] != pp[1]}
        target = max(occ, key=occ.get)
        j_ = k + pairs_all.index(target)
        inj_tr, inj_te = role_features(tr, role, k)[:, j_], role_features(te, role, k)[:, j_]
        F_tr, F_te = role_features(tr, role, k), role_features(te, role, k)
        gi_tr = {g: np.where(tr["game"].values == g)[0] for g in tr["game"].unique()}
        g_tr = np.array(list(gi_tr))
        for delta in POWER_DELTAS:
            hits = 0
            for _ in range(a.power):
                ii = np.concatenate([gi_tr[g] for g in rng.choice(g_tr, len(g_tr))])
                y_tr_ = tr["y"].values[ii] + delta * inj_tr[ii]
                y_te_ = yte + delta * inj_te
                w_tr_ = tr["poss"].values[ii]
                m_ = Ridge(alpha=lam).fit(xtr[ii], y_tr_, sample_weight=w_tr_)
                r_tr, p_te_ = y_tr_ - m_.predict(xtr[ii]), m_.predict(player_matrix(te, cols_tr, seen))
                mc = Ridge(alpha=comp_alpha).fit(F_tr[ii][:, counts], r_tr, sample_weight=w_tr_)
                mf = Ridge(alpha=comp_alpha).fit(F_tr[ii], r_tr, sample_weight=w_tr_)
                pc_, pf_ = p_te_ + mc.predict(F_te[:, counts]), p_te_ + mf.predict(F_te)
                incs = []
                for _ in range(a.power_B):
                    jj = np.concatenate([g_idx0[g] for g in rng.choice(games0, len(games0))])
                    incs.append(wr2(y_te_[jj], pf_[jj], wte[jj]) - wr2(y_te_[jj], pc_[jj], wte[jj]))
                hits += np.percentile(incs, 2.5) > 0
            power[str(delta)] = round(hits / a.power, 2)
            print("güç", target, delta, power[str(delta)], flush=True)
        power = {"cift": list(target), "guc": power, "sim": a.power, "B": a.power_B,
                 "olcut": "çift artışının maç-bootstrap GA alt sınırı > 0; eğitim maçları her tekrarda yeniden örneklenir",
                 "cift_dizilim_payi_egitim": round(float(occ[target]), 3), "cift_dizilim_payi_test": round(float(presence(te, target)), 3),
                 "cift_farkli_segment_payi_test": round(float(np.mean(inj_te != 0)), 3)}

    pairs = list(combinations_with_replacement(range(1, k + 1), 2))
    names = [f"n{r}" for r in range(1, k + 1)] + [f"n{x}×n{y}" for x, y in pairs]
    coef = pd.Series(comp.coef_, index=names).round(3)

    # 4. Nihai RAPM (tüm veri)
    full, cols = fit_rapm(st, lam)
    rapm = pd.Series(full.coef_[:-1], index=[p for p in cols if p != "__yedek__"], name="RAPM")
    pd.DataFrame({"Player_ID": rapm.index, "RAPM": rapm.values}).to_csv(PROC / "rapm.csv", index=False)
    car = ps.groupby("Player_ID").apply(lambda d: pd.Series({
        "VAL40": np.average(d["VAL40"], weights=d["MIN"]), "MIN": d["MIN"].sum()}), include_groups=False)
    main_role = (roles[["Player_ID", "Season", "Arketip"]].merge(ps[["Player_ID", "Season", "MIN"]], on=["Player_ID", "Season"])
                 .groupby(["Player_ID", "Arketip"])["MIN"].sum().reset_index()
                 .sort_values("MIN").groupby("Player_ID").tail(1).set_index("Player_ID")["Arketip"])
    j = car.join(rapm, how="inner").join(main_role)

    def eta2(c):
        g = j.groupby("Arketip")[c]
        return float(((g.transform("mean") - j[c].mean()) ** 2).sum() / ((j[c] - j[c].mean()) ** 2).sum())

    out = {
        "roller": a.roles, "K": k, "segment_N": int(len(st)), "egitim_N": int(len(tr)), "test_N": int(len(te)),
        "lambda_cv": cv, "lambda": lam, "yedek_katsayisi": round(float(full.coef_[-1]), 2),
        "testte_egitimde_gorulen_oyuncu_payi": round(share_seen, 3), "ev_sahibi_avantaji": round(float(full.intercept_), 2),
        "rapm_oyuncu_N": int(len(rapm)), "rapm_sd": round(float(rapm.std()), 2),
        "test_R2": {"sabit": round(float(wr2(yte, np.full(len(te), base), wte)), 5),
                    "VAL40_toplami": round(float(wr2(yte, val.predict(valsum(te)), wte)), 5),
                    "PIR40_toplami": round(float(wr2(yte, pirm.predict(pirsum(te)), wte)), 5),
                    "fark_GA95": r2_ci,
                    "RAPM": round(float(r2_rapm), 5), "RAPM_rol_bilesimi": round(float(r2_comp), 5)},
        "rol_bilesimi": {"kazanc": round(float(gain), 5), "B": a.B, "ceza_cv": comp_cv, "ceza": comp_alpha,
                         "terim_N": int(k + len(list(combinations_with_replacement(range(1, k + 1), 2)))),
                         "null_ort": round(float(null.mean()), 5), "null_p95": round(float(np.quantile(null, .95)), 5),
                         "p": round(float((1 + (null >= gain).sum()) / (1 + a.B)), 4),
                         "en_buyuk_katsayilar": coef.reindex(coef.abs().sort_values(ascending=False).index).head(8).to_dict()},
        "guc": power,
        "tahmin_SD_test": pred_sd,
        "ayristirma": decomp,
        "sizinti_denetimi": leak,
        "korelasyon_RAPM_VAL40": round(float(j["RAPM"].corr(j["VAL40"])), 3),
        "eta2_rol": {"RAPM": round(eta2("RAPM"), 3), "VAL40": round(eta2("VAL40"), 3)},
        "rol_ortalamalari": j.groupby("Arketip")[["RAPM", "VAL40"]].mean().round(2).to_dict(orient="index"),
        "en_yuksek_RAPM": (j.join(ps.groupby("Player_ID")["Player"].first()).sort_values("RAPM", ascending=False)
                           .head(15)[["Player", "RAPM", "VAL40"]].round(2).values.tolist()),
    }
    res = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    key = f"lineup_model_K{k}" if tag.startswith("archetypes") else f"lineup_model_{tag}"
    if not power and res.get(key, {}).get("guc"):  # önceki güç simülasyonunu koru
        out["guc"] = res[key]["guc"]
    res[f"lineup_model_K{k}" if tag.startswith("archetypes") else f"lineup_model_{tag}"] = out
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
