"""Ham EuroLeague JSON → analiz tabloları (data/processed/).

Çıktılar:
- player_game.csv.gz   : oyuncu-maç kutu skoru
- player_season.csv.gz : tez filtresi (kadroda ≥10 maç, ≥90 dk) + VAL40 ve öznitelikler (tez EK-2.1/2.2)
- stints_<mod>.csv.gz  : 5'e 5 segmentler; iki mod:
    thesis    — tez EK-2.7 mantığı: sahadaki beşli yalnızca IN/OUT olaylarından kurulur
                (başlangıç beşlileri eklenmez)
    corrected — başlangıç beşlileri kutu skorundaki IsStarter alanından alınır

    python -m engine.data.build_tables
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "euroleague"
OUT = ROOT / "data" / "processed"
QUARTERS = ["FirstQuarter", "SecondQuarter", "ThirdQuarter", "ForthQuarter", "ExtraTime"]
COUNTS = ["Points", "FieldGoalsMade2", "FieldGoalsAttempted2", "FieldGoalsMade3", "FieldGoalsAttempted3",
          "FreeThrowsMade", "FreeThrowsAttempted", "OffensiveRebounds", "DefensiveRebounds", "TotalRebounds",
          "Assistances", "Steals", "Turnovers", "BlocksFavour", "BlocksAgainst", "FoulsCommited",
          "FoulsReceived", "Valuation", "Plusminus"]


def _load(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def _minutes(s) -> float:
    try:
        m, sec = str(s).split(":")
        return int(m) + int(sec) / 60
    except ValueError:
        return 0.0  # "DNP" vb.


def player_game() -> pd.DataFrame:
    rows = []
    for box_path in sorted(RAW.glob("E*/*_box.json.gz")):
        season, game = int(box_path.parent.name[1:]), int(box_path.name[:3])
        for side, team in zip("AB", _load(box_path)["Stats"]):
            for p in team["PlayersStats"]:
                r = {k: p.get(k) or 0 for k in COUNTS}
                r.update(Season=season, Gamecode=game, Side=side, Team=p["Team"].strip(),
                         Player_ID=p["Player_ID"].strip(), Player=p["Player"], IsStarter=int(p["IsStarter"] or 0),
                         MIN=_minutes(p["Minutes"]))
                rows.append(r)
    return pd.DataFrame(rows)


def player_season(pg: pd.DataFrame) -> pd.DataFrame:
    """Tez EK-2.1 ve EK-2.2 ile aynı tanımlar."""
    grp = ["Player_ID", "Season"]
    ps = pg.groupby(grp, as_index=False)[COUNTS[:-2] + ["MIN"]].sum()
    ps["Player"] = pg.groupby(grp)["Player"].first().values
    ps["Team"] = pg.groupby(grp)["Team"].agg(lambda s: s.mode().iat[0]).values
    ps["G_kadro"] = pg.groupby(grp)["Gamecode"].nunique().values
    ps["G"] = pg[pg["MIN"] > 0].groupby(grp)["Gamecode"].nunique().reindex(
        ps.set_index(grp).index).fillna(0).values
    ps = ps[(ps["G_kadro"] >= 10) & (ps["MIN"] >= 90)].copy()

    def oran(a, b):
        return np.where(b > 0, a / b.where(b > 0, 1), 0.0)

    pos = ps["Points"] + ps["TotalRebounds"] + ps["Assistances"] + ps["Steals"] + ps["BlocksFavour"]
    neg = ((ps["FieldGoalsAttempted2"] - ps["FieldGoalsMade2"]) + (ps["FieldGoalsAttempted3"] - ps["FieldGoalsMade3"])
           + (ps["FreeThrowsAttempted"] - ps["FreeThrowsMade"]) + ps["Turnovers"])
    ps["VAL"] = pos - neg
    ps["VAL40"] = ps["VAL"] / ps["MIN"] * 40
    fga = ps["FieldGoalsAttempted2"] + ps["FieldGoalsAttempted3"]
    fgm = ps["FieldGoalsMade2"] + ps["FieldGoalsMade3"]
    ps["FG2_PCT"] = oran(ps["FieldGoalsMade2"], ps["FieldGoalsAttempted2"])
    ps["FG3_PCT"] = oran(ps["FieldGoalsMade3"], ps["FieldGoalsAttempted3"])
    ps["FT_PCT"] = oran(ps["FreeThrowsMade"], ps["FreeThrowsAttempted"])
    ps["eFG"] = oran(fgm + 0.5 * ps["FieldGoalsMade3"], fga)
    ps["TS"] = oran(ps["Points"], 2 * (fga + 0.44 * ps["FreeThrowsAttempted"]))
    ps["USG_proxy"] = (fga + 0.44 * ps["FreeThrowsAttempted"] + ps["Turnovers"]) / ps["MIN"] * 40
    ps["USGxEFG"] = ps["USG_proxy"] * ps["eFG"]
    for k in ["Points", "TotalRebounds", "Assistances", "Steals", "Turnovers", "BlocksFavour"]:
        ps[k + "_40"] = ps[k] / ps["MIN"] * 40
    return ps


def _clock(quarter: int, marker: str) -> float | None:
    """Maç başından geçen dakika; MARKERTIME çeyrekte kalan süredir (mm:ss)."""
    if ":" not in (marker or ""):
        return None
    m, s = marker.strip().split(":")[:2]
    length = 10 if quarter <= 4 else 5
    start = 10 * min(quarter - 1, 4) + 5 * max(quarter - 5, 0)
    return start + length - (int(m) + int(s) / 60)


def _events(pbp: dict) -> list[dict]:
    """Çeyreklere dağılmış olayları sıralı tek listeye çevirir; uzatmalar 5., 6., ... çeyrek."""
    out, ot_index = [], 0
    for qi, key in enumerate(QUARTERS, start=1):
        for e in pbp.get(key) or []:
            if key == "ExtraTime" and e["PLAYTYPE"] == "BP":
                ot_index += 1
            q = qi if key != "ExtraTime" else 4 + max(ot_index, 1)
            out.append({**e, "Q": q})
    return out


# Segment başına her iki takım için sayılan olaylar (FGA/FTA kodları kaçan atıştır; FV = blok yapan, AG = bloklanan)
# Op/Dp: yalnızca oyuncuya yazılmış ribaundlar (takım ribaundu hariç; ribaund yüzdelerinin paydası için)
TALLY = ["2FGM", "2FGA", "3FGM", "3FGA", "FTM", "FTA", "O", "D", "Op", "Dp", "TO", "AS", "ST", "FV", "AG", "CM", "RV"]


def stints(mode: str) -> pd.DataFrame:
    rows = []
    for pbp_path in sorted(RAW.glob("E*/*_pbp.json.gz")):
        season, game = int(pbp_path.parent.name[1:]), int(pbp_path.name[:3])
        box_path = pbp_path.with_name(pbp_path.name.replace("_pbp", "_box"))
        pbp = _load(pbp_path)
        code = {"A": pbp["CodeTeamA"].strip(), "B": pbp["CodeTeamB"].strip()}
        side_of = {v: k for k, v in code.items()}
        court = {"A": set(), "B": set()}
        if mode == "corrected" and box_path.exists():
            for side, team in zip("AB", _load(box_path)["Stats"]):
                court[side] = {p["Player_ID"].strip() for p in team["PlayersStats"] if p["IsStarter"]}
        t0, score, last = 0.0, {"A": 0, "B": 0}, {"A": 0, "B": 0}

        def reset():
            return {s: dict.fromkeys(TALLY, 0) for s in "AB"}

        tally, t_end = reset(), 0.0

        def close(t):
            nonlocal t0, last, tally
            rec = {"Season": season, "Gamecode": game, "t0": t0, "dur": t - t0,
                   "full": len(court["A"]) == 5 and len(court["B"]) == 5}
            for s in "AB":
                rec[f"lineup_{s}"] = "|".join(sorted(court[s]))
                rec[f"team_{s}"] = code[s]
                rec[f"pts_{s}"] = score[s] - last[s]
                c = tally[s]
                fga = c["2FGM"] + c["2FGA"] + c["3FGM"] + c["3FGA"]
                rec[f"poss_{s}"] = fga + 0.44 * (c["FTM"] + c["FTA"]) - c["O"] + c["TO"]
                rec.update({f"n_{k}_{s}": v for k, v in c.items()})
            rows.append(rec)
            t0, last, tally = t, dict(score), reset()

        for e in _events(pbp):
            t = _clock(e["Q"], e["MARKERTIME"] or "")
            for s_ in "AB":
                if e[f"POINTS_{s_}"] is not None:
                    score[s_] = int(e[f"POINTS_{s_}"])
            side = side_of.get((e["CODETEAM"] or "").strip())
            if side and e["PLAYTYPE"] in tally[side]:
                tally[side][e["PLAYTYPE"]] += 1
                if e["PLAYTYPE"] in ("O", "D") and (e["PLAYER_ID"] or "").strip():
                    tally[side][e["PLAYTYPE"] + "p"] += 1
            if t is not None:
                t_end = max(t_end, t)
            if e["PLAYTYPE"] not in ("IN", "OUT") or side is None or t is None:
                continue
            if t - t0 > 0:
                close(t)
            pid = (e["PLAYER_ID"] or "").strip()
            (court[side].add if e["PLAYTYPE"] == "IN" else court[side].discard)(pid)
        if mode == "corrected" and t_end - t0 > 0:  # son değişiklikten maç sonuna kadar olan segment
            close(t_end)
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pg = player_game()
    pg.to_csv(OUT / "player_game.csv.gz", index=False)
    ps = player_season(pg)
    ps.to_csv(OUT / "player_season.csv.gz", index=False)
    print(f"oyuncu-maç: {len(pg)} | maç: {pg.groupby(['Season', 'Gamecode']).ngroups} | oyuncu-sezon: {len(ps)}")
    for mode in ("thesis", "corrected"):
        st = stints(mode)
        st.to_csv(OUT / f"stints_{mode}.csv.gz", index=False)
        full = st[st["full"] & (st["dur"] >= 10 / 60)]
        print(f"{mode}: {len(st)} segment | tam 5'e 5 ve ≥10 sn: {len(full)}")


if __name__ == "__main__":
    main()
