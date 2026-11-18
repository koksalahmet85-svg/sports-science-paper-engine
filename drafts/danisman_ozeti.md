---
title: "Tezden iki makaleye: özet ve karar bekleyen noktalar"
subtitle: "Avrupa Ligi Basketbol Takımlarının Diziliş Rotasyonlarının Yapay Zekâ Tabanlı Analizi"
date: 2026-11-18
lang: tr
---

# En önemli nokta

Tezin üç ana iddiası açık EuroLeague verisiyle (2016–17 → 2024–25, 9 sezon, 2.646 maç) yeniden sınandı. İki hakem turundan sonra ulaşılan sonuçlar:

1. **Arketipler.** Tezdeki 7 küme kod düzeyinde birebir yeniden üretildi. Ancak oyuncu düzeyinde yeniden örneklemede kararsız çıktı (ortalama Jaccard ≈ 0,44). Önceden belirlenen kararlılık kuralı **4 işlevsel rol** seçti (Jaccard ≈ 0,89): top taşıyıcı, kanat/forvet, iç uzun ve pota koruyucu. **5 rol** neredeyse aynı kararlılıkta (≈ 0,85); bu çözüm kanat ile açılan forveti ayırıyor.
2. **"Belirli arketip kombinasyonları daha başarılıdır" iddiası desteklenmedi.** Her sezonun rolleri o sezonun verisiyle belirlendiğinde, rol bileşimi RAPM'in ötesinde anlamlı görünüyordu. Ancak test sezonlarının rolleri yalnızca önceden bilinen bilgiyle verildiğinde etki kayboldu (p ≈ 0,36). Sinerjiyi saptama gücü düşük (en fazla %16); bu nedenle "sinerji yoktur" da denemez.
3. **VAL/PIR ile ILP beşli seçimi.** PIR, aynı saha etkisine (RAPM) sahip oyuncular arasında pota koruyucu ve iç uzunlara top taşıyıcılardan yaklaşık 4–5 puan/40 dk fazla veriyor (kısmi η² ≈ 0,27). ILP ile seçilen beşliler, antrenörün en çok oynattığı beşliden hiçbir varyantta daha iyi değil: doğrudan farklar −3,6 ile +1,5 arasında ve tümü anlamsız.

Bu çalışma tezi çürütmüyor. Tezin sonuçlarını yöntemsel olarak düzelten ve sınırlarını açıkça çizen iki makale üretiyor.

# Makale A: işlevsel roller

**Başlık:** *Functional player roles in EuroLeague basketball: stability, positional overlap and no robust added value for lineup performance beyond player quality*

- **Yöntem:** Gauss karışım modeli (tied kovaryans) ve oyuncu düzeyinde bootstrap (B = 500, tek koşu). Değişkenler: ileri istatistikler, şut profili ve asist ağı.
- **Pozisyonla ilişki:** Top taşıyıcıların %92'si guard, pota koruyucuların %90'ı pivot. Kanat/forvet rolü ağırlıkla forvetlerden oluşuyor. Pozisyon örtüşmesi ön alanda (iç uzun: %59 pivot, %39 forvet).
- **Sızıntı denetimi:** Hakemin önerdiği bu denetim, önceki "anlamlı" bulgunun yeni oyuncuların kalitesine vekâlet eden rol etiketlerinden kaynaklandığını gösterdi.
- **Tezdeki χ² formül testi:** Kısa dizilimlerin seçilme yanlılığına duyarlı; asgari süre koyulunca "anlamlı" kombinasyon sayısı şans düzeyine iniyor.

# Makale B: oyuncu değeri ve ILP

**Başlık:** *Box-score performance indices depend on player role and show no advantage over coaches' rotations for lineup selection*

- **Rolün açıkladığı varyans (η²):** PIR40 için ≈ 0,26, VAL40 için ≈ 0,38, RAPM için ≈ 0,005.
- **Bulgu sağlam:** Bu fark dört denetimin hepsinde korunuyor:
  - RAPM sabit tutulduğunda,
  - ölçüm hatası düzeltildiğinde (2SLS),
  - PIR bileşeni içermeyen rollerle (iki sürüm),
  - güvenirlik düzeltmesinden sonra.
- **Gelecek sezonları öngörme:** RAPM, PIR toplamından daha iyi; farkın güven aralığı 0'ı dışlıyor. Sezon içinde ise ölçütler arası farklar anlamlı değil.
- **ILP ve antrenör:** Aynı takım-sezon içinde doğrudan karşılaştırıldı. Hiçbir varyantta avantaj yok; güven aralıkları geniş, bu nedenle bulgu "eşdeğerlik" değil, "kanıt yok" olarak raporlandı.

# Kalite güvencesi

- **Sayılar:** Metindeki tüm sayılar analiz çıktısından otomatik okunuyor. Kod sürümü, tohum ve paket sürümleri `results.json` içinde kayıtlı.
- **Atıflar:** Tümü DOI meta verisiyle eklendi ve otomatik denetlendi. Doğrulanamayan iki literatür iddiası (Chen, Wei) metinden çıkarıldı.
- **Hakem süreci:** Q1 düzeyinde üç hakem turu yapıldı. Her turdaki kritik eleştiriler yeniden analizle giderildi. Bulgular değiştiğinde (5 → 4 rol, anlamlı → anlamsız rol etkisi) dürüstçe raporlandı.
- **Yeniden üretim:** Veri ve kod açık; tek komutla yeniden üretilebilir: `make data paper-a paper-b render-all`.

# Danışmanla karar verilecek noktalar

1. Yazarlar, sıralama, kurum, fon, çıkar çatışması ve CRediT bilgileri.
2. Tezin kaynakçadaki künyesi: YÖK Tez Merkezi numarası gerekiyor. "Prior dissemination" beyanı hazır.
3. Hedef dergiler. Öneri: A için *Journal of Sports Sciences* veya *JQAS*; B için *JQAS* veya *European Journal of Sport Science*.
4. Synergy verisi: yazılı izin alınırsa dış doğrulama olarak kullanılabilir. İzin alınana kadar makalelere girmiyor.
5. Kod ve veri arşivi için Zenodo DOI'si (gönderimden önce).
6. Tezde düzeltilmesi önerilen noktalar:
   - EK-2.7'deki basılı kod, çalışan koddan farklı.
   - NRTG tanımı tutarsız (100 hücum başına mı, 40 dakika başına mı?).
   - "5.292 dizilim" aslında maç-takım gözlemi sayısı.
