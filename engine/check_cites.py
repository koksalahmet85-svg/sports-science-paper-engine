"""Metindeki her atıf anahtarı references.bib'de olmalı (uydurma kaynak kalkanı)."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSSREF = ("fig-", "tbl-", "sec-", "eq-", "lst-")


def main() -> int:
    bib = set(re.findall(r"@\w+\{([^,\s]+),", (ROOT / "manuscript" / "references.bib").read_text()))
    missing = {}
    for qmd in (ROOT / "manuscript").rglob("*.qmd"):
        text = re.sub(r"<!--.*?-->", "", qmd.read_text(), flags=re.S)
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for key in re.findall(r"(?<![\w.])-?@([A-Za-z0-9_][\w:.#$%&+?<>~/-]*\w)", text):
            if key not in bib and not key.startswith(CROSSREF):
                missing.setdefault(key, set()).add(qmd.relative_to(ROOT).as_posix())
    for key, files in sorted(missing.items()):
        print(f"  [@{key}] references.bib'de yok → {', '.join(sorted(files))}")
    print("Atıf denetimi: OK" if not missing else f"{len(missing)} doğrulanmamış atıf.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
