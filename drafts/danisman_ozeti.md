---
title: "Tezden iki makaleye: özet ve karar bekleyen noktalar"
subtitle: "Avrupa Ligi Basketbol Takımlarının Diziliş Rotasyonlarının Yapay Zekâ Tabanlı Analizi"
date: 2026-11-18
lang: tr
---

# En önemli nokta

Tezin üç ana iddiası açık EuroLeague verisiyle (2016–17 → 2024–25, 9 sezon) yeniden sınandı:

- **Arketipler:** Tezdeki 7 küme birebir yeniden üretildi. Ancak oyuncu düzeyinde yeniden örneklendiğinde bu kümeler kararsız çıktı (ortalama Jaccard ≈ 0,44). Kararlılık ölçütüyle seçilen **5 işlevsel rol** ise yeniden üretilebilir (ortalama Jaccard ≈ 0,84).
- **"Belirli arketip kombinasyonları daha başarılıdır":** Bireysel oyuncu kalitesi (RAPM) kontrol edildiğinde rol bilgisi küçük bir katkı sağlıyor. Bu katkı **rol sayılarından** geliyor, **rol çiftlerinden (sinerjiden) gelmiyor**. Güç analizine göre küçük sinerjiler de yakalanabilirdi.
- **VAL/PIR ile ILP beşli seçimi:** PIR, aynı saha etkisine sahip oyuncular arasında iç oyuncuları sistematik olarak yüksek puanlıyor (kısmi η² ≈ 0,33). ILP ile seçilen beşliler, hangi değerle seçilirse seçilsin, antrenörün en çok oynattığı beşliden daha iyi değil. Tüm farkların güven aralıkları 0'ı içeriyor.

Bu sonuçlar tezi çürütmüyor. Tezi düzelten ve sınırlarını çizen iki makale üretiyor.

# Makale A: işlevsel roller

**Başlık:** *Functional player roles in EuroLeague basketball: stability, positional overlap and no evidence of role synergy in lineup performance*

- Yöntem: Gauss karışım modeli (tied kovaryans). K seçimi BIC'e ve oyuncu düzeyinde bootstrap kararlılığına göre yapıldı. Değişkenler ileri istatistikler, şut profili ve asist ağı.
- Bulunan roller: top taşıyıcı, kanat, açılan forvet, iç uzun ve pota koruyucu. Kanat rolü en az kararlı olanı; K = 4 çözümü duyarlılık analizi olarak raporlanıyor.
- Pozisyonla ilişki: rol ile pozisyon arasında güçlü bir ilişki var (Cramér V ≈ 0,73). "Pozisyonsuz oyun" yalnızca orta pozisyonlarda (kanat ve forvet) geçerli.
- Dizilim: rol bileşimi RAPM'in ötesinde küçük bir öngörü kazancı sağlıyor (permütasyon p ≈ 0,04). Kazanç sayı etkilerinden geliyor; çift etkileşimleri ek katkı sağlamıyor.
- Tezdeki formül testi (χ²) kısa dizilimlerin seçilme yanlılığına duyarlı. Asgari süre koyulunca "anlamlı" kombinasyon sayısı şans düzeyine iniyor.

# Makale B: oyuncu değeri ve ILP

**Başlık:** *Box-score performance indices depend on player role and show no advantage over coaches' rotations for lineup selection*

- Rolün açıkladığı varyans (η²): PIR40 için ≈ 0,33, VAL40 için ≈ 0,42, RAPM için ≈ 0,01.
- Bu fark üç ek analizde de korunuyor: RAPM sabit tutulduğunda, PIR bileşeni içermeyen rollerle ve güvenirlik düzeltmesinden sonra.
- Gelecek sezonları öngörmede (2023–24 test) RAPM, PIR ve VAL toplamlarından daha iyi. Farkların güven aralıkları 0'ı dışlıyor.
- Sezon içinde yalnızca RAPM tabanlı dizilim değeri ikinci yarıyı anlamlı biçimde öngörüyor. Ancak eşleştirilmiş farklar anlamlı değil.
- ILP ile antrenörün seçimi arasındaki farklar −1,7 ile +0,4 puan arasında ve tümü anlamsız. ILP beşlileri antrenör beşlisiyle yaklaşık 3 oyuncuyu paylaşıyor.
- Yorum: Antrenörler kutu skorunda görünmeyen bilgiyi kullanıyor. Buna "optimizer's curse" (gürültülü tahminleri maksimize etmenin bedeli) ekleniyor.

# Kalite güvencesi

- Metindeki tüm sayılar analiz çıktısından otomatik okunuyor; elle sayı yazılmadı.
- Tüm atıflar DOI'den gelen meta veriyle `references.bib` dosyasına eklendi ve otomatik olarak denetlendi.
- Literatür karşılaştırmaları tam metinlerden doğrulandı.
- Her iki makale bir Q1 hakem döngüsünden geçti. İlk turdaki kritik eleştirilerin tamamı yeniden analizle giderildi: oyuncu düzeyinde bootstrap, aşırı parametreli kovaryansın düzeltilmesi, döngüsel boy değişkeninin çıkarılması, cezanın çapraz doğrulamayla seçilmesi, koşullu yanlılık analizi ve eşleştirilmiş ILP testi.
- Veri ve kod açık; tek komutla yeniden üretilebilir (`make data paper-a paper-b render-all`).

# Danışmanla karar verilecek noktalar

1. Yazarlar, sıralama, kurum, fon, çıkar çatışması ve CRediT bilgileri.
2. Tezin kaynakçada nasıl gösterileceği: YÖK Tez Merkezi numarası gerekiyor.
3. Hedef dergiler. Öneri: A için *Journal of Sports Sciences* veya *JQAS*; B için *JQAS* veya *European Journal of Sport Science*.
4. Synergy verisi: Synergy'den yazılı izin alınırsa dış doğrulama olarak (rol ↔ oyun tipi) kullanılabilir. İzin alınana kadar makalelere girmiyor.
5. Kod ve veri arşivi için Zenodo DOI'si.
6. Tezde gözden geçirilmesi önerilen noktalar:
   - EK-2.7'deki basılı kod, çalışan koddan farklı.
   - NRTG tanımı tutarsız (100 hücum başına mı, 40 dakika başına mı?).
   - "5.292 dizilim" aslında maç-takım gözlemi sayısı.
