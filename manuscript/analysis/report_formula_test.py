"""results.json → formula_test_report.md (OPEN_QUESTIONS #2 raporu; sayılar elle yazılmaz)."""

import json
from pathlib import Path

HERE = Path(__file__).parent
R = json.loads((HERE / "results.json").read_text())
VARIANTS = [("corrected", 0), ("corrected", 2), ("thesis", 0), ("thesis", 2)]
LABEL = {"corrected": "Düzeltilmiş (başlangıç beşlileri kutu skorundan)", "thesis": "Tez EK-2.7 kodu (başlangıç beşlisi yok)"}


def row(mode, m):
    d = R[f"formula_test_{mode}_min{m:g}"]
    p = d["permutasyon"]
    return (f"| {LABEL[mode]} | {'yok' if m == 0 else f'≥ {m:g} dk'} | {d['dizilim_mac_N']:,} | "
            f"{d['test_edilen_formul']} | {d['anlamli_formul']} ({d['anlamli_formul_pozitif']} pozitif) | "
            f"{p['null_anlamli_formul_ort']} | {p['anlamli_formul_sayisi_p']} | {d['bh_fdr_sonrasi_kalan']} | "
            f"{d['chi2']} | {d['chi2_p_naif']:.2g} | {p['chi2_p']} | {d['DKR_payi']} | {p['DKR_payi_p']} |")


main = R["formula_test_corrected_min0"]
cl = main["kumeleme"]
lines = [
    "# OPEN_QUESTIONS #2 — Başarılı formüllerde arketip dağılımı rastlantısal mı?",
    "",
    "Veri: EuroLeague resmî API, E2016–E2024 (`engine/data/euroleague.py`, `engine/data/build_tables.py`).",
    f"Oyuncu-sezon örneklemi: {R['n']} ({R['n_sezon']} sezon) — tezle birebir aynı.",
    "Yöntem: `manuscript/analysis/archetype_formulas.py`. Tezin formül seçim süreci (N ≥ 10, tek örneklem t, p < ,05) "
    f"aynen uygulanır; ardından NRTG40 takım-sezon blokları içinde karıştırılarak süreç {main['permutasyon']['B']} kez tekrarlanır.",
    "",
    "| Segment modu | Dizilim-maç süresi | Dizilim-maç N | Test edilen formül | Anlamlı formül | Şansla beklenen anlamlı (perm. ort.) "
    "| p (anlamlı formül sayısı) | BH-FDR sonrası | χ² | p naif | p permütasyon | DKR payı | p (DKR) |",
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    *[row(mo, m) for mo, m in VARIANTS],
    "",
    "## Okuma",
    "- **Anlamlı formül sayısı hiçbir varyantta şansla beklenenin üzerinde değil** (permütasyon p sütunu). "
    "Yani \"anlamlı formüller\" kümesinin kendisi büyük ölçüde rastlantısal gürültüyle uyumlu.",
    "- **Naif χ² ile permütasyon p'si arasındaki fark**, tezdeki χ² testinin bağımsızlık varsayımını (aynı formüldeki "
    "5 gözlem, formül seçimi, çoklu test) ihlal ettiğini sayısal olarak gösterir.",
    "- **Süre filtresi kritik.** Filtre yokken anlamlı formüllerin neredeyse tamamı negatif: kısa dizilimler kötü "
    f"gittiği için oyundan alınır (ağırlıksız NRTG40 ort. {main['NRTG40_ort_agirliksiz']}, dakika ağırlıklı "
    f"{main['NRTG40_ort_dakika_agirlikli']}). ≥ 2 dk filtresiyle bu yapay etki kalkar ve arketip bileşimi şanstan ayrışmaz.",
    "- **Filtresiz varyantta BH-FDR'den çok formülün geçmesi gerçek etki değildir:** ağırlıksız NRTG40'ın genel ortalaması "
    "sıfırdan uzak olduğu için H0: μ = 0 yanlış referanstır; permütasyon altında da benzer sayıda \"anlamlı\" formül çıkar.",
    "- **DKR aşırı temsili** yalnızca tez EK-2.7 kodu + filtresiz varyantta permütasyon altında anlamlı; sağlam varyantlarda kaybolur.",
    "",
    "## Sınırlılık: kümeler tezle aynı değil",
    f"Aynı 2.014 gözlem ve EK-2.5'teki 9 değişkenle K = 7 silhouette = {cl['silhouette_K7']} (tez: 0,089); küme boyutları "
    f"{cl['boyutlar']} (tez: {cl['tez_boyutlar']}). Arketipler tez Tablo 3 profillerine en yakın eşleşmeyle adlandırıldı. "
    "Kesin sonuç için tezin kendi arketip atamaları (`oyuncu_sezon_arketip.csv`) gerekir; betik o dosyayla çalıştırılabilir: `python manuscript/analysis/archetype_formulas.py --arketip-dosyasi oyuncu_sezon_arketip.csv`.",
]
(HERE / "formula_test_report.md").write_text("\n".join(lines) + "\n")
print("→ manuscript/analysis/formula_test_report.md")
