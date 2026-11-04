"""Tek giriş noktası: data/processed → manuscript/analysis/results.json (+ şekiller).

Metindeki her sayı bu dosyadan gelir; data-analyst ajanı analizleri buraya ekler.
Diğer analiz betiklerinin (ör. archetype_formulas.py) yazdığı anahtarlar korunur.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed" / "player_season.csv.gz"
OUT = Path(__file__).with_name("results.json")


def main() -> None:
    results = json.loads(OUT.read_text()) if OUT.exists() else {}
    if not DATA.exists():
        results["status"] = "no-data"
        OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"Veri yok: {DATA.relative_to(ROOT)} (önce: python -m engine.data.euroleague && "
              "python -m engine.data.build_tables)")
        return
    import pandas as pd

    ps = pd.read_csv(DATA)
    results.update(status="ok", n=int(len(ps)), n_sezon=int(ps["Season"].nunique()))
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"→ {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
