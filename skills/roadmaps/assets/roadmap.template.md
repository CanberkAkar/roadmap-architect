# {{Proje adı}} — Roadmap

> Bu doküman yaşayan bir plandır. Değişiklikler en alttaki changelog'a yazılır.
> Kaynak veri: `plan.json` · Son güncelleme: {{tarih}} · Durum: {{Taslak / Onaylandı / Yürürlükte}}
> Müşteri sunumu: `docs/roadmap-deck.pdf` — aynı `plan.json`'dan üretilir, elle düzenlenmez.

<!-- slogan plan.json'da doluysa bu satır kalır, degilse tamamen sil -->
**Slogan:** {{slogan.chosen}} — alternatifler: {{slogan.alternatives, virgülle}}

## Hedef

{{Tek cümlelik business hedefi.}}

**Başarı kriteri**

| Metrik | Baseline | Hedef | Ölçüm zamanı |
|---|---|---|---|
| {{metrik}} | {{değer}} | {{değer}} | {{faz}} |

<!-- business_case plan.json'da doluysa bu bölüm kalır, degilse tamamen sil -->
## İş değeri

**Problem:** {{bugün ne oluyor ve maliyeti}}
**Fırsat:** {{talep büyüklüğü — kaç aday, kaç kullanıcı, hangi pazar}}
**Beklenen etki:** {{ölçülebilir, mümkünse rakamlı}}
**Yapılmazsa:** {{maliyet}}

<!-- competitive_analysis plan.json'da doluysa bu bölüm kalır, degilse tamamen sil -->
## Rakip analizi

| Alternatif | Fiyat | Pazar konumu | İyi yaptığı | Yapamadığı |
|---|---|---|---|---|
| {{Rakip A}} | {{499$/ay}} | {{kurumsal segment}} | {{...}} | {{...}} |
| {{Rakip B}} | {{99$/ay}} | {{KOBİ/startup}} | {{...}} | {{...}} |
| {{Statüko / hiçbir şey yapmamak}} | {{...}} | — | {{...}} | {{...}} |

**Bizim farkımız:** {{somut fark 1}} · {{somut fark 2}} · {{somut fark 3}}

<!-- swot plan.json'da doluysa bu bölüm kalır, degilse tamamen sil -->
## SWOT analizi

| Güçlü yönler | Zayıf yönler |
|---|---|
| {{madde 1}} | {{madde 1}} |
| {{madde 2}} | {{madde 2}} |

| Fırsatlar | Tehditler |
|---|---|
| {{madde 1}} | {{madde 1}} |
| {{madde 2}} | {{madde 2}} |

<!-- market_impact plan.json'da doluysa bu bölüm kalır, degilse tamamen sil -->
## Türkiye ve global etki

**Türkiye** — {{pazar büyüklüğü}}
{{özet: bugün pazarda ne durumda}}
- {{örnek girişim/şirket 1}}
- {{örnek girişim/şirket 2}}

**Global** — {{pazar büyüklüğü}}
{{özet: global pazarda ne durumda}}
- {{örnek şirket 1}}
- {{örnek şirket 2}}

**Kaynak/varsayım:** {{market_impact.notes}}

## Ekip büyüklüğü önerisi

*İsim gerektirmez — toplam iş yükü ve kritik yoldan otomatik hesaplanır.*

| Ekip büyüklüğü | Süre | Sınırlayan |
|---|---|---|
| 1-3 kişi | {{N}} gün ({{N}} sprint) | {{kapasite / kritik yol}} |
| 3-5 kişi | {{N}} gün ({{N}} sprint) | {{kapasite / kritik yol}} |
| 5+ kişi | {{N}} gün ({{N}} sprint) | {{kapasite / kritik yol}} |

**Öneri:** {{en kısa süreye ulaşan en küçük ekip}} — daha büyük ekip kritik yolu kısaltmıyorsa sadece maliyeti artırır.

<!-- team_members plan.json'da doluysa bu bölüm kalır (SADECE gerçek, kullanıcının verdiği isimlerle — asla uydurma), degilse tamamen sil -->
## Ekip (isimli)

| İsim | Rol | Neden güvenilir |
|---|---|---|
| {{isim}} | {{rol}} | {{deneyim/başarı}} |

<!-- traction plan.json'da doluysa bu bölüm kalır, degilse tamamen sil -->
## Traction

| Metrik | Değer |
|---|---|
| {{Pilot müşteri}} | {{3}} |
| {{Bekleme listesi}} | {{18}} |

> "{{traction.quote.text}}" — {{traction.quote.source}}

<!-- marketing_strategy plan.json'da doluysa bu bölüm kalır, degilse tamamen sil -->
## Pazarlama ve reklam stratejisi

**Önerilen içerik tarzı:** {{marketing_strategy.content_style}}

| Kanal | Yaklaşım | Neden |
|---|---|---|
| {{kanal}} | {{yaklaşım}} | {{gerekçe}} |

**Renk paleti**

| Renk | Ad | Anlamı/tetiklediği |
|---|---|---|
| {{#hex}} | {{ad}} | {{anlam}} |

**Önerilen AI içerik araçları** *(zamanla eskir — plan güncellenirken WebSearch ile yeniden doğrulanmalı, {{tarih}} itibarıyla)*

| Araç | Kullanım alanı | Neden |
|---|---|---|
| {{araç adı}} | {{ne için}} | {{gerekçe}} |

<!-- cost_estimate plan.json'da doluysa bu bölüm kalır, degilse tamamen sil -->
## İşletme gideri

| Kalem | Tutar | Not |
|---|---|---|
| {{Sunucu / hosting}} | {{150}} {{USD}}/ay | {{varsayım}} |

**Aylık toplam:** {{730}} {{USD}} · **Yıllık toplam:** {{8.760}} {{USD}}
{{Tek seferlik kurulum maliyeti varsa buraya bir satır ekle}}

<!-- growth_projection plan.json'da doluysa bu bölüm kalır, degilse tamamen sil -->
## Büyüme projeksiyonu (hayata geçtikten sonra, birikmiş)

| Ay | Müşteri | Yeni müşteri | Gelir | Yeni gelir |
|---|---|---|---|---|
| {{3}} | {{15}} | {{+15}} | {{45.000}} {{USD}} | {{+45.000}} |
| {{6}} | {{40}} | {{+25}} | {{120.000}} {{USD}} | {{+75.000}} |
| {{12}} | {{90}} | {{+50}} | {{320.000}} {{USD}} | {{+200.000}} |

**Varsayım:** {{growth_projection.notes}}

## Kısıtlar

- {{kısıt}} → roadmap'e etkisi: {{...}}

## Kapsam dışı

- {{madde}} → nedeni: {{...}}

## Açık varsayımlar

| # | Varsayım | Yanlışsa ne olur | Nasıl doğrulanıyor |
|---|---|---|---|
| A1 | {{...}} | {{etki}} | {{spike/faz}} |

---

## Faz haritası

| Faz | Amaç | Öncelik | Effort (P50–P80) | Bağımlı | Durum |
|---|---|---|---|---|---|
| P1 · {{ad}} | {{durum değişikliği}} | P0 | 5–9 | — | Planlandı |
| P2 · {{ad}} | {{...}} | P0 | 22–30 | P1 | Planlandı |

**Kritik yol:** {{T01 → T03 → T04 → ...}} · {{N}} gün
**Paralelleşebilirlik indeksi:** {{PI}} · **Akış sayısı:** {{S}}

<!-- deadline plan.json'da doluysa bu satır kalır, degilse tamamen sil -->
**Teslim güvenilirliği:** elinizdeki süre {{M}} gün ({{driver}}) · tampon {{+/-X}} gün (%{{Y}}) → {{Rahat / Sıkışık / Riskli}}

---

## Fazlar

### P1 · {{Faz adı}}

**Müşteri çıktısı:** {{Bu aşama bitince müşteri ne yapabilir hale geliyor — teknik terim yok}}
**Amaç (teknik):** {{Faz bittiğinde sistem nerede olacak}}
**Milestone:** {{Demo edilebilir / ölçülebilir kanıt}}
**Öncelik:** P0 · **Effort:** {{P50}}–{{P80}} insan-günü · **Durum:** Planlandı
**Bağımlılıklar:** {{iç fazlar, dış aktörler}}
**Çıktı:** {{kim ne alıyor}}

| İş | Effort (P50–P80) | Akış | Bağımlı | Risk |
|---|---|---|---|---|
| T01 {{ad}} | 3–5 | veri | — | Yüksek |

**Bu fazda cevaplanacak sorular**
- {{soru}} → {{doğrulama biçimi}} → karar noktası: {{sonuç X ise plan Y olur}}

---

## Riskler

| # | Risk | Tür | Etki | Olasılık | Ne zaman öğreniriz | Doğrulama | Karar noktası |
|---|---|---|---|---|---|---|---|
| R1 | {{...}} | Teknik | Yüksek | Orta | Faz 1 | {{spike}} | {{...}} |

## Müşteriden beklenenler

Bunlar kritik yol hesabına dahildir — geciktiklerinde teslim doğrudan kayar.

| Ne | Kimden | Ne zaman gerekiyor | Lead time | Gecikirse |
|---|---|---|---|---|
| {{SSO metadata}} | {{müşteri IT}} | Sprint {{1}} | {{10}} gün | {{Aşama 2 bir sprint kayar}} |

## Dış bağımlılıklar

| Ne | Kimden | Lead time | Ne zaman tetiklenmeli | Sahibi |
|---|---|---|---|---|
| {{...}} | {{...}} | {{N}} gün | Sprint {{N}} | {{kişi}} |

---

## Kapasite ve ölçeklendirme

**Ekip:** {{N}} kişi · odak faktörü {{0.65}} · sprint {{10}} gün → sprint kapasitesi {{26}} insan-günü
**Minimum süre:** {{N}} sprint ({{kapasite / kritik yol}} bağlıyor)

| Faz | Paralel iş (PI) | Önerilen agent | Sınırlayan | Not |
|---|---|---|---|---|
| P1 | {{...}} | {{N}} | {{darboğaz}} | {{...}} |

**Darboğazı kaldırmak için:** {{eylem}}

## Sprint özeti

| Sprint | Faz | İşler | Planlanan / Kapasite | Sprint sonu kanıtı |
|---|---|---|---|---|
| 1 | P1 | T01, T02 | 7 / 26 | {{...}} |

---

## Müşteriye giden güncelleme özeti

Her revizyonda üç satır, teknik terim olmadan:

```
Ne değişti: {{olgu}}
Plana etkisi: {{hangi aşama ne kadar kaydı}}
Sizden gereken: {{varsa; yoksa "yok" yaz}}
```

## Changelog

### {{YYYY-AA-GG}} · {{başlık}}
**Ne oldu:** {{olgu}}
**Düşen varsayım:** {{A1}}
**Karar:** {{...}}
**Etki:** {{faz +N gün · kritik yol X → Y · faz Z kaydı}}
**Alternatifler:** {{seçilmeyenler ve neden}}
