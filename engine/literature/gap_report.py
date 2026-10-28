"""gpt-researcher: bir araştırma sorusu için atıflı literatür + boşluk (gap) raporu.

Retriever'lar .env'de akademik kaynaklara (Semantic Scholar, PubMed Central, arXiv)
kısıtlanır; genel web/blog kaynakları Q1 bir giriş bölümüne girmemeli.

    sspe-gap "Elit basketbolda haftalık yük dalgalanması ile sakatlık ilişkisi"
"""

from __future__ import annotations

import argparse
import asyncio
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "literature" / "gap_reports"

PROMPT_SUFFIX = (
    " Synthesize peer-reviewed evidence only. Structure: (1) what is established, with effect sizes "
    "and sample characteristics; (2) contradictory findings and likely methodological reasons; "
    "(3) explicit research gaps (population, design, measurement, analysis); "
    "(4) 3 testable hypotheses that would fill the most important gap."
)


async def run(rq: str) -> str:
    from gpt_researcher import GPTResearcher

    researcher = GPTResearcher(query=rq + PROMPT_SUFFIX, report_type="research_report")
    await researcher.conduct_research()
    return await researcher.write_report()


def main() -> None:
    load_dotenv(ROOT / ".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("research_question")
    a = ap.parse_args()
    report = asyncio.run(run(a.research_question))
    OUT.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", a.research_question.lower())[:60].strip("-")
    out = OUT / f"{datetime.now():%Y%m%d}-{slug}.md"
    out.write_text(report)
    print(f"→ {out.relative_to(ROOT)}\n"
          "Not: Rapordaki kaynakları `sspe-search` ile references.bib'e almadan metne atıf yapmayın.")


if __name__ == "__main__":
    main()
