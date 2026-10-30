"""DOI → references.bib (doi.org content negotiation; Crossref/DataCite kaydı).

Semantic Scholar kısıtlandığında ya da kaynak Consensus/Drive gibi başka bir yoldan
bulunduğunda kullanılır. Kayıt yayıncı meta verisinden gelir; bellekten BibTeX yazılmaz.

    sspe-doi 10.1080/01605682.2022.2118634 10.1287/mnsc.1050.0451
"""

from __future__ import annotations

import argparse
import re
import unicodedata
import urllib.request

from engine.literature.s2_search import BIB, _existing_keys


def fetch(doi: str) -> str:
    req = urllib.request.Request(f"https://doi.org/{doi}", headers={"Accept": "application/x-bibtex"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8").strip()


def rekey(bib: str) -> tuple[str, str]:
    author = re.search(r"author\s*=\s*\{([^,}]+)", bib)
    year = re.search(r"year\s*=\s*\{?(\d{4})", bib)
    title = re.search(r"title\s*=\s*\{([^}]+)", bib)
    first = (author.group(1) if author else "anon").split()[-1]
    word = next((w for w in re.findall(r"[A-Za-z]+", title.group(1) if title else "") if len(w) > 3), "paper")
    first = unicodedata.normalize("NFKD", first).encode("ascii", "ignore").decode()
    key = re.sub(r"[^a-z0-9]", "", f"{first}{year.group(1) if year else 'nd'}{word}".lower())
    return key, re.sub(r"^@(\w+)\{[^,]*,", rf"@\1{{{key},", bib, count=1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dois", nargs="+")
    a = ap.parse_args()
    keys, new = _existing_keys(), []
    for doi in a.dois:
        try:
            key, entry = rekey(fetch(doi))
        except Exception as e:
            print(f"  alınamadı [{doi}]: {e}")
            continue
        if key in keys:
            print(f"  zaten var: {key}")
            continue
        keys.add(key)
        new.append(entry)
        print(f"  + {key}")
    if new:
        with BIB.open("a") as f:
            f.write("\n\n" + "\n\n".join(new) + "\n")
    print(f"{len(new)} yeni kayıt → {BIB.name}")


if __name__ == "__main__":
    main()
