# STROBE kontrol listesi (gözlemsel çalışmalar) — Makale A ve Makale B

Kaynak: STROBE Statement, 22 madde. "Bölüm" sütunu metindeki yeri gösterir; "–" uygulanamaz.

| # | Madde | Makale A | Makale B |
|---|---|---|---|
| 1 | Başlık ve özet: tasarım belirtilmiş, yapılandırılmış özet | Başlık, Özet | Başlık, Özet |
| 2 | Arka plan / gerekçe | Giriş ¶1–2 | Giriş ¶1–2 |
| 3 | Amaçlar / hipotezler | Giriş ¶3 | Giriş ¶3 |
| 4 | Çalışma tasarımı | Yöntem: Design and data (retrospektif gözlemsel) | Yöntem: Data |
| 5 | Ortam: yer, dönem, veri toplama | Yöntem: Design and data (EuroLeague 2016–17 → 2024–25, resmî API) | Yöntem: Data |
| 6 | Katılımcılar: dahil etme ölçütleri | Yöntem: ≥ 10 maç, ≥ 90 dk; model için ≥ 400 dk | Yöntem: ≥ 400 kariyer dakikası; ILP için ≥ 100 dk |
| 7 | Değişkenler: sonuç, maruziyet, karıştırıcılar | Yöntem: Role variables; Roles and lineup performance (net rating; RAPM kontrolü) | Yöntem: Player value measures; Within-season validity (rakip RAPM, ev sahipliği) |
| 8 | Veri kaynakları / ölçüm | Yöntem: segment kurulumu, hücum tahmini | Yöntem: Data, PIR tanımı |
| 9 | Yanlılık | Oyuncu düzeyi bootstrap; sonuçtan bağımsız rol değişkenleri; zamansal doğrulama | Zamansal ve sezon içi doğrulama; antrenör tabanı |
| 10 | Örneklem büyüklüğü | Tüm maçlar (nüfus); geçerli güç simülasyonu (çift artışı, eğitim maçları yeniden örneklenir) — güç düşük, Sınırlılıklar'da | Tüm maçlar; bootstrap GA; GA genişliği raporlandı |
| 11 | Nicel değişkenlerin işlenmesi | Sezon içi z, karekök dönüşümü | 40 dakikaya ölçekleme, takım içi z |
| 12 | İstatistiksel yöntemler, eksik veri, duyarlılık | Yöntem: GMM/BIC, Jaccard, ARI, ridge, permütasyon, duyarlılık; eksik değer yok (tahmin örneklemi) | Yöntem: η² + bootstrap, R² + maç bootstrap, eğim + takım-sezon bootstrap |
| 13 | Katılımcı akışı | Yöntem: oyuncu-maç → 2.014 oyuncu-sezon → 1.286 (kestirim); segment: tümü → eksiksiz 5'e 5 → ≥ 1 hücum (eğitim/test N'leri) | Yöntem: 519 oyuncu (≥ 400 dk), 485 (güvenirlik), 481 (2SLS); segment: test N, takım-segment gözlemleri |
| 14 | Betimsel veriler | Tablo 2 | Tablo 1 |
| 15 | Sonuç verileri | Bulgular | Bulgular |
| 16 | Ana sonuçlar: kestirim + GA | Cramér V GA, permütasyon p, çift artışı GA, güç | η² ve kısmi η² GA, rol farkı GA (RAPM sabit, 2SLS), R² farkı GA, eğim GA, doğrudan ILP–antrenör farkı GA |
| 17 | Diğer analizler | Değişken seti duyarlılığı (Tablo 2), 5 rol, tez çözümü, sızıntı denetimleri, rol-kombinasyonu testleri | λ duyarlılığı, PIR bileşensiz roller (iki sürüm), ortak alt küme, kısıt varyantları |
| 18 | Ana bulguların özeti | Tartışma ¶1 | Tartışma ¶1 |
| 19 | Sınırlılıklar | Limitations | Limitations |
| 20 | Yorum | Tartışma ¶2–4 | Tartışma ¶2–4 |
| 21 | Genellenebilirlik | Limitations (EuroLeague'e özgü) | Limitations |
| 22 | Finansman | ❓ yazar dolduracak | ❓ yazar dolduracak |


**Yazılım (her iki makale):** Python; paket sürümleri, rastgele tohum ve git commit'i `results.json["provenance"]` içinde (`provenance.py`). GMM: scikit-learn, n_init = 5, reg_covar = 1e-4. ILP: scipy.optimize.milp.
