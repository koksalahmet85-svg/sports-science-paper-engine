"""paper-qa: literature/pdfs içindeki PDF'lere sayfa/kaynak atıflı soru sorar.

Yazar ajanı Bulgular/Tartışma'da bir iddia kuracaksa önce buradan kanıt çeker;
çıktı literature/answers/ altına kaydedilir ve metne yalnızca oradaki atıflar girer.

    sspe-ask "ACWR > 1.5 sakatlık riskini ne kadar artırıyor? Hangi örneklemlerde?"
"""

from __future__ import annotations

import argparse
import asyncio
import os
import pickle
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
PDFS = ROOT / "literature" / "pdfs"
CACHE = ROOT / "literature" / ".pqa_cache" / "docs.pkl"
ANSWERS = ROOT / "literature" / "answers"


def _settings():
    from paperqa import Settings

    s = Settings(
        llm=os.getenv("PQA_LLM", "anthropic/claude-sonnet-5-5"),
        summary_llm=os.getenv("PQA_SUMMARY_LLM", "anthropic/claude-haiku-5-5"),
        embedding=os.getenv("PQA_EMBEDDING", "st-multi-qa-MiniLM-L6-cos-v1"),
        temperature=0.0,
    )
    s.answer.evidence_k = 15
    s.answer.answer_max_sources = 8
    return s


async def _load_docs(settings):
    from paperqa import Docs

    docs = pickle.loads(CACHE.read_bytes()) if CACHE.exists() else Docs()
    known = {d.docname for d in docs.docs.values()}
    for pdf in sorted(PDFS.glob("*.pdf")):
        if pdf.stem in known:
            continue
        print(f"  indeksleniyor: {pdf.name}")
        # docname = bibkey → yanıttaki atıflar doğrudan references.bib anahtarlarına eşlenir
        await docs.aadd(pdf, docname=pdf.stem, settings=settings)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_bytes(pickle.dumps(docs))
    return docs


async def ask(question: str) -> str:
    settings = _settings()
    docs = await _load_docs(settings)
    session = await docs.aquery(question, settings=settings)
    return session.formatted_answer


def main() -> None:
    load_dotenv(ROOT / ".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    a = ap.parse_args()
    if not any(PDFS.glob("*.pdf")):
        raise SystemExit("literature/pdfs boş. Önce: sspe-search \"<sorgu>\"")
    answer = asyncio.run(ask(a.question))
    ANSWERS.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", a.question.lower())[:60].strip("-")
    out = ANSWERS / f"{datetime.now():%Y%m%d-%H%M}-{slug}.md"
    out.write_text(f"# {a.question}\n\n{answer}\n")
    print(answer, f"\n\n→ {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
