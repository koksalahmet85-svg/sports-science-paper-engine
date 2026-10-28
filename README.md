# sports-science-paper-engine

Claude Code tabanlı, **kaynağa dayalı** spor bilimleri makale üretim hattı.
Temel ilke: model hiçbir zaman toplanmamış bir kaynağa atıf yapamaz ve elle sayı yazamaz.

```
RQ ─► literature-scout ──► methodologist ──► data-analyst ──► yazım ──► /paper-loop ──► Quarto
       │ sspe-search  (Semantic Scholar → references.bib + açık erişim PDF)      (q1-reviewer ⇄ ajanlar,
       │ sspe-gap     (gpt-researcher → gap raporu)                               en fazla 4 tur)
       │ sspe-ask     (paper-qa → sayfa atıflı yanıt)
       └─ make check-cites: metindeki her [@key] references.bib'de mi?
```

## Bileşen kararları

| Repo | Durum | Neden |
|---|---|---|
| `Future-House/paper-qa` (eski `whitead/paper-qa`) | **Çekirdek** (`pip`, extra: `qa`) | Halüsinasyona karşı asıl kalkan. PDF adı = bibkey, böylece atıflar .bib'e doğrudan eşlenir. |
| `assafelovic/gpt-researcher` | **Opsiyonel** (extra: `research`) | Gap raporu için iyi; retriever'lar `.env`'de Semantic Scholar / PubMed Central / arXiv'e kısıtlı. Çıktısı taslaktır, kaynakları `sspe-search` ile doğrulanmadan metne girmez. |
| `quarto-dev/quarto-cli` | **Çekirdek** (CLI, ayrı kurulum) | `.qmd` + `results.json` → DOCX/HTML/PDF. Dergi şablonları: `quarto-journals/*` uzantıları (`make journal J=elsevier`). |
| `microsoft/autogen` | **Kullanılmıyor** | Microsoft yeni geliştirmeyi Agent Framework'e taşıdı; AutoGen bakım modunda. Ayrıca Claude Code alt ajanları aynı rol dağılımını ek bağımlılık olmadan sağlıyor. |
| `crewAIInc/crewAI` (eski `joaomdmoura/crewAI`) | **Şimdilik yok** | Yalnızca hattı Claude Code dışında (ör. zamanlanmış, başsız) çalıştırmak gerekirse eklenir. |

Neden submodule değil: hepsi PyPI paketi ya da CLI. Submodule kaynak kodu kopyalar ama sürüm sabitleme/güncelleme yükü getirir; `pyproject.toml` extras daha temiz.

## Kurulum

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[all]"          # ya da sadece: pip install -e ".[qa,analysis]"
cp .env.example .env             # ANTHROPIC_API_KEY (+ opsiyonel SEMANTIC_SCHOLAR_API_KEY)
# Quarto: https://quarto.org/docs/get-started/
```

## Kullanım

```bash
make search Q="session RPE training load injury soccer"
make gap    Q="Elit basketbolda haftalık yük dalgalanması ile sakatlık ilişkisi"
make ask    Q="sRPE ile GPS tabanlı iç/dış yük arasındaki korelasyon aralığı nedir?"
make analysis render
```

Claude Code içinde: `literature-scout`, `methodologist`, `data-analyst`, `q1-reviewer` alt ajanları ve `/paper-loop` komutu.

## Dizinler

- `engine/literature/` — arama, paper-qa, gpt-researcher sarmalayıcıları
- `literature/` — PDF'ler, kanıt tablosu, gap raporları, paper-qa yanıtları
- `manuscript/` — Quarto projesi, `sections/*.qmd`, `analysis/run.py`, `reviews/`, `checklists/`
- `data/raw` (salt okunur, git dışı), `data/processed`
