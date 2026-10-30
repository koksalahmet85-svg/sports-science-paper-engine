# Açık sorular — Q1 hakem riski haritası (tez metnine göre güncellendi)

Kaynak: tez tam metni (Ege Üniv., 2026, "Avrupa Ligi Basketbol Takımlarının Diziliş Rotasyonlarının Yapay Zeka Tabanlı Analizi") + Consensus taraması (`literature/consensus_report.md`).
Durum: ✅ tezde karşılanmış · ⚠️ kısmen · ❌ açık. Öncelik: 🔴 reddettirebilir · 🟠 major · 🟡 minor.

## 🔴 Kritik (makaleye taşınmadan önce çözülmeli)

1. ⚠️ **VAL40 + GBR döngüselliği.** Tez bunu açıkça kabul ediyor: öznitelikler VAL40'ın aritmetik bileşenlerini içeriyor; R² = 0,949 "tahmin değil açıklayıcı ayrıştırma" olarak yorumlanıyor. Şeffaflık iyi, ama Q1 hakem "o zaman GBR aşaması neden var?" diye soracak.
   **Öneri (birini seç):** (a) Makale A'dan GBR'yi çıkar, VAL40'ı doğrudan kullan; (b) GBR'yi **ileriye dönük** kur: t sezonunun özniteliklerinden t+1 sezonunun VAL40'ını tahmin et — bu gerçek bir tahmin görevi olur ve ILP'ye girdi olarak savunulabilir.

2. ❌ **Ki-kare özette yanlış referansla raporlanıyor.** Özetteki χ²(6) = 35,12, arketiplerin **eşit (%14,3)** dağıldığı varsayımına karşı. Arketipler zaten eşit sıklıkta değil; bu sıfır hipotezi zayıf. Gerçek oyuncu dağılımına karşı değer χ² = 27,68 (tez, Bölüm 4). Ayrıca segmentler bağımsız değil.
   **Öneri:** Başlık bulgusu olarak gerçek dağılıma karşı testi raporla; ek olarak takım-sezon bloklarını koruyan **permütasyon testi** veya rastgele takım/sezon kesişimli karma etkili lojistik model ekle.

3. ❌ **Küme kalitesi düşük: silhouette = 0,089** (K=6'da 0,115). Tez bunu "keskin sınıf değil işlevsel etiket" olarak çerçeveliyor ve GMM karşılaştırması yapmış (Tablo 10) — iyi. Ama kararlılık analizi yok.
   **Öneri:** Bootstrap küme kararlılığı (Jaccard; [@hennig2007cluster]); sezonlar arası kararlılık; K seçimini CH + DB + kararlılık birlikte gerekçelendir. Yumuşak üyelik (GMM) zaten var — [@kalman2020lineup] ile aynı yaklaşım, karşılaştırmalı sun.

4. ❌ **ILP için örneklem dışı doğrulama yok; optimizasyoncunun laneti** [@smith2006optimizer]. Optimal beşli toplam değeri (131,6–142,7) VAL40 tahminlerinin toplamı; sahadaki karşılığı sınanmamış. Tez de H4 için "gerçek maçlarda geriye dönük doğrulama yapılmamıştır" diyor.
   **Öneri:** 2016–2022'de seç, 2023–2024'te ILP beşlilerinin (veya en yakın gözlenen beşlilerin) hücum başına net verimini gerçek rotasyonlarla karşılaştır.

## 🟠 Major

5. ⚠️ **Segment gürültüsü.** Ortalama stint süresi 1,95 dk (Tablo 8). Segment düzeyi öngörü gücü r = 0,074 — tez bunu dürüstçe raporluyor.
   **Öneri:** Hücum sayısı eşiği + ağırlıklandırma; dizilim değerini regularize et (L-RAPM, öncül olarak arketip bilgisi: [@petridis2026lineup]). Bu aynı zamanda Bayesgil katmanını güçlendirir.
6. ⚠️ **Seçim yanlılığı.** DKR (Düşük Kullanım Rol) aşırı temsili muhtemelen "rol oyuncuları yıldızlarla birlikte oynar" seçim mekanizması — tez Bölüm 5.3'te kabul ediyor. Makalede rakip ve oyuncu kalitesine göre düzeltme ile sınanmalı.
7. ✅ **Zamansal sızıntı.** Eğitim 2016–2022 / test 2023–2024 zamansal bölümleme var.
8. ✅ **Dakika eşiği.** En az 10 maç ve 90 dakika filtresi var. 🟡 Ek öneri: per-40 değerlerde ampirik Bayes küçültme.
9. ⚠️ **Kesintili sezonlar.** 2019-20 COVID kesintisi tezde not edilmiş. 2020-21 seyircisiz sezon (ev sahibi avantajı) ve 2021-22 Rus kulüplerinin çekilmesi için duyarlılık analizi eklenmeli.
10. ⚠️ **H4 (Bayesgil güncelleme) yalnızca sentetik seri üzerinde pilot.** Makale B'de gerçek play-by-play üzerinde geriye dönük sınanmadan ana iddia yapılmamalı.
11. 🟠 **"Transfer yatırımı" çerçevesi.** Maliyet/maaş verisi yok; giriş cümlesi motivasyon olarak kalabilir ama bulgu iddiası olmamalı.

## 🟡 Minor
12. Ders kitabı atıfları (Hastie, Géron, McKinney) dergi makalesinde birincil metodolojik kaynaklarla desteklenmeli.
13. EuroLeague'de doğrudan önceki çalışma var: [@grassetti2020extended] (2018/19, Bayesgil RAPM, sezon içi güncelleme). "Avrupa Ligi'nde bütünleşik çalışma azdır" iddiası bu çalışmaya atıfla daraltılmalı.
14. ILP + arketip sinerjisi ile kadro kurma: [@muniz2022sports] (JORS) — en yakın yöneylem çalışması; fark (beşli/segment düzeyi vs. kadro düzeyi) açıkça yazılmalı.
