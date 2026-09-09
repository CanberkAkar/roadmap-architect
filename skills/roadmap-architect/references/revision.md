# Güncelleme: roadmap'i yaşayan tutmak

Roadmap sabit bir plan değil, planlama aracıdır. Ama "yaşayan" olmak keyfi olmak demek değil — güncellemenin de bir protokolü var, yoksa roadmap güvenilirliğini kaybeder.

## Ne zaman güncellenir

**Takvimsel:** her sprint sonunda kısa gözden geçirme, her faz sonunda tam gözden geçirme.

**Tetikleyici olayla:** takvimi bekleme, şu durumlarda hemen güncelle:

- Bir spike/doğrulama işi sonuçlandı — karar noktası tetiklendi
- Bir varsayım yanlış çıktı
- Business önceliği değişti (yeni müşteri, rakip hamlesi, regülasyon)
- Bir dependency kaydı veya düştü
- Bir işin gerçekleşen effort'u tahminin 1.5 katını aştı — bu tekil bir sapma değil, tahmin modelinin sinyalidir

## Protokol

### 1. Neyin değiştiğini yaz, planı değil
Önce olguyu kaydet: "Sağlayıcı sandbox'ta 3DS desteklemiyor, canlıda destekliyor." Bu, planın nasıl değişeceğinden bağımsız bir gerçektir ve altı ay sonra kararın nedenini açıklayan tek kayıt olacaktır.

### 2. Hangi varsayımın düştüğünü belirle
Discovery'deki "Açık varsayımlar" listesine dön. Değişimin hangi maddeye dokunduğunu bul. Listede karşılığı yoksa, o varsayımı fark etmemişsindir — şimdi ekle.

### 3. Etkiyi sınırla
Sırayla sor, ilk "evet"te dur:

1. Sadece faz içi sıralama mı değişiyor? → sprint planını güncelle, roadmap'e dokunma
2. Bir fazın kapsamı mı değişiyor? → fazı güncelle, effort'u yeniden tahmin et
3. Faz sırası mı değişiyor? → dependency grafiğini güncelle, script'i tekrar çalıştır
4. Hedef veya başarı kriteri mi değişti? → discovery'ye dön, roadmap'i yeniden türet

Çoğu değişiklik 1 veya 2'dir. 4'e sıçramak yaygın bir aşırı tepkidir; gerçekten hedef değiştiyse yap, yoksa yapma.

### 4. `plan.json`'ı güncelle ve yeniden hesapla
Sayıları elle düzeltme. `plan.json`'ı düzelt, script'i çalıştır, kritik yol ve agent önerisinin nasıl değiştiğine bak. Kritik yol değiştiyse bunu ayrıca duyur — çoğu gecikme oradan gelir.

### 5. Changelog'a yaz
`docs/roadmap.md` sonundaki changelog bölümüne ekle:

```markdown
## Changelog

### 2026-03-14 · Faz 2 kapsam değişikliği
**Ne oldu:** Ödeme sağlayıcı sandbox'ta 3DS desteklemiyor (spike T12 sonucu)
**Düşen varsayım:** "Sağlayıcı entegrasyonu sandbox'ta tam doğrulanabilir"
**Karar:** Faz 2'ye sınırlı canlı test ortamı eklendi
**Etki:** Faz 2 +4 gün · kritik yol 38 → 42 gün · Faz 3 bir sprint kaydı
**Alternatifler:** Sağlayıcı değişimi (+20 gün, reddedildi) · 3DS'siz çıkma (uyum riski, reddedildi)
```

Alternatifler satırını atlama. Bir kararın nedeni, seçilmeyenler yazılmadan tam anlaşılmaz.

## Fazı silme, durumunu değiştir

Bir faz veya iş artık yapılmayacaksa satırı silme. Durumunu işaretle: `İptal`, `Ertelendi`, `Kapsam dışı`. Nedenini bir cümleyle yaz. Silinen satır, üç ay sonra "bunu neden yapmıyoruz?" sorusuna cevap veremez ve iş sessizce geri gelir.

Durum değerleri: `Planlandı` · `Devam ediyor` · `Tamamlandı` · `Bloke` · `Ertelendi` · `İptal`

## Tahmin kalibrasyonu

Her faz sonunda tahmin vs. gerçekleşen oranını hesapla ve kalan fazlara uygula:

```
kalibrasyon = gerçekleşen_toplam / tahmin_toplam
```

1.3 çıktıysa kalan tahminler de muhtemelen %30 düşüktür. Bunu görmezden gelip her fazda aynı sürprizle karşılaşmak yaygın bir hatadır. `focus_factor`'ı buna göre güncelle ve düzeltmeyi changelog'a yaz.

## Güncelleme sonrası çıktı

Roadmap değiştiğinde ekibin gördüğü şey de değişmeli:

1. `docs/roadmap.md` — güncellenmiş, changelog'lu
2. Görseller ve PDF — `render_visuals.py` + Marp yeniden çalıştırılmış. Görselleri elle düzeltme; `plan.json`'ı düzelt ve yeniden üret.
3. **Değişim özeti** — iki versiyon: ekip için 3–5 satır (ne değişti, kritik yol nasıl etkilendi, kim ne yapacak) ve müşteri için üç satır (`references/audience.md`): **ne değişti · plana etkisi · sizden gereken**. "Sizden gereken: yok" satırını atlama — müşteri her güncellemede kendisinden bir şey isteneceğini varsayar.

Üçüncüsü en çok atlanan ve en çok işe yarayandır. Kimse 40 slaytlık güncellenmiş sunumu baştan okumaz.
