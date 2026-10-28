---
description: Yazar → hakem döngüsünü Q1 eşiğine ulaşana kadar (en fazla 4 tur) çalıştırır
argument-hint: "[bölüm adı veya 'all']"
---
Hedef bölüm: $ARGUMENTS (boşsa tüm makale).

Her tur için:
1. `q1-reviewer` alt ajanını çağır → `manuscript/reviews/round-N.md`.
2. Karar "Accept" ise dur ve özet ver.
3. Kritik sorunları sınıflandır: yöntem → `methodologist`, analiz/sayı → `data-analyst`, kaynak eksikliği → `literature-scout`. İlgili ajanlara yalnızca kendi maddelerini ver.
4. Düzeltmelerden sonra `make analysis render` çalıştır; hata varsa düzelt.
5. Bir sonraki tura geç. 4 turda Accept gelmezse kalan sorunları `manuscript/OPEN_QUESTIONS.md`'ye yaz ve bana raporla.

Hiçbir turda references.bib'de olmayan bir kaynağa atıf eklenmez; elle yazılmış sayı eklenmez.
