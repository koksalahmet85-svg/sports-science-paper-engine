# OPEN_QUESTIONS #2 — Başarılı formüllerde arketip dağılımı rastlantısal mı?

Veri: EuroLeague resmî API, E2016–E2024 (`engine/data/euroleague.py`, `engine/data/build_tables.py`).
Oyuncu-sezon örneklemi: 2014 (9 sezon) — tezle birebir aynı.
Yöntem: `manuscript/analysis/archetype_formulas.py`. Tezin formül seçim süreci (N ≥ 10, tek örneklem t, p < ,05) aynen uygulanır; ardından NRTG40 takım-sezon blokları içinde karıştırılarak süreç 1000 kez tekrarlanır.

| Segment modu | Dizilim-maç süresi | Dizilim-maç N | Test edilen formül | Anlamlı formül | Şansla beklenen anlamlı (perm. ort.) | p (anlamlı formül sayısı) | BH-FDR sonrası | χ² | p naif | p permütasyon | DKR payı | p (DKR) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Düzeltilmiş (başlangıç beşlileri kutu skorundan) | yok | 79,504 | 227 | 78 (0 pozitif) | 73.8 | 0.2178 | 46 | 49.39 | 6.2e-09 | 0.023 | 0.141 | 0.1848 |
| Düzeltilmiş (başlangıç beşlileri kutu skorundan) | ≥ 2 dk | 34,002 | 182 | 30 (28 pozitif) | 24.2 | 0.0629 | 2 | 7.31 | 0.29 | 0.4705 | 0.047 | 0.8511 |
| Tez EK-2.7 kodu (başlangıç beşlisi yok) | yok | 63,386 | 213 | 68 (1 pozitif) | 68.5 | 0.5834 | 43 | 35.79 | 3e-06 | 0.028 | 0.159 | 0.012 |
| Tez EK-2.7 kodu (başlangıç beşlisi yok) | ≥ 2 dk | 25,630 | 158 | 30 (30 pozitif) | 28.2 | 0.3586 | 6 | 6.55 | 0.36 | 0.3576 | 0.06 | 0.6993 |

## Okuma
- **Anlamlı formül sayısı hiçbir varyantta şansla beklenenin üzerinde değil** (permütasyon p sütunu). Yani "anlamlı formüller" kümesinin kendisi büyük ölçüde rastlantısal gürültüyle uyumlu.
- **Naif χ² ile permütasyon p'si arasındaki fark**, tezdeki χ² testinin bağımsızlık varsayımını (aynı formüldeki 5 gözlem, formül seçimi, çoklu test) ihlal ettiğini sayısal olarak gösterir.
- **Süre filtresi kritik.** Filtre yokken anlamlı formüllerin neredeyse tamamı negatif: kısa dizilimler kötü gittiği için oyundan alınır (ağırlıksız NRTG40 ort. -10.09, dakika ağırlıklı 0.55). ≥ 2 dk filtresiyle bu yapay etki kalkar ve arketip bileşimi şanstan ayrışmaz.
- **Filtresiz varyantta BH-FDR'den çok formülün geçmesi gerçek etki değildir:** ağırlıksız NRTG40'ın genel ortalaması sıfırdan uzak olduğu için H0: μ = 0 yanlış referanstır; permütasyon altında da benzer sayıda "anlamlı" formül çıkar.
- **DKR aşırı temsili** yalnızca tez EK-2.7 kodu + filtresiz varyantta permütasyon altında anlamlı; sağlam varyantlarda kaybolur.

## Sınırlılık: kümeler tezle aynı değil
Aynı 2.014 gözlem ve EK-2.5'teki 9 değişkenle K = 7 silhouette = 0.113 (tez: 0,089); küme boyutları {'OK': 277, 'ÇYF': 236, 'BAS': 261, 'YHS': 536, 'KŞ': 446, 'SDAK': 29, 'DKR': 229} (tez: {'OK': 456, 'ÇYF': 74, 'BAS': 237, 'YHS': 192, 'KŞ': 514, 'SDAK': 196, 'DKR': 345}). Arketipler tez Tablo 3 profillerine en yakın eşleşmeyle adlandırıldı. Kesin sonuç için tezin kendi arketip atamaları (`oyuncu_sezon_arketip.csv`) gerekir; betik o dosyayla çalıştırılabilir: `python manuscript/analysis/archetype_formulas.py --arketip-dosyasi oyuncu_sezon_arketip.csv`.
