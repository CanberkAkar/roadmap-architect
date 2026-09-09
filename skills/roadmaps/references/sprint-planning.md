# Sprint planı

Sprint planı roadmap'in altındaki katmandır. Roadmap "hangi aşamalardan geçeceğiz"i, sprint planı "önümüzdeki N hafta ne yapılıyor"u söyler. İkisini aynı dokümana karıştırma.

## Girdi

`plan.json` + kapasite script'inin çıktısı. Script sprint dağılımını zaten yapar; senin işin onu okunur ve savunulabilir hale getirmek.

```bash
python3 skills/roadmaps/scripts/plan_capacity.py plan.json --json > capacity.json
```

## Script'in kullandığı sıralama

Her sprintte "hazır" işler (tüm dependency'leri önceki sprintlerde biten) şu önceliğe göre yerleşir:

1. Yüksek riskli işler — erken doğrulama ilkesi
2. En çok işin önünü açanlar (dependent sayısı fazla olanlar)
3. Kritik yol üzerindekiler
4. Küçük olanlar (sprint'in artan kapasitesini doldurur)

Bu sıralamayı değiştirmen gereken durumlar olur (sabit bir dış tarih, sözleşme yükümlülüğü, demo zorunluluğu). Değiştirdiğinde nedenini plana yaz — script tekrar çalıştırıldığında farkın nereden geldiği anlaşılsın.

## İlk sprint farklıdır

İlk sprintin işi hız değil, **belirsizliği düşürmek ve akışı kurmak**tır. Kapasitesinin en az yarısını şuraya ayır:

- En yüksek riskli 1–2 spike
- Uzun lead time'lı dış bağımlılıkların tetiklenmesi (talebin gönderilmesi bile bir iş kalemidir)
- Ortam/CI/deploy hattının çalışır hale gelmesi
- Başarı metriğinin ölçülebilir olması

Ekip yeni oluştuysa ilk sprint kapasitesini %30 düşür. Bu bir tampon değil, gözlenmiş bir gerçeklik.

## Sprint kartı formatı

```markdown
### Sprint 3 · Faz 2: Ödeme akışı
**Amaç:** Test ortamında uçtan uca ödeme alınabiliyor
**Kapasite:** 26 insan-günü (4 kişi × 10 gün × 0.65) · **Planlanan:** 24
**Paralel akış:** 3 (api · web · ödeme-entegrasyonu)

| İş | Effort | Akış | Bağımlı olduğu | Risk |
|---|---|---|---|---|
| T12 Ödeme sağlayıcı sözleşme testi | 2 | ödeme | — | Yüksek |
| T13 Checkout uç noktası | 6 | api | T09 | Orta |
| T14 Ödeme adımı UI | 5 | web | T13 | Düşük |

**Sprint sonu kanıtı:** Test kartıyla sipariş tamamlanıp webhook'la onay düşüyor
**Riskler / bu sprintte cevaplanacak sorular:** Sağlayıcı 3DS akışını sandbox'ta destekliyor mu?
```

Her sprintin bir **kanıtı** olmalı. Kanıtı yazılamayan sprint, sprint değil takvim dilimidir.

## Sprint boyu

- **1 hafta** — belirsizlik yüksek, yön sık değişiyor, ekip küçük
- **2 hafta** — varsayılan
- **3+ hafta** — önerme; geri bildirim döngüsü roadmap'i güncel tutamayacak kadar yavaşlar

## Taşma ve tampon

Sprint'i %100 doldurma. Kapasitenin **%15–20'sini** planlanmamış bırak: gelen hata, üretim olayı, inceleme yükü, tahmin sapması. Script bunu `focus_factor` içinde kısmen hesaba katar; kalanını sprint dolduruken bilinçli bırak.

Bir sprint iki kez üst üste taşıyorsa sorun plan değil, `focus_factor`'dır. Gerçekleşene göre düşür ve kalan sprintleri yeniden hesapla — taşmayı sonraki sprinte itmek planı sessizce bozar.

## Sprint planından sonra

Sprint planını üretmek roadmap'i bitirmez. Her sprint sonunda `references/revision.md` içindeki güncelleme protokolünü çalıştır: ne öğrenildi, hangi varsayım düştü, kalan fazlar nasıl kaydı.
