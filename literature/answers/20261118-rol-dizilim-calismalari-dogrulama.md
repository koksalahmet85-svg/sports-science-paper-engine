# Tartışmadaki karşılaştırmaların tam metin doğrulaması (Makale A)

Not: CLAUDE.md kural 4 `sspe-ask` (paper-qa) çıktısı ister; bu ortamda API anahtarı olmadığı için doğrulama tam metinden
elle yapıldı. Kaynak ve kapsam her satırda belirtildi.

| Kaynak | Erişim | Rol → başarı bağlantısı | Bireysel kalite kontrolü | Örneklem dışı doğrulama |
|---|---|---|---|---|
| [@kalman2020lineup] | Tam metin (yazarın Drive'ı) | Sezon toplamı 5'li dizilimler (14.234); çıktı: takım net rating'ine doğru büzülmüş (empirical Bayes) dizilim net rating'i; öngörücüler: 9 GMM kümesine yumuşak üyelik toplamları; OLS ve rastgele orman | Yok. Yalnızca 9 küme toplamı; PER yalnızca kümeleme girdisi; rakip gücü yok | Yok; 2019-20 testi gelecek çalışmaya bırakılmış |
| [@chen2023modeling] | Tam metin (Frontiers, açık erişim) | Takım düzeyi: yarı finale kalma (ikili) ~ rol kümeleri, lojistik regresyon (OR) | Yok; yazarlar sınırlılıkta "players' playing time and efficiency values ... not considered" diyor | Raporlanmamış |
| [@penner2025player] | Tam metin (Frontiers, açık erişim) | Arketip oranları, artı-eksi ≥ 15 olan oyunculardan türetilmiş; başarı testi yok | Sonuca göre seçim (artı-eksi filtresi); istatistiksel kontrol yok | Raporlanmamış; kararlılık için Jaccard %11,89 ("low similarity") |
| [@wei2025enhancing] | Yalnızca özet (tam metin bu ortamdan erişilemedi) | Mükemmel hücum / savunma / net rating dizilimlerinde roller arası ağ analizi (22.661 dizilim) | Özetten belirlenemiyor — metinde iddia edilmemeli | Özetten belirlenemiyor |

## Özetten doğrulanan diğer iddialar
- [@ribes2026identifying]: "Seven recurrent IPRs emerged: paint protector, shooter, role player, floor general, defensive player, versatile player, and explosive player"; farkların yöntem heterojenliğinden kaynaklandığı ve tek tip yöntem gerektiği (özet, Consensus/Crossref).
- [@pendolareinecke2025exploring]: Kadınlar EuroLeague, 3 ana rol (özet). [@ibanez2025redefining]: 9 kararlı rol, k-means + GMM (özet).
- [@grassetti2020extended]: 2018/19 EuroLeague, düzenlileştirilmiş adjusted plus-minus ile dizilim yönetimi (özet); rol analizi yok.
- [@hennig2007cluster]: bootstrap Jaccard; ≥ 0,75 kararlı, ≤ 0,5 dağılmış eşikleri bu makaleden.
