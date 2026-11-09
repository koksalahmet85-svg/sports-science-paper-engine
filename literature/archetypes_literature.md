# Arketipler v2 — literatür desteği

Kaynak: Consensus taraması (2026-11-09), DOI'ler Crossref üzerinden doğrulandı ve `sspe-doi` ile eklendi.
Sayısal sonuçlar: `manuscript/analysis/archetypes_v2.py` → `results.json["archetypes_v2"]`.

## 1. Neden yeni arketipler?
- Tezin Ward K = 7 çözümü bootstrap altında kararsız (ortalama Jaccard < 0,5) ve küçük ön işleme farklarıyla
  değişiyor (`formula_test_report.md`, "Kümelerin yeniden üretimi").
- Rol sınıflaması literatürü heterojen: sistematik derleme, basketbolda bireysel oyun rollerinin yöntemsel
  farklılıklar nedeniyle çalışmadan çalışmaya değiştiğini ve tek tip, yüksek kaliteli bir yöntem gerektiğini
  vurguluyor [@ribes2026identifying]. Küme sayıları 3 [@pendolareinecke2025exploring] ile 19 [@wei2025enhancing]
  arasında değişiyor. → v2'de K, kararlılık ölçütüyle seçildi; bu doğrudan derlemenin çağrısına yanıt.

## 2. v2 rolleri ve literatürdeki karşılıkları

| v2 | Profil (sezon içi z) | Örnek oyuncular | Literatürdeki karşılığı |
|---|---|---|---|
| 1 — Boyalı Alan Koruyucusu (*paint protector*) | Düşük üçlük oranı, yüksek serbest atış oranı, blok, faul | Tavares, Poirier, Nebo | Derlemedeki yinelenen "paint protector" rolü [@ribes2026identifying] |
| 2 — Kenar Şutörü (*off-ball shooter*) | Yüksek üçlük oranı, düşük kullanım ve serbest atış oranı | Hezonja, Peters, Thompkins | "Shooter" [@ribes2026identifying]; "perimeter specialists" (Kadınlar EuroLeague) [@pendolareinecke2025exploring]; "Off-Ball Shooter" [@wei2025enhancing]; "Spot-up Wings" [@chen2023modeling] |
| 3 — Çok Yönlü Forvet (*versatile player*) | Dengeli; ribaund + blok + bir miktar dış şut | Mirotić, Vezenkov, Moneke | "Versatile player" [@ribes2026identifying]; "Versatile Big" [@wei2025enhancing] |
| 4 — Oyun Yöneticisi (*floor general*) | Yüksek kullanım, asist, top kaybı, kazanılan faul | Dončić, De Colo, Calathes, Shorts | "Floor general" [@ribes2026identifying]; "Core Ball Handler" [@wei2025enhancing] |

Not: [@wei2025enhancing], Core Ball Handler varlığının çoğu takım arkadaşının performansını artırdığını ve Off-Ball
Shooter performansının Ball Handler ve Versatile Big ile etkileşime bağlı olduğunu bildiriyor (CBA). Bu, v2 rolleriyle
dizilim düzeyinde sınanabilir bir hipotez verir (Makale A).

## 3. Yöntem seçimlerinin dayanağı
- **Pozisyonların istatistiksel olarak ayrışması, ama örtüşmesi:** Kutu skoru istatistikleri geleneksel pozisyonları
  ayırt eder [@sampaio2006discriminant], ancak işlevsel örtüşme yüksektir ve veri temelli roller daha bilgilendiricidir
  [@ibanez2025redefining].
- **Yumuşak üyelik (GMM):** Oyuncuların birden çok role kısmi aidiyeti — NBA'de GMM ile yumuşak atama [@kalman2020lineup];
  kadın basketbolunda k-means ve GMM ile kararlı işlevsel roller [@ibanez2025redefining]. Uygulama/model seçimi için
  [@scrucca2016mclust].
- **K seçimi ve geçerlik indeksleri:** Küme geçerlik indeksleriyle K seçimi [@duman2021cluster]; bootstrap Jaccard
  kararlılığı [@hennig2007cluster].
- **Arketip ≠ kalite:** v2'de verimlilik değişkenleri (eFG, 3P%, FT%, VAL40) kümelemeye girmez; rol ile oyuncu değeri
  ayrı tutulur. Böylece ILP'de arketip kısıtı ile VAL40 amaç fonksiyonu aynı bilgiyi iki kez saymaz.

## 4. Doğrulanamayan / eklenmeyen kaynak
- Bianchi, Facchinetti ve Zuccolotto (2017), "Role revolution: towards a new meaning of positions in basketball",
  *Electronic Journal of Applied Statistical Analysis* — SOM + bulanık kümeleme ile 5 rol. Crossref'te kaydı bulunamadı;
  DOI dergi sitesinden elle doğrulanmadan `references.bib`'e eklenmemeli.
