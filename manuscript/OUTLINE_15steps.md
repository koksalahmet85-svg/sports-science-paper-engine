# Makale A — 15 Adım iskeleti (Drake & Han, 2025, PLOS Comput Biol, doi:10.1371/journal.pcbi.1013505)

Bu belge yazımın "düşünme" kısmıdır; makaleye girmez. Sayılar burada yok, hepsi `analysis/results.json`'da.
Makaleye dönük her yeni paragraf önce burada bir **amaç cümlesi** alır (Adım 11).

> Not (Adım 0): Makale, yapay zekâyı fikirler biçimlendikten sonra kullanmayı öneriyor. Adım 1, 2, 7 ve 10 yazarın
> kendi kararıdır; aşağıdakiler öneridir, yazar onaylamadan kesinleşmez.

## Adım 1 — Tez (tek bildirme cümlesi)
**Öneri:** *Five functional roles describe EuroLeague players reproducibly, but a lineup's role mix adds nothing to its
performance once player quality is known.*
Kontrol: özne (roles / role mix) + yüklem (describe / adds nothing) + kapsam (EuroLeague, lineup performance) ✔

## Adım 2 — Anlatı yayı (iki parça)
Şablon: **"Pattern in observations → Model to test it"** (makaledeki tabloda son satıra yakın).
- Motivasyon: roller hem pozisyonların yerine hem de dizilim kurmak için kullanılıyor.
- Soru: hangi roller gerçekten kararlı, ve rol karışımı dizilim başarısını açıklıyor mu?
- **Parça 1 (gözlem):** açık veriden kararlı 5 rol; pozisyonlarla örtüşmesi.
- **Parça 2 (model):** oyuncu kalitesini (RAPM) kontrol eden dizilim modeli + permütasyon testi.
- Yeni bilgi: roller betimleyici olarak geçerli, ama dizilim başarısının açıklayıcısı değil.

## Adım 3–5 — Yöntemler, gerekçeler, sonuçlar
| # | Yöntem | Gerekçe | Sonuç(lar) |
|---|---|---|---|
| 1 | Rol değişkenleri: sahadaki gerçek paydalarla paylar, şut profili, asist ağı, boy; sezon içi z | Rol ≠ kalite; dönem eğilimini ayıkla | R1 |
| 2 | GMM + bootstrap Jaccard + dönemler arası ARI; K = 4–8; Ward karşılaştırması | K'yı iç geçerlik indeksi değil kararlılık seçsin | R1: 4–5 rol kararlı, ≥ 6 değil; R2: önceki 7 kümelik çözüm kararsız |
| 3 | Rol × resmî pozisyon (Cramér V, baskın pozisyon payı) | "Pozisyon-ötesi" iddiasını doğrudan sına | R3: uçlarda bağlı, ortada kesiyor |
| 4 | RAPM (ridge, maç bazında CV), zamansal doğrulama | Bireysel kaliteyi kontrol etmek | R4: RAPM rolden bağımsız, VAL40 değil; R5: RAPM geleceği VAL40'tan iyi öngörüyor |
| 5 | RAPM artığı ~ rol bileşimi; rol etiketi permütasyonu | Rol karışımının EK bilgisini sınamak | R6: kazanç şanstan ayırt edilemiyor (K = 5 ve 4) |
| 6 | Önceki prosedürün (anlamlı formül + χ²) permütasyonlu tekrarı | Önceki pozitif bulgunun kaynağını göstermek | R7: kısa dizilim yanlılığı; ≥ 2 dk ile etki yok |

## Adım 6 — Giriş: alan → niş → nişi doldurma
- **Alan:** veri temelli roller pozisyonların yerini alıyor ve dizilim kararlarında kullanılıyor.
- **Niş:** (a) rol sayısı kararlılıkla seçilmiyor; (b) rol–başarı ilişkisi oyuncu kalitesi kontrol edilmeden raporlanıyor; (c) EuroLeague'de rol çalışması yok.
- **Nişi doldurma:** *Here we show* cümlesi — ⚠️ **taslakta eksikti, eklendi.**

## Adım 7 — Bulgular (sonuçların yorumu)
- B1 (R1, R2): Açık veriyle beşten ince bir rol yapısı kararlı değil; iç geçerlik indeksleri tek başına yeterli değil.
- B2 (R3): "Pozisyonsuz basketbol" pozisyon yelpazesinin ortasının özelliği, bütününün değil.
- B3 (R4–R6): İyi bir beşli, ilk yaklaşımla iyi oyunculardan oluşan beşlidir.
- B4 (R4, R5): Kutu skoru değer endeksleri rol yanlı; roller arası karşılaştırmada kullanılmamalı.
- B5 (R7): Önceki rol-kombinasyonu bulguları, kısa dizilimlerin seçilme biçiminden doğmuş olabilir.

## Adım 8–9 — Sorun ↔ yanıt çiftleri (tartışmanın ikinci yarısı)
| Sorun | Yanıt |
|---|---|
| Segment sonucu çok gürültülü; küçük sinerji etkileri gözden kaçmış olabilir | Testin gücü sınırlı; sonuç "etki yok" değil "kaliteye ek bilgi gösterilemedi" olarak okunmalı; permütasyon aynı gürültüyü taşıdığı için karşılaştırma adil |
| Yalnızca ikili rol etkileşimleri sınandı | Daha yüksek dereceli etkileşimler bu örneklemde tahmin edilemez; ileride oyun-tipi verisiyle |
| Savunma rolü dolaylı ölçüldü | Rol yapısı dört değişken grubunda aynı çıktı; savunma izleme verisi gelince yeniden sınanmalı |
| Kanat rolü orta kararlılıkta | Bu rol yalnızca betimsel kullanılmalı; ana sonuç (rol bileşiminin ek bilgisi yok) K = 4 ile de aynı |
| Roller tüm sezondan hesaplandı (aynı sezonun sonucuyla) | Rol değişkenleri sonuçtan (net rating) bağımsız; zamansal doğrulama 2016–2022 → 2023–2024 |
| Bulgular EuroLeague'e özgü | Yöntem ve kod açık; diğer liglerde doğrudan tekrarlanabilir |
⚠️ Taslaktaki "Limitations" yalnızca sorun listesiydi (makaledeki "üçüncü yanıt yetersiz" örneği) — **yanıtlarla yeniden yazıldı.**

## Adım 10 — Kapanış paragrafının tezi
**Öneri:** *Teams can describe players with five reproducible roles, but they should value them — and build lineups — with
plus-minus-based measures rather than with role mix or box-score valuation.*
Kurallar: olumlu bitir, "daha fazla araştırma gerekir" ile bitirme, somut uygulama öner. ⚠️ Taslak kapanışı bir uyarıyla
("biased by role") bitiyordu — **yeniden yazıldı.**

## Adım 11 — Paragraflar ve amaç cümleleri
**Giriş**
1. Roller pozisyonların yerini alıyor ve sayıları çalışmadan çalışmaya değişiyor. (alan)
2. İki boşluk: kararlılık ve kalite kontrolü. (niş)
3. Amaç + *Here we show*. (doldurma)

**Yöntem** — Tasarım ve veri · Dizilim segmentleri · Rol değişkenleri · Kümeleme ve K seçimi · Roller ve pozisyonlar · Roller ve dizilim performansı

**Bulgular**
1. Rol sayısı ve kararlılık (Şekil 1, Tablo 1)
2. Beş rol (Şekil 2, Tablo 2)
3. Roller ve pozisyonlar
4. Değer, RAPM ve rol bileşimi
5. Duyarlılık: önceki prosedür

**Tartışma**
1. Ana bulgunun özeti (tez)
2. B1 — literatürle karşılaştırma
3. B2 — pozisyonsuzluk ortada
4. B3 + B5 — rol bileşimi ve önceki bulgular
5. B4 — değer endekslerinin rol yanlılığı
6. Sorun ↔ yanıt çiftleri
7. Kapanış (Adım 10)

## Adım 12 — Şekiller (başlıklar tam cümle)
- **Şekil 1.** *Role partitions finer than five are not stable under resampling.* — `figures/fig1_stability.png`
- **Şekil 2.** *The five roles differ mainly in shot creation, shot location and size.* — `figures/fig2_role_profiles.png`
- Aday Şekil 3: permütasyon sıfır dağılımı + gözlenen kazanç (sıfır dağılımı şu an saklanmıyor; `lineup_model.py` güncellenmeli).

## Adım 13–15 — Konu cümlesi, kapanış cümlesi, destek cümleleri
Taslakta paragrafların çoğu konu cümlesiyle başlıyor. Kontrol edilecek: her paragrafın son cümlesi bir sonrakine geçiş yapıyor mu?
Bu, hakem döngüsünde (`q1-reviewer`) ayrı bir madde olarak kontrol edilecek.
