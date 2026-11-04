"""EuroLeague resmî API'sinden ham veri: maç listesi, kutu skoru, play-by-play.

Tezle aynı kapsam: E2016–E2024 (9 sezon, 2016-17 → 2024-25). Her maç için yanıt
olduğu gibi data/raw/euroleague/<sezon>/ altına gzip'li JSON olarak yazılır; inen
dosyalar bir daha indirilmez, yani betik kesilirse kaldığı yerden devam eder.

    python -m engine.data.euroleague                 # tüm sezonlar
    python -m engine.data.euroleague --seasons E2023 # tek sezon
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "euroleague"
SEASONS = [f"E{y}" for y in range(2016, 2025)]
RESULTS = "https://api-live.euroleague.net/v1/results?seasonCode={season}"
ENDPOINTS = {
    "box": "https://live.euroleague.net/api/Boxscore?gamecode={game}&seasoncode={season}",
    "pbp": "https://live.euroleague.net/api/PlaybyPlay?gamecode={game}&seasoncode={season}",
}


def _get(url: str, retries: int = 5) -> bytes:
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "sports-science-paper-engine"}), timeout=60) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError("unreachable")


def games(season: str) -> list[dict]:
    """Oynanmış maçlar: gamenumber, tur, tarih, takımlar, skor."""
    xml = _get(RESULTS.format(season=season)).decode("utf-8")
    out = []
    for block in re.findall(r"<game>(.*?)</game>", xml, flags=re.S):
        g = dict(re.findall(r"<(\w+)>([^<]*)</\1>", block))
        if g.get("played") == "true":
            out.append(g)
    return out


def _fetch_one(season: str, game: str, kind: str, path: Path, delay: float) -> str | None:
    try:
        body = _get(ENDPOINTS[kind].format(game=game, season=season))
        json.loads(body)  # boş/HTML yanıtı kaydetme
    except Exception as e:
        return f"{season}/{game}/{kind}: {e}"
    path.write_bytes(gzip.compress(body))
    time.sleep(delay)
    return None


def fetch_season(season: str, delay: float, workers: int) -> tuple[int, list[str]]:
    folder = RAW / season
    folder.mkdir(parents=True, exist_ok=True)
    gl = games(season)
    (folder / "games.json").write_text(json.dumps(gl, ensure_ascii=False, indent=1))
    todo = [(g["gamenumber"], kind, folder / f"{int(g['gamenumber']):03d}_{kind}.json.gz")
            for g in gl for kind in ENDPOINTS]
    todo = [t for t in todo if not t[2].exists()]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        failed = [r for r in pool.map(lambda t: _fetch_one(season, *t, delay), todo) if r]
    return len(gl), failed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seasons", nargs="+", default=SEASONS)
    ap.add_argument("--delay", type=float, default=0.2, help="her bağlantıda istekler arası bekleme (sn)")
    ap.add_argument("--workers", type=int, default=4, help="eşzamanlı bağlantı sayısı")
    a = ap.parse_args()
    all_failed = []
    for s in a.seasons:
        n, failed = fetch_season(s, a.delay, a.workers)
        all_failed += failed
        print(f"{s}: {n} maç, {len(failed)} hata", flush=True)
    if all_failed:
        (RAW / "failed.txt").write_text("\n".join(all_failed))
        print(f"Hatalar → {(RAW / 'failed.txt').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
