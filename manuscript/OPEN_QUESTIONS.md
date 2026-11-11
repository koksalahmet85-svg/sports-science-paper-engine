# Açık sorular — Q1 hakem riski haritası (tez metnine göre güncellendi)

Kaynak: tez tam metni (Ege Üniv., 2026, "Avrupa Ligi Basketbol Takımlarının Diziliş Rotasyonlarının Yapay Zeka Tabanlı Analizi") + Consensus taraması (`literature/consensus_report.md`).
Durum: ✅ tezde karşılanmış · ⚠️ kısmen · ❌ açık. Öncelik: 🔴 reddettirebilir · 🟠 major · 🟡 minor.

## 🔴 Kritik (makaleye taşınmadan önce çözülmeli)

1. ⚠️ **VAL40 + GBR döngüselliği.** Tez bunu açıkça kabul ediyor: öznitelikler VAL40'ın aritmetik bileşenlerini içeriyor; R² = 0,949 "tahmin değil açıklayıcı ayrıştırma" olarak yorumlanıyor. Şeffaflık iyi, ama Q1 hakem "o zaman GBR aşaması neden var?" diye soracak.
   **Öneri (birini seç):** (a) Makale A'dan GBR'yi çıkar, VAL40'ı doğrudan kullan; (b) GBR'yi **ileriye dönük** kur: t sezonunun özniteliklerinden t+1 sezonunun VAL40'ını tahmin et — bu gerçek bir tahmin görevi olur ve ILP'ye girdi olarak savunulabilir.

2. 🔬 **Ki-kare / "rastlantısal değil" iddiası — tezin kendi arketipleriyle (birebir) ve EuroLeague API verisiyle yeniden sınandı.** DKR fazlalığı yalnızca kısa süreli KAYBEDEN dizilimlerde; ≥ 2 dk filtresiyle bileşim şanstan ayrışmıyor (rapor: `manuscript/analysis/formula_test_report.md`).
   - Tezin formül seçim süreci aynen uygulanıp permütasyonla (takım-sezon blokları, B = 1000) sınandığında **anlamlı formül sayısı hiçbir varyantta şansla beklenenin üzerinde değil**.
   - Naif χ² küçük p verirken permütasyon p'si büyüyor: tezdeki χ² bağımsızlık varsayımını ihlal ediyor.
   - ≥ 2 dk dizilim-maç filtresiyle (kısa dizilimlerin "kötü gidince oyundan alınma" yanlılığı giderilince) arketip bileşimi şanstan ayrışmıyor; DKR aşırı temsili kayboluyor.
   - **Sınırlılık:** EK-2.5 koduyla elde edilen kümeler tezdekiyle aynı değil (bkz. #16). Kesin sonuç için tezin arketip atama dosyası gerekli.
   - **Makale için öneri:** "Başarılı formüllerde arketip dağılımı rastlantısal değildir" iddiası bu haliyle makaleye taşınmamalı. Yerine dakika/hücum ağırlıklı, rakibe göre düzeltilmiş dizilim modeli (RAPM tipi) ile arketip etkisi sınanmalı.

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

## Tez metni ile EuroLeague API replikasyonu arasında bulunan yeni sorular (2026-11-04)
16. ✅ **Çözüldü (2026-11-09):** Tezin gerçek kodu (Drive: ek_kod_1–2) ile kümeler birebir üretildi (`manuscript/analysis/thesis_archetypes.py`). Fark: USG maç başına, 0/0 oranlar ortalamayla dolduruluyor, toplulaştırma oyuncu adını da içeriyor — basılı tez metni ve EK-2.5 bunları farklı anlatıyor; makalede gerçek kod esas alınmalı. Eski not: **Kümeler ekteki kodla yeniden üretilemiyor.** Aynı 2.014 oyuncu-sezon ve EK-2.5'teki 9 değişkenle K = 7 silhouette 0,113 (tez 0,089), K = 6'da 0,132 (tez 0,115); küme boyutları farklı. **Soru:** Kümelemede ek bir ön işleme (ör. aykırı değer kırpma, farklı USG tanımı — Tablo 3 notunda USG "maç başına", kodda "40 dakikaya") kullanıldı mı?
17. ✅ **Doğrulandı:** gerçek kod (ek_kod_5) maç-takım gözlemi üretiyor (5.289). Bu bir dizilim birimi değil; makalede birim yeniden tanımlanmalı. Eski not: **"5.292 kadro dizilimi-maç gözlemi" = 2 × 2.646.** Bu, takım başına maç başına tam olarak bir dizilim demek; dizilim-maç tanımı (ör. yalnızca ilk beşler mi, en çok süre alan beşli mi?) netleşmeli.
18. ✅ **Doğrulandı:** gerçek kod (ek_kod_5) başlangıç beşlilerini kutu skorundan alıyor; yalnızca tezin ekindeki basılı kod hatalı. Eki gerçek kodla değiştir. Eski not: **EK-2.7'deki kod başlangıç beşlilerini eklemiyor** (BP olayı oyuncu içermez; ilk beşler yalnızca kutu skorundaki IsStarter alanında). Tezdeki 67.001 segment sayısı bu kodun ürettiğinden (60.592) fazla, düzeltilmiş motorun ürettiğinden (80.460) az; gerçekte çalışan kod ekten farklı olmalı. Ek, çalışan kodla değiştirilmeli.
19. 🟠 **EK-2.7'de `pts_diff=("pts_a","sum")`** yalnızca atılan sayıyı topluyor, skor farkını değil (pts_a − pts_b olmalı). Tezdeki analizde hangisinin kullanıldığı doğrulanmalı.
20. 🟠 **NRTG tanımı tutarsız:** kısaltmalar listesinde "100 hücum başına", kodda 40 dakika başına (NRTG40). Ayrıca ağırlıksız ortalama kısa dizilimlerde ciddi negatif yanlılık üretiyor (rapordaki ağırlıksız vs dakika ağırlıklı ortalama).

21. 🆕 **Arketipler v2** (`manuscript/analysis/archetypes_v2.py`, literatür: `literature/archetypes_literature.md`): rol değişkenleri + sezon içi z; yalnızca GMM K = 4 kararlı (ortalama Jaccard ≈ 0,77; Ward hiçbir K'da > 0,55 değil). Karar: Makale A'da v2 rolleri mi, tez arketipleri mi kullanılacak? (Öneri: v2; tez arketipleri duyarlılık analizi.) Şut profiliyle iki düzeyli yapı: 4 ana rol (doğrulayıcı) → 6 alt rol (keşifsel; `archetypes_hier.py`).
22. 🔴 **VAL40 rol yanlılığı → ILP.** Rol, VAL40 varyansının ~%24'ünü, On−Off etkisinin ~%1'ini açıklıyor (`role_value_summary.py`). VAL40'ı maksimize eden ILP yapısal olarak uzun oyuncuları seçer. Makale B'de amaç fonksiyonu rol içi z-VAL40 veya etki tabanlı değerle (L-RAPM vb.) yeniden kurulmalı; ham VAL40 duyarlılık analizi olarak kalabilir.
23. 🆕 **Nihai rol çözümü adayı: 5 rol** (`archetypes_v2.py --features full`; ileri istatistik + şut profili + boy + asist ağı). K = 5 kararlılığı K = 4 ile eşit (≈ 0,71), dönemler arası uyumu daha yüksek. Karar: ana analiz K = 5, duyarlılık K = 4 (öneri).
