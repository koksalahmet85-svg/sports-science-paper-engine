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

## 5. Ek istatistiklerle ikinci düzey: 4 ana rol → 6 alt rol (2026-11-09)
Şut koordinatları (pota mesafesi, köşe üçlüğü), hızlı hücum / ikinci şans payı ve asistli isabet payı eklendi
(`engine/data/shot_profile.py`; 325.151 saha içi atış). Sonuçlar (`archetypes_v2.py`, bootstrap Jaccard):
- Tek düzeyde K artırıldığında kararlılık yine düşüyor (GMM K = 4 ≈ 0,73; K = 5 ≈ 0,62; K = 7 ≈ 0,51) — ek
  istatistikler 7 düz kümeyi kararlı hale getirmiyor.
- İç içe (ana rol içinde) bölünmede iki anlamlı alt rol çıkıyor (`archetypes_hier.py`):

| Ana rol | Alt rol | Profil | Örnek | Kararlılık | Literatür |
|---|---|---|---|---|---|
| Çok Yönlü Forvet | İç Saha Forveti | Yüksek kullanım, boyalı alan/pota şutu, hücum ribaundu, serbest atış | Mirotić, Shengelia, Clyburn | ≈ 0,77 (kararlı) | "Bigs who Cut to the Rim" [@chen2023modeling]; "Versatile Big" [@wei2025enhancing] |
| Çok Yönlü Forvet | Stretch Forvet | Köşe üçlüğü, asistli isabet, düşük top kaybı | Vezenkov, Leday, Hernangómez | ≈ 0,77 (kararlı) | "Spot-up Wings" [@chen2023modeling] |
| Oyun Yöneticisi | Organizatör Oyun Kurucu | Önce pas, daha düşük kullanım | Calathes, Satoranský, Walkup | ≈ 0,70 (sınırda) | "Core Ball Handler" [@wei2025enhancing] |
| Oyun Yöneticisi | Yaratıcı Skorer | Çok yüksek kullanım, asistsiz şut, orta mesafe, kazanılan faul | Larkin, Mike James, Mičić | ≈ 0,70 (sınırda) | "Ball Dominant Scorer" [@wei2025enhancing] |

Not: [@wei2025enhancing] (CBA) Core Ball Handler'ın takım arkadaşlarının çoğunun performansını artırdığını, Ball Dominant
Scorer'ın ise diğer rollere olumsuz etkisini bildiriyor — EuroLeague'de bu iki alt rolün dizilim etkisi sınanabilir
bir hipotez. Öneri: doğrulayıcı analizler 4 ana rolle, betimsel/keşifsel analizler 6 alt rolle.

## 6. İleri istatistiklerle doğrulama (2026-11-10)
`engine/data/advanced.py`: USG%, AST%, ORB%, DRB%, STL%, BLK%, TOV%, 3PAr, FTr, FD%, PF% — paydalar, play-by-play'den
kurulan beşlilerde oyuncu sahadayken GERÇEK takım/rakip toplamları (Basketball-Reference'ın sezon toplamı tahmini yerine).
Doğrulama: PBP sayımları kutu skoruyla %97–99,8 birebir; sahada dakika / kutu dakikası medyanı 0,998.
- Üç bağımsız değişken setinde (kutu skoru, şut profili, ileri istatistik) kararlı çözüm aynı: GMM K = 4
  (Jaccard ≈ 0,73–0,77); K ≥ 5'te kararlılık düşüyor. Rol yapısı değişken seçimine dayanıklı.
- Temel ve ileri K = 4 çözümleri aynı dört rolü eşliyor (çapraz tablo), ama sınırdaki oyuncuların ~%25'i rol
  değiştiriyor (ARI ≈ 0,49).
- İleri istatistiklerle hiçbir alt rol kararlılık eşiğini geçmiyor; Çok Yönlü Forvet bölünmesi en yakın (≈ 0,72).

**VAL40'ın rol yanlılığı** (`role_value_summary.py`, results.json["role_value"]): rol, VAL40 varyansının ~%24'ünü,
sahadaki etkinin (On−Off net rating) ise yalnızca ~%1'ini açıklıyor. Kutu skoru bileşik endeksleri uzun oyuncuları
(ribaund, blok, yüksek isabet) sistematik olarak öne çıkarıyor. → ILP'nin amaç fonksiyonunda ham VAL40 yerine rol içi
standartlaştırılmış değer ya da etki tabanlı (RAPM tipi) değer kullanılmalı.
