# Sports Science Paper Engine — Claude Code çalışma kuralları

## Değişmez kurallar
1. **Kaynaksız iddia yok.** Metne giren her `[@key]` `manuscript/references.bib`'de olmalı; `make check-cites` bunu denetler. Kaynak ancak `sspe-search` ile eklenir; bellekten BibTeX yazılmaz.
2. **Elle sayı yok.** Bulgulardaki her sayı `manuscript/analysis/results.json`'dan okunur.
3. **Ham veriye dokunma.** `data/raw/` salt okunur.
4. **Tartışmadaki karşılaştırmalar** `sspe-ask` çıktısına (`literature/answers/`) dayanır.
5. Eksik bilgi → varsayım değil, `manuscript/OPEN_QUESTIONS.md`'ye soru.

## Hat
RQ → `literature-scout` (sspe-search / sspe-gap / sspe-ask) → `methodologist` → `data-analyst` (`make analysis`) → yazım → `/paper-loop` (q1-reviewer döngüsü) → `make render` / `make journal J=elsevier`.

## Komutlar
- `make search Q="..."`, `make gap Q="..."`, `make ask Q="..."`
- `make analysis`, `make check-cites`, `make render`
