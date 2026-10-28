"""Semantic Scholar → references.bib + evidence table + açık erişimli PDF'ler.

Hattın ilk halkası: ne paper-qa ne de yazar ajanı, burada toplanmamış bir kaynağa
atıf yapamaz. Böylece "uydurma referans" riski kaynağında kesilir.

    sspe-search "acute:chronic workload ratio injury soccer" --limit 40 --year 2015-
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

API = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "title,year,authors,venue,externalIds,openAccessPdf,citationCount,abstract,citationStyles,publicationTypes"
ROOT = Path(__file__).resolve().parents[2]
BIB = ROOT / "manuscript" / "references.bib"
TABLE = ROOT / "literature" / "evidence_table.csv"
PDFS = ROOT / "literature" / "pdfs"


def _get(url: str, retries: int = 6) -> dict:
    headers = {"User-Agent": "sports-science-paper-engine"}
    if key := os.getenv("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = key
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))  # anahtarsız uç nokta paylaşımlı kotada sık 429 verir
    raise RuntimeError("unreachable")


def search(query: str, limit: int, year: str | None) -> list[dict]:
    params = {"query": query, "limit": min(limit, 100), "fields": FIELDS}
    if year:
        params["year"] = year
    return _get(f"{API}?{urllib.parse.urlencode(params)}").get("data", [])


def _bibkey(p: dict) -> str:
    first = (p.get("authors") or [{"name": "anon"}])[0]["name"].split()[-1]
    word = next((w for w in re.findall(r"[A-Za-z]+", p.get("title", "")) if len(w) > 3), "paper")
    return re.sub(r"[^A-Za-z0-9]", "", f"{first}{p.get('year') or 'nd'}{word}").lower()


def _bibtex(p: dict, key: str) -> str:
    raw = (p.get("citationStyles") or {}).get("bibtex")
    if raw:
        return re.sub(r"^@(\w+)\{[^,]*,", rf"@\1{{{key},", raw.strip(), count=1)
    doi = (p.get("externalIds") or {}).get("DOI", "")
    authors = " and ".join(a["name"] for a in p.get("authors", []))
    return (f"@article{{{key},\n  title = {{{p.get('title')}}},\n  author = {{{authors}}},\n"
            f"  year = {{{p.get('year')}}},\n  journal = {{{p.get('venue')}}},\n  doi = {{{doi}}}\n}}")


def _existing_keys() -> set[str]:
    return set(re.findall(r"@\w+\{([^,]+),", BIB.read_text())) if BIB.exists() else set()


def main() -> None:
    load_dotenv(ROOT / ".env")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--year", help="örn. 2015- veya 2018-2026")
    ap.add_argument("--min-citations", type=int, default=0)
    ap.add_argument("--no-pdf", action="store_true", help="PDF indirme")
    a = ap.parse_args()

    papers = [p for p in search(a.query, a.limit, a.year) if (p.get("citationCount") or 0) >= a.min_citations]
    keys, new_bib, rows = _existing_keys(), [], []
    PDFS.mkdir(parents=True, exist_ok=True)

    for p in papers:
        key = _bibkey(p)
        if key not in keys:
            keys.add(key)
            new_bib.append(_bibtex(p, key))
        pdf_url = (p.get("openAccessPdf") or {}).get("url")
        pdf_path = PDFS / f"{key}.pdf"
        if pdf_url and not a.no_pdf and not pdf_path.exists():
            try:
                urllib.request.urlretrieve(pdf_url, pdf_path)
            except Exception as e:  # yayıncı engelleri sık; tablo yine de kaydedilir
                print(f"  PDF alınamadı [{key}]: {e}")
        rows.append({
            "bibkey": key, "year": p.get("year"), "title": p.get("title"), "venue": p.get("venue"),
            "doi": (p.get("externalIds") or {}).get("DOI"), "citations": p.get("citationCount"),
            "types": ";".join(p.get("publicationTypes") or []), "pdf": pdf_path.name if pdf_path.exists() else "",
            "query": a.query,
        })

    if new_bib:
        with BIB.open("a") as f:
            f.write("\n\n".join(new_bib) + "\n\n")
    write_header = not TABLE.exists()
    with TABLE.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["bibkey"])
        if write_header:
            w.writeheader()
        w.writerows(rows)
    print(f"{len(papers)} makale | {len(new_bib)} yeni .bib kaydı | "
          f"{sum(1 for r in rows if r['pdf'])} PDF → {PDFS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
