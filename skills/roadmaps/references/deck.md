# Sunum ve PDF

Bu bir **pitch**: müşteriye veya yatırımcıya tek yönlü, güçlü ve görsel bir sunum. Amaç ortada karar aldırmak veya itiraz toplamak değil — vizyonu, fırsatı ve planı ikna edici şekilde anlatmak. `roadmap.md` referans dokümandır ve tüm teknik derinliği, belirsizlikleri, kapsam dışı listesini ve müşteriden beklenen işleri tam olarak taşır; PDF sunum bunların hiçbirini slayt olarak göstermez. Aynı `plan.json`'dan gelirler ama aynı içeriği taşımazlar.

Dil kurallarını önce `references/audience.md` içinden oku. Sunumun tamamı müşteri diliyle yazılır; teknik derinlik `roadmap.md` içinde kalır.

## Üretim sırası

```bash
# 1. Hesap
python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/scripts/plan_capacity.py plan.json

# 2. Görseller (müşteri diliyle)
python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/scripts/render_visuals.py plan.json \
  --out docs/assets --audience customer

# 3. Slaytları yaz — assets/deck.template.md şablonundan, docs/roadmap-deck.md olarak

# 4. PDF
npx --yes @marp-team/marp-cli@latest docs/roadmap-deck.md \
  --theme ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/assets/theme.css \
  --allow-local-files --pdf -o docs/roadmap-deck.pdf
```

`--allow-local-files` olmadan SVG'ler PDF'e gömülmez, slaytlar boş çıkar.

**Tarayıcı yoksa** (CI, konteyner, sunucu): `--pdf` yerine `--html -o docs/roadmap-deck.html` kullan ve kullanıcıya söyle — HTML'i tarayıcıda açıp "PDF olarak yazdır" demesi yeterli, çıktı aynı. HTML `docs/assets/` klasörüne bağımlıdır, ikisini birlikte taşımak gerekir; PDF ise kendi kendine yeter.

`--pptx` de mümkün ama görseller tek parça resim olarak gömülür, düzenlenemez. Müşteri düzenlenebilir dosya istiyorsa ve ortamda `pptx` skill'i varsa onu kullan; yine de `roadmap-deck.md` kaynağını da yaz ki plan güncellendiğinde yeniden üretilebilsin.

## Görseller

`render_visuals.py` `plan.json`'dan üretir. Elle çizme, elle düzenleme — plan değişince yeniden üretilebilir kalmalı. Deck'e giren görseller sadece şunlardır — `timeline.svg`, `depgraph.svg` ve `capacity.svg` de üretilir ama bunlar yürütme/kapasite detayıdır, pitch'e değil `roadmap.md`'ye ve ekip içi çalışmaya hizmet eder, deck'te kullanılmaz:

| Dosya | Ne anlatır | Hangi soruya cevap |
|---|---|---|
| `journey.svg` | Faz yolculuğu, her aşamanın müşteri çıktısı ve kanıtı | "Ne zaman ne alıyorum?" |
| `riskmatrix.svg` | Etki × olasılık, azaltma planıyla | "Riskleri nasıl yönetiyorsunuz?" |
| `deadline.svg` | Kritik yol vs elinizdeki süre, tampon | "Bu tarihe yetişir mi?" |
| `cost.svg` | Aylık işletme gideri, kalem kalem | "Yatırım ve işletme maliyeti ne?" |

`deadline.svg` yalnızca `plan.json`'da `deadline.days_available`, `cost.svg` yalnızca `cost_estimate.recurring_monthly` doluysa üretilir; yoksa sessizce atlanır ve deck'teki karşılık gelen slayt tamamen silinir.

`--audience delivery` ile teknik adları kullanan ikinci bir set üretilir; ekip içi çalışma için (timeline/depgraph/capacity dahil tüm görseller).

Görsellerin okunabilirliği `plan.json`'daki metin uzunluklarına bağlı. Faz adı 30, iş adı 40 karakteri geçerse kırpılır — plan yazarken bunu gözet.

## Slayt yapısı

Ölçeğe göre 8–13 slayt. Sıra bir argüman kurar — fırsat, çözüm, güven, kapanış:

| # | Slayt | Neden burada |
|---|---|---|
| 1 | Kapak + tek cümlelik hedef | Aynı şeyi mi konuşuyoruz |
| 2 | Neden bu proje (metrik kartları) | Problemi rakamla sabitle |
| 2b | **Fırsat** (`business_case` varsa) | Fırsatın büyüklüğünü ve zamanlamasını rakamla göster |
| 2c | **Neden biz** (`competitive_analysis` varsa) | Alternatiflere karşı somut farkı göster |
| 3 | Çözüm yol haritası (`journey.svg`) | Müşteri ne zaman ne alıyor |
| 4..n | Faz detayları, faz başına bir slayt | Somutlaştır, güven ver |
| n+1 | **Yatırım ve getiri** (`cost.svg`, `cost_estimate` varsa) | Maliyeti şeffaf koy, beklenen getiriyle yan yana göster |
| n+2 | Riskler ve yönetimi (`riskmatrix.svg`) | Riskleri gizlemeden, kontrol altında olduğunu göster |
| n+3 | **Teslim güvenilirliği** (`deadline.svg`, `deadline` varsa) | Bu tarihe yetişir mi, tamponu ne kadar |
| n+4 | Sonraki adım | Kapanış — vizyonu tekrar bağla |

1, 2, 3, n+2 ve son slayt zorunlu. 2b, 2c, n+1 ve n+3 opsiyonel — sırasıyla `plan.json`'da `business_case`, `competitive_analysis`, `cost_estimate` ve `deadline` alanları doluysa eklenir, boşsa slayt tamamen silinir (yarım doldurulmuş slayt göstermek boş slayttan kötüdür).

Bu deck'te **olmaması gerekenler**: "Bu planda YOK" (kapsam dışı listesi), "Sizden beklenenler" (müşteriden istenen işler listesi), "Bugün karar verilecekler" (karar/onay listesi). Bunların hiçbiri pitch'in işi değil — üçü de `roadmap.md`'de tam olarak durur ve toplantıda soru gelirse oradan sözlü cevaplanır. Deck'e bunlardan birini eklemek istersen önce kendine sor: bu bir onay/itiraz toplama slaytı mı? Öyleyse `roadmap.md`'ye yaz, deck'e koyma.

## Belirsizliği deck'te gösterme

`roadmap.md` her şeyi gösterir: "bilinmiyor" baseline'lar, açık varsayımlar, efor aralıklarının genişliği. Deck bunları **göstermez, gizlemez de** — basitçe o veri yoksa ilgili KPI kartı/satır deck'ten çıkarılır. Sahte bir rakamla doldurma; slaydı veya kartı sil.

- `success_metric.baseline` "bilinmiyor" ise o KPI kartını deck'ten çıkar, `roadmap.md`'de "bilinmiyor" olarak dursun.
- `business_case`, `competitive_analysis`, `deadline`, `cost_estimate` boşsa ilgili slayt tamamen silinir — boş şablon veya "veri yok" yazan bir slayt bırakma.
- Efor **aralığı** (P50–P80) deck'te tek sayıya yuvarlanabilir ("~20 iş günü") — sahte kesinlik yaratmaz çünkü teknik taahhüt değil, büyüklük hissi vermek içindir. `roadmap.md`'de aralık tam kalır.

## Slayt yazım kuralları

- Slayt başına tek fikir. İki fikir varsa iki slayt.
- Satır başına en fazla ~12 kelime, metin slaytında en fazla 6 satır.
- Görsel slaytlarında `<!-- _class: visual -->` kullan; görsel tam genişliğe yayılır, yanına metin koyma.
- Görsel slaytlarındaki grafiklerin altına yazılan sayılar dahil, cümle kurarken teknik terim kullanma (`references/audience.md`).
- Riski gizleme ama **çözümsüz** bırakma: her risk cümlesinin yanında nasıl yönetildiği/azaltıldığı olsun — "X olabilir" değil, "X olabilir, bunun için Y yapıyoruz".
- `.callout` bloğunu slayt başına en fazla bir kez kullan; her yerde varsa hiçbir yerde vurgu kalmaz.
- Ton cesur ve net olsun — soru sorarak değil, iddia ederek yaz. "Sizce nasıl olur?" yerine "Bu şekilde çalışıyor."

## Tema

`assets/theme.css`. Marp'a `--theme` ile verilir. Sağladığı sınıflar:

| Sınıf | Kullanım |
|---|---|
| `<!-- _class: lead -->` | Kapak slaytı |
| `<!-- _class: visual -->` | Tam genişlik görsel slaytı |
| `.kpi` | Yan yana metrik kartları (2–4 tane) |
| `.callout` | Vurgulanan tek paragraf |
| `.callout.risk` | Kırmızı kenarlı uyarı |
| `.callout.ask` | Turuncu kenarlı — varsayılan şablonda kullanılmaz, gerçekten müşteriden tek bir şey istemen gerekirse elle eklenebilir |
| `.muted` `.risk` `.warn` `.ok` | Satır içi renk vurguları |

Renkleri değiştirmen gerekirse `theme.css` içindeki `:root` değişkenlerini ve `render_visuals.py` başındaki paleti **birlikte** güncelle; ikisi aynı renkleri kullanır.

## Sunum ve roadmap.md arasındaki iş bölümü

| | `roadmap.md` | PDF sunum |
|---|---|---|
| İzleyici | Teknik ekip + PM | Müşteri / yatırımcı |
| Amaç | Referans, tek doğruluk kaynağı | İkna — vizyon ve güven |
| Detay | Tam: her iş, her dependency, kapsam dışı, müşteriden beklenenler | Faz seviyesi, sadece güçlü metrikler |
| Effort | İş bazında, P50–P80 aralığı | Faz toplamı, yuvarlanmış |
| Risk | Tam tablo | En kritik 2–3, azaltma planıyla |
| Belirsizlik ("bilinmiyor") | Açıkça yazılır | Gösterilmez, o kart/satır silinir |
| Kapsam dışı / Sizden beklenenler / Kararlar | Tam liste | Yok |
| Changelog | Var | Yok |

Sunumu `roadmap.md`'nin kısaltılmış hâli olarak üretme. Farklı işe hizmet ediyorlar: biri kanıt, biri ikna.
