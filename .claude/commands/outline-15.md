---
description: Bir makale için Drake & Han (2025) 15 Adım iskeletini kurar veya mevcut taslağı bu adımlarla denetler
argument-hint: "[makale adı, ör. 'Makale B']"
---
Hedef: $ARGUMENTS. Kaynak: Drake & Han (2025), "How to write a scientific paper in fifteen steps", PLOS Comput Biol [@drake2025write]. Örnek: `manuscript/OUTLINE_15steps.md` (Makale A).

1. `manuscript/OUTLINE_<ad>.md` oluştur. Adım 1 (tez cümlesi), 2 (iki parçalı anlatı yayı), 7 (bulgular) ve 10 (kapanış tezi) için ÖNERİ yaz ve yazarın onayına bırak — makale, fikirler yazara ait olmadan yapay zekâ kullanılmamasını öneriyor.
2. Adım 3–5: yöntem → gerekçe → sonuç tablosu. Sonuçlar yalnızca `analysis/results.json`'daki anahtarlara dayanır; sayı yazma, anahtar adı yaz.
3. Adım 6: giriş için alan → niş → nişi doldurma; "Here we show" cümlesi zorunlu.
4. Adım 8–9: her sınırlılık bir YANITLA eşleşmeli (yalnızca sorun listesi kabul edilmez).
5. Adım 10: kapanış olumlu ve somut bir uygulamayla biter; "daha fazla araştırma gerekir" ile bitmez.
6. Adım 11: her paragraf için bir amaç cümlesi. Adım 12: şekiller yazımdan önce `analysis/` altındaki bir betikle üretilir; şekil başlığının ilk cümlesi tam bir cümledir.
7. Taslak varsa her adımı taslakla karşılaştır, eksikleri ⚠️ ile işaretle ve düzelt; ardından `make check-cites` ve `quarto render`.
