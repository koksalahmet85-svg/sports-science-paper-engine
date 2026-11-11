"""EuroLeague oyuncu künyesi: boy, kilo, doğum tarihi, resmî pozisyon (Guard / Forward / Center).

Ham yanıt data/raw/euroleague/<sezon>/people.json.gz, tablo data/processed/bio.csv.gz.
Bir oyuncu sezon içinde takım değiştirdiyse ilk kayıt alınır; eksik boy, oyuncunun diğer sezonlarından doldurulur.

    python -m engine.data.bio
"""

from __future__ import annotations

import gzip
import json

import pandas as pd

from engine.data.euroleague import RAW, ROOT, SEASONS, _get

URL = "https://api-live.euroleague.net/v2/competitions/E/seasons/{season}/people?personType=J&limit=1000"
OUT = ROOT / "data" / "processed"


def main() -> None:
    rows = []
    for season in SEASONS:
        path = RAW / season / "people.json.gz"
        if not path.exists():
            body = _get(URL.format(season=season))
            json.loads(body)
            path.write_bytes(gzip.compress(body))
        for x in json.loads(gzip.decompress(path.read_bytes()))["data"]:
            p = x["person"]
            rows.append({"Player_ID": "P" + p["code"], "Season": int(season[1:]), "height_cm": p.get("height") or None,
                         "weight_kg": p.get("weight") or None, "birth": (p.get("birthDate") or "")[:10],
                         "position": x.get("positionName") or None})
    bio = pd.DataFrame(rows).drop_duplicates(["Player_ID", "Season"])
    for c in ("height_cm", "weight_kg", "position"):
        bio[c] = bio.groupby("Player_ID")[c].transform(lambda s: s.ffill().bfill())
    bio["age"] = bio["Season"] + 0.75 - pd.to_datetime(bio["birth"], errors="coerce").dt.year  # sezon ortası yaklaşık yaş
    OUT.mkdir(parents=True, exist_ok=True)
    bio.to_csv(OUT / "bio.csv.gz", index=False)
    ps = pd.read_csv(OUT / "player_season.csv.gz")[["Player_ID", "Season"]].merge(bio, how="left")
    print(f"künye: {len(bio)} oyuncu-sezon | analiz örnekleminde eksik: boy {ps['height_cm'].isna().sum()}, "
          f"pozisyon {ps['position'].isna().sum()} / {len(ps)}")
    print(ps.groupby("position")["height_cm"].agg(["size", "mean", "std"]).round(1))


if __name__ == "__main__":
    main()
