"""Tek giriş noktası: data/processed → manuscript/analysis/results.json (+ şekiller).

Metindeki her sayı bu dosyadan gelir; data-analyst ajanı analizleri buraya ekler.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed" / "dataset.csv"
OUT = Path(__file__).with_name("results.json")


def main() -> None:
    if not DATA.exists():
        OUT.write_text(json.dumps({"status": "no-data"}, indent=2))
        print(f"Veri yok: {DATA.relative_to(ROOT)}")
        return
    import pandas as pd

    df = pd.read_csv(DATA)
    results = {"status": "ok", "n": int(df.shape[0])}
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"→ {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
