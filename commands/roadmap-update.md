---
description: Yeni bulgu, feedback veya öncelik değişikliğine göre roadmap'i günceller
argument-hint: <ne değişti>
---

`roadmap-architect` skill'ini, özellikle `references/revision.md` bölümünü kullan.

Değişiklik: $ARGUMENTS

1. **Olguyu yaz** — planın nasıl değişeceğinden bağımsız olarak ne olduğunu kaydet.
2. **Düşen varsayımı bul** — `docs/roadmap.md` içindeki "Açık varsayımlar" tablosuna dön. Karşılığı yoksa varsayımı fark etmemişsindir, şimdi ekle.
3. **Etkiyi sınırla** — ilk "evet"te dur: faz içi sıralama mı? faz kapsamı mı? faz sırası mı? hedef mi? Çoğu değişiklik ilk ikisidir; hedefe sıçramak yaygın bir aşırı tepkidir.
4. **`plan.json`'ı güncelle** ve script'i yeniden çalıştır. Kritik yol değiştiyse bunu ayrıca duyur.
5. **Changelog'a yaz** — ne oldu / düşen varsayım / karar / etki / değerlendirilip seçilmeyen alternatifler.
6. **Çıktıları yeniden üret** — `docs/roadmap.md`, `docs/roadmap-deck.md`.

Faz veya iş iptal olduysa satırı silme; durumunu `İptal` / `Ertelendi` yap ve nedenini yaz.

Bitirince sohbette 3–5 satırlık değişim özeti ver: ne değişti, kritik yol nasıl etkilendi, kimin ne yapması gerekiyor. Kimse güncellenmiş sunumu baştan okumaz.
