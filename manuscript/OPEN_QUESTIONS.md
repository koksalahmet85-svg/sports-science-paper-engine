# Açık sorular — Q1 hakem riski haritası

Tez özetine göre bir Q1 hakemin büyük olasılıkla soracağı sorular. Her birine tezden cevap (sayfa/bölüm) ya da ek analiz gerekiyor.
Öncelik: 🔴 reddettirebilir · 🟠 major revizyon · 🟡 minor.

## Model ve ölçüm
1. 🔴 **VAL40 + GBR döngüselliği.** VAL (PIR) kutu-skoru istatistiklerinin doğrusal toplamıdır. GBR'nin girdileri sayı, ribaund, asist gibi aynı bileşenleri içeriyorsa model hedefi yeniden üretir; yüksek R² bilgi taşımaz (döngüsel analiz / double dipping — Drive'daki Kriegeskorte ve ark., 2009). **Soru:** Öznitelikler neler? Hedefin bileşenleri girdilerden çıkarıldı mı? Tahmin bir sonraki sezonun VAL40'ı mı (ileriye dönük) yoksa aynı sezonunki mi?
2. 🟠 **Dakika normalizasyonu gürültüsü.** 40 dakikaya ölçekleme az oynayan oyuncuları şişirir. **Soru:** Minimum dakika / maç eşiği var mı? Küçültme (empirical Bayes shrinkage) uygulandı mı?
3. 🟠 **VAL'ın geçerliliği.** PIR savunma katkısını ve takım bağlamını büyük ölçüde dışarıda bırakır; hacmi ödüllendirir. Bir alternatif ölçüyle (ör. RAPM, net rating) duyarlılık analizi gerekebilir.

## Kümeleme
4. 🟠 **k = 7 gerekçesi.** Calinski–Harabasz ve Davies–Bouldin (Drive'da mevcut) iyi; ek olarak bootstrap ile küme kararlılığı (ör. Jaccard) ve sezonlar arası kararlılık bekleniyor.
5. 🟡 **Ön işleme.** Standardizasyon, yüksek korelasyonlu değişkenler (VIF), hacim mi oran mı (per-40 / yüzde) kullanıldığı açıkça raporlanmalı.

## Dizilim analizi
6. 🔴 **Segment tanımı ve küçük örneklem.** 67.001 segmentin çoğu birkaç hücumluk olabilir. **Soru:** Segment başarısı nasıl ölçüldü (net rating / 100 hücum)? Minimum hücum eşiği ve hücum sayısıyla ağırlıklandırma var mı?
7. 🔴 **"Rastlantısal değil" testi.** Segmentler bağımsız değil (aynı maç, takım, oyuncu). **Soru:** Hangi test kullanıldı? Ki-kare bağımsızlık varsayımını ihlal eder. Takım-sezon yapısını koruyan permütasyon testi veya karma etkili model gerekir.
8. 🟠 **Nedensellik dili.** "Başarılı formüllerde arketip dağılımı rastlantısal değil" ilişkiseldir. İyi takımlar hem iyi oyuncuya hem belirli bileşimlere sahip olabilir (karıştırıcı: oyuncu kalitesi, rakip gücü). Rakip ve takım kalitesine göre düzeltme önerilir.

## Optimizasyon ve Bayesgil katman
9. 🔴 **Optimizasyoncunun laneti (optimizer's curse).** ILP, gürültülü tahminlerin en yükseklerini seçer; seçilen beşlinin beklenen değeri yukarı yanlıdır. Bayesgil küçültme bunu hafifletebilir, ama örneklem dışı doğrulama şart. **Soru:** "Optimal" beşliler sonraki maçlarda / sezonda gerçek dizilimlerle karşılaştırıldı mı?
10. 🟠 **Bayesgil güncelleme tanımı.** Öncül ne, olabilirlik ne, neyi güncelliyor (oyuncu değeri mi, arketip-başarı olasılığı mı)? Öncül duyarlılık analizi gerekir.
11. 🟡 **ILP global optimum savı.** Wolsey (2020) atfı doğru; ancak optimum, girdinin tahmin belirsizliği altında "optimal" değildir. Bu ayrım metinde net olmalı.

## Veri
12. 🟠 **Kesintili sezonlar.** 2019-20 COVID nedeniyle yarıda kaldı; 2020-21 seyircisizdi (ev sahibi avantajı değişti); 2021-22'de Rus kulüpleri sezon ortasında çekildi. **Soru:** Bu sezonlar nasıl ele alındı?
13. 🟡 **Tekrarlanabilirlik.** EuroLeague API'si bu oturumda erişilebilir. Veri çekme betiği `manuscript/analysis/` altına konursa veri/kod paylaşımı beyanı güçlenir.

## Çerçeveleme
14. 🟠 **"Transfer yatırımı" iddiası.** EuroLeague maaş/transfer verisi kamuya açık değil. Yatırım-getiri ilişkisi doğrudan ölçülmüyorsa başlık ve girişte iddia yumuşatılmalı ya da bir maliyet vekili tanımlanmalı.
15. 🟡 **Ders kitabı atıfları.** Hastie, Géron, McKinney gibi kaynaklar tezde uygun; dergi makalesinde metodolojik iddialar birincil makale kaynaklarıyla desteklenmeli.
