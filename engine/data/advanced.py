"""İleri istatistikler: oyuncu sahadayken GERÇEK takım/rakip paydalarıyla (data/processed/advanced.csv.gz).

Basketball-Reference paydaları takımın sezon toplamından tahmin eder; burada her oyuncu için play-by-play'den
yeniden kurulan beşli segmentlerde sahada olduğu anların takım ve rakip toplamları kullanılır.
Pay (oyuncu) değerleri kutu skorundan, paydalar segmentlerden gelir.

Rol / pay metrikleri (kümelemeye uygun):
  USG%  = (FGA + 0,44·FTA + TOV) / sahadaki takımın (FGA + 0,44·FTA + TOV)
  AST%  = AST / (sahadaki takım FGM − oyuncunun FGM)
  ORB%  = ORB / (takım oyuncu-ORB + rakip oyuncu-DRB)      DRB% simetrik
  STL%  = STL / rakip hücum sayısı                          BLK% = BLK / rakip 2 sayılık denemesi
  TOV%  = TOV / (FGA + 0,44·FTA + TOV)                      3PAr = 3PA / FGA,  FTr = FTA / FGA
  FD%   = kazanılan faul / takım hücumu                     PF%  = yapılan faul / rakip hücumu
Verimlilik / etki metrikleri (kümelemeye GİRMEZ; arketip içi değer için):
  TS%, sahadayken ORtg/DRtg/NetRtg (100 hücum başına), On−Off net rating

    python -m engine.data.advanced
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
CODES = ["2FGM", "2FGA", "3FGM", "3FGA", "FTM", "FTA", "Op", "Dp", "TO"]


def on_court(st: pd.DataFrame) -> pd.DataFrame:
    """Her (oyuncu, sezon) için sahadayken takım (tm_) ve rakip (op_) toplamları."""
    parts = []
    for us, them in (("A", "B"), ("B", "A")):
        cols = {"Season": st["Season"], "team": st[f"team_{us}"], "lineup": st[f"lineup_{us}"], "dur": st["dur"],
                "tm_pts": st[f"pts_{us}"], "op_pts": st[f"pts_{them}"],
                "tm_poss": st[f"poss_{us}"], "op_poss": st[f"poss_{them}"]}
        cols.update({f"tm_{c}": st[f"n_{c}_{us}"] for c in CODES})
        cols.update({f"op_{c}": st[f"n_{c}_{them}"] for c in CODES})
        parts.append(pd.DataFrame(cols))
    seg = pd.concat(parts, ignore_index=True)
    team_tot = seg.groupby(["Season", "team"]).sum(numeric_only=True)
    seg["Player_ID"] = seg["lineup"].str.split("|")
    seg = seg.explode("Player_ID")
    on = seg.groupby(["Player_ID", "Season", "team"]).sum(numeric_only=True)
    off = team_tot.reindex(on.index.droplevel("Player_ID")).set_axis(on.index) - on
    on = on.groupby(level=["Player_ID", "Season"]).sum()
    off = off.groupby(level=["Player_ID", "Season"]).sum().add_prefix("off_")
    return on.join(off).reset_index()


def main() -> None:
    st = pd.read_csv(PROC / "stints_corrected.csv.gz")
    st = st[st["full"] & (st["dur"] > 0)]
    ps = pd.read_csv(PROC / "player_season.csv.gz")
    a = ps.merge(on_court(st), how="left", on=["Player_ID", "Season"])

    def safe(num, den):
        return np.where(den > 0, num / den.where(den > 0, 1), np.nan)

    fga = a["FieldGoalsAttempted2"] + a["FieldGoalsAttempted3"]
    fgm = a["FieldGoalsMade2"] + a["FieldGoalsMade3"]
    tm_fga = a["tm_2FGM"] + a["tm_2FGA"] + a["tm_3FGM"] + a["tm_3FGA"]
    tm_fta = a["tm_FTM"] + a["tm_FTA"]
    tm_fgm = a["tm_2FGM"] + a["tm_3FGM"]
    plays = fga + 0.44 * a["FreeThrowsAttempted"] + a["Turnovers"]
    out = a[["Player_ID", "Player", "Season", "Team", "MIN", "VAL40"]].copy()
    out["on_court_min"] = a["dur"]
    # rol / pay
    out["USG_pct"] = safe(plays, tm_fga + 0.44 * tm_fta + a["tm_TO"])
    out["AST_pct"] = safe(a["Assistances"], tm_fgm - fgm)
    out["ORB_pct"] = safe(a["OffensiveRebounds"], a["tm_Op"] + a["op_Dp"])
    out["DRB_pct"] = safe(a["DefensiveRebounds"], a["tm_Dp"] + a["op_Op"])
    out["STL_pct"] = safe(a["Steals"], a["op_poss"])
    out["BLK_pct"] = safe(a["BlocksFavour"], a["op_2FGM"] + a["op_2FGA"])
    out["TOV_pct"] = safe(a["Turnovers"], plays)
    out["3PAr"] = safe(a["FieldGoalsAttempted3"], fga)
    out["FTr"] = safe(a["FreeThrowsAttempted"], fga)
    out["FD_pct"] = safe(a["FoulsReceived"], a["tm_poss"])
    out["PF_pct"] = safe(a["FoulsCommited"], a["op_poss"])
    # verimlilik / etki
    out["TS_pct"] = safe(a["Points"], 2 * (fga + 0.44 * a["FreeThrowsAttempted"]))
    out["ORtg_on"] = safe(a["tm_pts"], a["tm_poss"]) * 100
    out["DRtg_on"] = safe(a["op_pts"], a["op_poss"]) * 100
    out["NetRtg_on"] = out["ORtg_on"] - out["DRtg_on"]
    net_off = (safe(a["off_tm_pts"], a["off_tm_poss"]) - safe(a["off_op_pts"], a["off_op_poss"])) * 100
    out["OnOff_net"] = out["NetRtg_on"] - net_off
    # Dört faktör (Oliver): oyuncu sahadayken takımın hücum (O_) ve savunma (D_) faktörleri, sahada − kenarda farkı
    def four(pre, us, them):
        g = lambda c: a[f"{pre}{c}"]
        fga_ = g(f"{us}_2FGM") + g(f"{us}_2FGA") + g(f"{us}_3FGM") + g(f"{us}_3FGA")
        return {"eFG": safe(g(f"{us}_2FGM") + 1.5 * g(f"{us}_3FGM"), fga_),
                "TOV": safe(g(f"{us}_TO"), g(f"{us}_poss")),
                "ORB": safe(g(f"{us}_Op"), g(f"{us}_Op") + g(f"{them}_Dp")),
                "FTr": safe(g(f"{us}_FTM") + g(f"{us}_FTA"), fga_)}

    for side, us, them in (("O", "tm", "op"), ("D", "op", "tm")):
        on, off = four("", us, them), four("off_", us, them)
        for k in on:
            out[f"FF_{side}_{k}_on"] = on[k]
            out[f"FF_{side}_{k}_diff"] = on[k] - off[k]
    out.to_csv(PROC / "advanced.csv.gz", index=False)
    show = ["USG_pct", "AST_pct", "ORB_pct", "DRB_pct", "STL_pct", "BLK_pct", "TOV_pct", "3PAr", "FTr", "TS_pct",
            "NetRtg_on", "OnOff_net"]
    print(f"oyuncu-sezon: {len(out)} | sahada dakika eşleşmesi (segment/kutu): "
          f"{(out['on_court_min'] / out['MIN']).median():.3f}")
    print(out[show].describe().loc[["mean", "50%", "std"]].round(3).to_string())


if __name__ == "__main__":
    main()
