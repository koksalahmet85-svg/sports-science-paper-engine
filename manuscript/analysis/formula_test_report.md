# OPEN_QUESTIONS #2 — Başarılı formüllerde arketip dağılımı rastlantısal mı?

Veri: EuroLeague resmî API, E2016–E2024 (`engine/data/euroleague.py`, `engine/data/build_tables.py`).
Oyuncu-sezon örneklemi: 2014 (9 sezon) — tezle birebir aynı.
Yöntem: `manuscript/analysis/archetype_formulas.py`. Tezin formül seçim süreci (N ≥ 10, tek örneklem t, p < ,05) aynen uygulanır; ardından NRTG40 takım-sezon blokları içinde karıştırılarak süreç 1000 kez tekrarlanır.


## A. Tezin kendi arketipleriyle (birebir yeniden üretim: `thesis_archetypes.py`) — ana sonuç

| Segment modu | Dizilim-maç süresi | Dizilim-maç N | Test edilen formül | Anlamlı formül | Şansla beklenen anlamlı (perm. ort.) | p (anlamlı formül sayısı) | BH-FDR sonrası | χ² | p naif | p permütasyon | DKR payı | p (DKR) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Düzeltilmiş (başlangıç beşlileri kutu skorundan) | yok | 79,401 | 255 | 92 (2 pozitif) | 80.3 | 0.007 | 56 | 42.31 | 1.6e-07 | 0.002 | 0.193 | 0.036 |
| Düzeltilmiş (başlangıç beşlileri kutu skorundan) | ≥ 2 dk | 33,971 | 225 | 28 (23 pozitif) | 26.3 | 0.3666 | 4 | 8.85 | 0.18 | 0.2318 | 0.136 | 0.1678 |
| Tez EK-2.7 kodu (başlangıç beşlisi yok) | yok | 63,297 | 244 | 88 (2 pozitif) | 74.4 | 0.008 | 48 | 45.8 | 3.3e-08 | 0.001 | 0.209 | 0.005 |
| Tez EK-2.7 kodu (başlangıç beşlisi yok) | ≥ 2 dk | 25,602 | 211 | 34 (30 pozitif) | 32.0 | 0.3447 | 5 | 3.2 | 0.78 | 0.7922 | 0.112 | 0.4505 |

## B. Yaklaşık arketiplerle (tez EK-2.5 basılı kodu) — duyarlılık

| Segment modu | Dizilim-maç süresi | Dizilim-maç N | Test edilen formül | Anlamlı formül | Şansla beklenen anlamlı (perm. ort.) | p (anlamlı formül sayısı) | BH-FDR sonrası | χ² | p naif | p permütasyon | DKR payı | p (DKR) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Düzeltilmiş (başlangıç beşlileri kutu skorundan) | yok | 79,504 | 227 | 78 (0 pozitif) | 73.8 | 0.2178 | 46 | 49.39 | 6.2e-09 | 0.023 | 0.141 | 0.1848 |
| Düzeltilmiş (başlangıç beşlileri kutu skorundan) | ≥ 2 dk | 34,002 | 182 | 30 (28 pozitif) | 24.2 | 0.0629 | 2 | 7.31 | 0.29 | 0.4705 | 0.047 | 0.8511 |
| Tez EK-2.7 kodu (başlangıç beşlisi yok) | yok | 63,386 | 213 | 68 (1 pozitif) | 68.5 | 0.5834 | 43 | 35.79 | 3e-06 | 0.028 | 0.159 | 0.012 |
| Tez EK-2.7 kodu (başlangıç beşlisi yok) | ≥ 2 dk | 25,630 | 158 | 30 (30 pozitif) | 28.2 | 0.3586 | 6 | 6.55 | 0.36 | 0.3576 | 0.06 | 0.6993 |

## Okuma
- **Anlamlı formül sayısı, kısa dizilim yanlılığı giderildiğinde (≥ 2 dk) şansla beklenenin üzerinde değil** (permütasyon p sütunu). Filtresiz varyantta fazlalık var, ancak o formüllerin neredeyse tamamı negatif.
- **Naif χ² ile permütasyon p'si arasındaki fark**, tezdeki χ² testinin bağımsızlık varsayımını (aynı formüldeki 5 gözlem, formül seçimi, çoklu test) ihlal ettiğini sayısal olarak gösterir.
- **Süre filtresi kritik.** Filtre yokken anlamlı formüllerin neredeyse tamamı negatif: kısa dizilimler kötü gittiği için oyundan alınır (ağırlıksız NRTG40 ort. -10.09, dakika ağırlıklı 0.55). ≥ 2 dk filtresiyle bu yapay etki kalkar ve arketip bileşimi şanstan ayrışmaz.
- **Filtresiz varyantta BH-FDR'den çok formülün geçmesi gerçek etki değildir:** ağırlıksız NRTG40'ın genel ortalaması sıfırdan uzak olduğu için H0: μ = 0 yanlış referanstır; permütasyon altında da benzer sayıda "anlamlı" formül çıkar.
- **DKR aşırı temsili (tablo A):** filtresiz varyantta permütasyon altında da anlamlı, ancak anlamlı formüllerin neredeyse tamamı NEGATİF. Yani DKR, başarılı değil kısa süre sahada kalıp kaybeden dizilimlerde fazla. ≥ 2 dk filtresiyle (anlamlı formüllerin çoğu pozitif) arketip bileşimi şanstan ayrışmıyor. Tezdeki "başarılı formüllerde DKR aşırı temsili" bulgusu bu veriyle desteklenmiyor.

## Kümelerin yeniden üretimi
Tezin gerçek kodu (EK KOD 1–2) ile tez arketipleri birebir üretildi (K1–K7 = 456, 74, 237, 192, 514, 196, 345; silhouette 0,089). Basılı EK-2.5 kodu ise farklı bir çözüm veriyor (silhouette 0.113, boyutlar {'OK': 277, 'ÇYF': 236, 'BAS': 261, 'YHS': 536, 'KŞ': 446, 'SDAK': 29, 'DKR': 229}): USG tanımı (maç başına / 40 dk), 0/0 oranların doldurulması (ortalama / 0) ve satır sırası gibi küçük farklar küme yapısını değiştiriyor. Bu, Ward K = 7 çözümünün kararsızlığının bir başka göstergesi (bkz. `archetypes_v2.py` bootstrap Jaccard).
