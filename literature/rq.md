# Araştırma özeti — Doktora tezi → Q1 makale(ler)

Kaynak: tez özeti (Ahmet Köksal), Drive "Doktora Literatur" klasörü, 2026-10-30.

## Tezin iddiası (özetten)
- **Bağlam:** Profesyonel basketbolda transfer yatırımının sahadaki karşılığı kadro dizilimi kararlarına bağlıdır.
- **Amaç:** Performans ölçümünden kadro optimizasyonuna uzanan YZ tabanlı karar destek çerçevesi; EuroLeague verisiyle sınama.
- **Veri:** EuroLeague 2016–2024; 2.014 oyuncu-sezon; 67.001 kadro dizilimi (lineup) segmenti.
- **Yöntem zinciri:** VAL40 (40 dakikaya normalize Valuation/PIR) → Gradient Boosting Regressor → Ward kümelemesi (7 işlevsel arketip) → doğrusal tam sayılı programlama (ILP) ile optimal beşli → Bayesgil güncelleme.
- **Bulgu:** Başarılı dizilimlerde arketip dağılımı rastlantısal değil; EuroLeague'in pozisyon-ötesi yapısı nicel olarak belgeleniyor.

## Yapılandırılmış soru (PECO)
| | |
|---|---|
| **P** | EuroLeague oyuncuları ve 5'li dizilimleri, 2016-17 → 2023-24 |
| **E** | Dizilimin arketip bileşimi (7 işlevsel arketip) |
| **C** | Rastlantısal / pozisyon-temelli (PG–C) bileşimler |
| **O** | Dizilim verimliliği (net rating / 100 hücum — tanım netleştirilecek) |

## Makale bölme önerisi (tez → 2 makale)
1. **Makale A — "Positionless archetypes in EuroLeague":** VAL40 + Ward kümeleme + arketip bileşimi ile dizilim başarısı. Katkı: Avrupa basketbolunda pozisyon-ötesi yapının ilk çok-sezonluk nicel belgesi (NBA odaklı literatürle karşılaştırmalı).
2. **Makale B — "From player value to lineup decisions":** GBR + ILP + Bayesgil güncelleme karar destek çerçevesi. Hedef: yöneylem araştırması / spor analitiği dergileri.

Hedef dergiler, SJR/JCR çeyrekleri gönderim öncesi güncel olarak doğrulanmalı.

## Doğrudan rakip / en yakın çalışmalar (references.bib'de)
- Arketip ve kadro: [@penner2025player], [@kalman2020lineup], [@yamada2024offensive], [@guo2025quantifying], [@li2026impact]
- Dizilim değerlemesi (RAPM): [@grassetti2020extended], [@petridis2026lineup], [@grassetti2026revisiting], [@watts2026dummy]
- Takım arkadaşı etkileşimi / Markov: [@sandri2020markov], [@zuccolotto2019modelling]
- Avrupa elit basketbolu: [@alonsoprezchao2025perceptual]

**Kritik not — yenilik iddiasına en yakın iki çalışma** (içerik web üzerinden doğrulandı, 2026-10-30):
- [@penner2025player] — Frontiers in Sports and Active Living, 2025 (doi:10.3389/fspor.2025.1639431). Üniversite ve profesyonel lig oyuncularını pozisyon yerine oyun stiline göre **9 kümeye** ayırıyor; şampiyonluk kadrosu kurmak için lig gücü metriği ve oyuncu sıralaması öneriyor. NBA ve FIBA verisi. → Tezin farkı: tek elit Avrupa ligi, 8 sezon, **dizilim (lineup) düzeyinde** sınama ve ILP ile karar desteği.
- [@petridis2026lineup] — arXiv:2601.15000, 2026. Rakip gücüne göre düzeltilmiş dizilim derecelendirmesi; oyuncu düzeyi bilgiyi **öncül** olarak kullanıyor ve küçük örneklemli dizilimlerde tahmin gücünü artırıyor (NBA). → Tezin Bayesgil katmanıyla doğrudan ilişkili; ayrıca OPEN_QUESTIONS #6 ve #9 (küçük segment, optimizasyoncunun laneti) için hazır bir yöntemsel çözüm.
