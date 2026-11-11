"""Asist ağı: play-by-play'de isabetin hemen ardından gelen aynı takım AS olayı = pasör → bitirici kenarı.

Oyuncu-sezon başına rol değişkenleri (data/processed/assist_net.csv.gz):
  creator_idx     = AST / (AST + FGM)                    yaratıcı ↔ bitirici
  ast3_share      = verdiği asistlerin üçlüğe giden payı (kick-out)
  ast_rim_share   = verdiği asistlerin ≤ 3 m şuta giden payı (pick-and-roll / kesme beslemesi)
  ast_to_C_share  = verdiği asistlerin resmî pozisyonu Center olan oyunculara giden payı
  out_entropy     = asist verdiği oyuncuların çeşitliliği (normalize Shannon entropisi)
  assisted2_rate  = isabetli 2 sayılıklarının asistli payı
  assisted3_rate  = isabetli üçlüklerinin asistli payı (hazır şut ↔ top sürerek şut)
  fed_by_G_share  = aldığı asistlerin Guard'lardan gelen payı
Şut mesafesi, Points uç noktasındaki koordinattan (NUM_ANOT = NUMBEROFPLAY) alınır.

    python -m engine.data.assist_network
"""

from __future__ import annotations

import gzip
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "euroleague"
OUT = ROOT / "data" / "processed"
QUARTERS = ["FirstQuarter", "SecondQuarter", "ThirdQuarter", "ForthQuarter", "ExtraTime"]


def _load(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def main() -> None:
    pos = {(r.Player_ID, r.Season): r.position for r in pd.read_csv(OUT / "bio.csv.gz").itertuples()}
    a = defaultdict(Counter)       # sayaçlar
    out_edges = defaultdict(Counter)  # pasör → bitirici
    edges = []
    for f in sorted(RAW.glob("E*/*_pbp.json.gz")):
        season = int(f.parent.name[1:])
        pts = f.with_name(f.name.replace("_pbp", "_pts"))
        dist = {r["NUM_ANOT"]: math.hypot(r["COORD_X"], r["COORD_Y"]) / 100
                for r in (_load(pts).get("Rows") or [])} if pts.exists() else {}
        pbp = _load(f)
        ev = [e for q in QUARTERS for e in (pbp.get(q) or [])]
        for i, e in enumerate(ev):
            if e["PLAYTYPE"] not in ("2FGM", "3FGM"):
                continue
            scorer = ((e["PLAYER_ID"] or "").strip(), season)
            three = e["PLAYTYPE"] == "3FGM"
            a[scorer]["fgm3" if three else "fgm2"] += 1
            nxt = ev[i + 1] if i + 1 < len(ev) else None
            if not (nxt and nxt["PLAYTYPE"] == "AS" and nxt["CODETEAM"] == e["CODETEAM"]):
                continue
            passer = ((nxt["PLAYER_ID"] or "").strip(), season)
            a[scorer]["ast_fgm3" if three else "ast_fgm2"] += 1
            a[scorer]["fed"] += 1
            a[scorer]["fed_by_G"] += pos.get(passer) == "Guard"
            a[passer]["ast"] += 1
            a[passer]["ast3"] += three
            a[passer]["ast_rim"] += (not three) and dist.get(e["NUMBEROFPLAY"], 99) <= 3.0
            a[passer]["ast_to_C"] += pos.get(scorer) == "Center"
            out_edges[passer][scorer[0]] += 1
            edges.append((season, passer[0], scorer[0], int(three)))

    def share(n, d):
        return n / d if d else 0.0

    rows = []
    for (pid, season), c in a.items():
        fgm = c["fgm2"] + c["fgm3"]
        w = list(out_edges[(pid, season)].values())
        tot = sum(w)
        ent = -sum(x / tot * math.log(x / tot) for x in w) / math.log(len(w)) if len(w) > 1 else 0.0
        rows.append({"Player_ID": pid, "Season": season, "ast_pbp": c["ast"],
                     "creator_idx": share(c["ast"], c["ast"] + fgm),
                     "ast3_share": share(c["ast3"], c["ast"]), "ast_rim_share": share(c["ast_rim"], c["ast"]),
                     "ast_to_C_share": share(c["ast_to_C"], c["ast"]), "out_entropy": ent,
                     "assisted2_rate": share(c["ast_fgm2"], c["fgm2"]),
                     "assisted3_rate": share(c["ast_fgm3"], c["fgm3"]),
                     "fed_by_G_share": share(c["fed_by_G"], c["fed"])})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "assist_net.csv.gz", index=False)
    pd.DataFrame(edges, columns=["Season", "passer", "scorer", "three"]).to_csv(OUT / "assist_edges.csv.gz", index=False)
    print(f"oyuncu-sezon: {len(df)} | asist kenarı: {len(edges)}")
    print(df.drop(columns=["Player_ID", "Season", "ast_pbp"]).describe().loc[["mean", "std"]].round(3).to_string())


if __name__ == "__main__":
    main()
