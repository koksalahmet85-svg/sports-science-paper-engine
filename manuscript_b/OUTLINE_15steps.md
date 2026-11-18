# Makale B — 15 Adım iskeleti (Drake & Han, 2025)

Sayı yok; tüm değerler `manuscript/analysis/results.json` anahtarlarından gelir. Adım 1, 2, 7, 10 yazar onayı bekleyen önerilerdir.

## Adım 1 — Tez
**Öneri:** *The EuroLeague's official performance index favours some player roles and forecasts lineup outcomes worse than
adjusted plus-minus, and lineups optimised on any of these values do not outperform the coach's own rotation.*

## Adım 2 — Anlatı yayı: "Ölçüm karşılaştırması → karar modeli testi"
- Motivasyon: kulüpler oyuncu değerini PIR gibi kutu skoru endeksleriyle izliyor; tezde bu değerler ILP ile beşli seçimine aktarıldı.
- **Parça 1 (ölçüm):** PIR40 / VAL40 / RAPM — (a) rol yanlılığı (η², rol ortalamaları), (b) örneklem dışı öngörü (zamansal R², sezon içi yarı-sezon doğrulaması).
- **Parça 2 (karar modeli):** ILP ile seçilen beşliler, sezonun ikinci yarısında antrenörün en çok oynattığı beşliyle karşılaştırılır; rol kısıtlarının etkisi.
- Yeni bilgi: değer ölçütünün seçimi önemli, ama ölçütlerden optimize edilen beşli antrenör kararını geçmiyor.

## Adım 3–5 — Yöntem → gerekçe → sonuç
| # | Yöntem | Gerekçe | Sonuç (results.json) |
|---|---|---|---|
| 1 | PIR40, VAL40, RAPM tanımları; RAPM: ridge, maç gruplu CV | Uygulamadaki endeks + tezdeki endeks + kalite kontrollü etki ölçüsü | — |
| 2 | Rol (Makale A nihai rolleri) başına η², oyuncu bootstrap GA; RAPM λ duyarlılığı | Rol yanlılığı ölçütün özelliği mi, büzülmenin mi? | `paper_b_values` |
| 3 | 2016–2022 → 2023–2024 segment net rating R²; maç bootstrap GA | Örneklem dışı geçerlilik | `lineup_model_roles_final_K*` → `test_R2` |
| 4 | Yarı sezon tasarımı: dizilim toplam değerinin (takım içi z) ikinci yarı net rating'ine eğimi; takım-sezon kümeli bootstrap | Ölçütün karar birimi olan dizilimde geçerliliği | `ilp_validation.amac_fonksiyonu_egimi` |
| 5 | ILP (kısıtsız / tezdeki ≥ 1 pivot / dengeli) vs en çok süre alan beşli | Karar modelinin antrenöre katkısı | `ilp_validation.ilp_beslisi` |

## Adım 6 — Giriş
- Alan: kulüpler ve medya oyuncuları PIR gibi kutu skoru endeksleriyle değerlendiriyor; analitik karar destek çerçeveleri beşli optimizasyonu öneriyor.
- Niş: endekslerin rol yanlılığı ve örneklem dışı geçerliliği EuroLeague'de sınanmadı; optimizasyon çıktıları antrenörün fiili kararlarıyla karşılaştırılmıyor.
- *Here we show* cümlesi.

## Adım 7 — Bulgular
- B1: Kutu skoru endeksleri rolle güçlü biçimde ilişkili; RAPM değil.
- B2: RAPM gelecekteki dizilim sonuçlarını kutu skoru endekslerinden daha iyi öngörüyor.
- B3: Optimize edilen beşliler ortalamanın üstünde ama antrenörün en çok oynattığı beşliden ayırt edilemiyor; rol kısıtları sonucu değiştirmiyor.

## Adım 8–9 — Sorun ↔ yanıt
| Sorun | Yanıt |
|---|---|
| RAPM'in kendisi de gürültülü, mutlak R² çok küçük | Karşılaştırma göreli; maç bootstrap GA veriliyor; segment düzeyi gürültü tüm ölçütler için aynı |
| RAPM büzülmesi rol farkını yapay olarak küçültebilir | Daha zayıf ceza (λ = 1000) ile η² yeniden hesaplandı |
| ILP beşlisi sahada nadiren tam olarak oynuyor | ≥ 4 oyuncu eşleşmesi kullanıldı; hücum payı raporlandı |
| Antrenör tabanı (dakika) bilgi sızıntısı içeriyor mu? | Yalnızca sezonun ilk yarısındaki dakikalar kullanıldı |
| Kazanılan maç değil net rating | Net rating maç sonucunun en doğrudan dizilim düzeyi karşılığı; maç düzeyi analiz gelecek çalışma |
| Rakip gücü | RAPM toplamı ve ev sahipliği kontrol edildi |

## Adım 10 — Kapanış tezi
**Öneri:** *Clubs should compare players with plus-minus-based measures rather than PIR, and judge lineup tools against the coach's own rotation, the benchmark any decision aid must beat.*

## Adım 11 — Paragraflar
Giriş 3 · Yöntem 6 alt başlık · Bulgular 4 (rol yanlılığı, zamansal R², yarı sezon eğimi, ILP vs antrenör) · Tartışma 6 + kapanış.

## Adım 12 — Şekiller
- Şekil 1: *Box-score indices, unlike RAPM, differ systematically between player roles.* (rol × ölçüt z-ortalamaları)
- Şekil 2: *Only RAPM-based lineup value predicts second-half net rating more strongly than minutes played.* (eğim forest plot)
- Şekil 3: *Optimised lineups perform no better than the coach's most-used players.* (ILP karşıtlıkları forest plot)
