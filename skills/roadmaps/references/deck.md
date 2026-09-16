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

| Dosya | Grafik türü | Ne anlatır | Hangi soruya cevap |
|---|---|---|---|
| `journey.svg` | Kart dizisi | Faz yolculuğu, her aşamanın müşteri çıktısı ve kanıtı | "Ne zaman ne alıyorum?" |
| `swot.svg` | **2x2 panel** | Güçlü/zayıf yönler, fırsatlar/tehditler | "Fikir sağlam mı, nereden vurulabilir?" |
| `team_size.svg` | **Sütun (3 senaryo)** | 1-3/3-5/5+ kişi karşılaştırması, süre bazlı öneri | "Kaç kişilik ekip bu işe yeter?" |
| `team.svg` | **Kart dizisi** | Ekip üyeleri, rol, güven verici deneyim | "Bunu kim yapacak, neden başarabilirler?" |
| `traction.svg` | **Stat + alıntı** | Pilot/LOI/bekleme listesi sayıları, gerçek kullanıcı sözü | "Bu iş zaten çalıştığını kanıtladı mı?" |
| `riskmatrix.svg` | Matris + liste | Etki × olasılık, azaltma planıyla | "Riskleri nasıl yönetiyorsunuz?" |
| `market_impact.svg` | **İki panel kart** | Türkiye ve global pazar büyüklüğü, örnek girişimlerle | "Bu pazarın gerçek karşılığı var mı?" |
| `deadline.svg` | Gauge (tek çubuk) | Kritik yol vs elinizdeki süre, tampon | "Bu tarihe yetişir mi?" |
| `cost.svg` | **Pasta (donut)** | Aylık işletme gideri, kalem kalem, yüzde | "Yatırım ve işletme maliyeti ne?" |
| `growth.svg` | **Sütun (çift panel)** | Hayata geçtikten sonra 3/6/12 ay birikmiş müşteri ve gelir | "Bu iş büyür mü, ne kadar?" |
| `marketing.svg` | **Üç kolon** | Kampanya fikirleri, renk paleti (anlamıyla), AI içerik araçları | "Büyümeyi nasıl tetikleyeceğiz?" |
| `ad_creative.svg` | **Mockup kart** | Önerilen palet/sloganla somut bir örnek reklam görseli | "Bu nasıl görünecek?" |

Grafik türleri kasıtlı olarak çeşitli tutulur (kart, 2x2 panel, stat+alıntı, matris, kart-panel, gauge, pasta, sütun, üç kolon, mockup) — art arda aynı çubuk grafiği tekrarlamak sunumu monoton gösterir.

`team_size.svg` isim gerektirmez — `plan.json`'daki iş/effort/bağımlılık verisinden hesaplanır, bu yüzden **her zaman** üretilir (opsiyonel değildir). `team.svg` bunun tam tersi: **SADECE** `team_members` alanında gerçek, kullanıcının verdiği isimler varsa üretilir — isim uydurmak kesinlikle yasaktır, veri yoksa bu görsel hiç üretilmez ve deck'te `team_size.svg` kullanılır (`references/discovery.md`).

`swot.svg` yalnızca `swot`'un en az bir alt alanı, `traction.svg` yalnızca `traction.metrics` veya `traction.quote`, `deadline.svg` yalnızca `deadline.days_available`, `cost.svg` yalnızca `cost_estimate.recurring_monthly`, `growth.svg` yalnızca `growth_projection.milestones`, `market_impact.svg` yalnızca `market_impact.turkey` veya `market_impact.global`, `marketing.svg` yalnızca `marketing_strategy`'nin bir alt alanı, `ad_creative.svg` yalnızca `marketing_strategy.color_palette` doluysa üretilir; yoksa sessizce atlanır ve deck'teki karşılık gelen slayt tamamen silinir. Bunların hepsi ve `competitive_analysis` teknik olarak opsiyoneldir ama **varsayılan olarak beklenir** — discovery'de aktif olarak doldurulmalı, sadece gerçekten imkansızsa atlanır (`references/discovery.md`).

`--audience delivery` ile teknik adları kullanan ikinci bir set üretilir; ekip içi çalışma için (timeline/depgraph/capacity dahil tüm görseller).

Görsellerin okunabilirliği `plan.json`'daki metin uzunluklarına bağlı. Faz adı 30, iş adı 40 karakteri geçerse kırpılır — plan yazarken bunu gözet.

## Slayt yapısı

Ölçeğe göre 12–18 slayt — ölçek büyüdükçe faz sayısı artmaz, çünkü faz detayı ayrı slaytlara yayılmaz (aşağıya bak). Sıra bir argüman kurar — fırsat, kanıt, çözüm, getiri, büyüme, güven, kapanış:

| # | Slayt | Neden burada |
|---|---|---|
| 1 | Kapak — proje adı, **slogan**, tek cümlelik hedef | Aynı şeyi mi konuşuyoruz, akılda kalıcı aç |
| 2 | Neden bu proje (metrik kartları) | Problemi rakamla sabitle |
| 2b | **Fırsat** (`business_case` varsa) | Fırsatın büyüklüğünü rakamla göster |
| 2c | **Neden biz** (`competitive_analysis` varsa) | Alternatiflere karşı somut farkı göster |
| 2d | **SWOT analizi** (`swot.svg`, `swot` varsa) | Fikri dört yönden dürüstçe sınayan tek görsel |
| 2e | **Ekip** (`team_size.svg` varsayılan; gerçek isim varsa `team.svg`) | Kaç kişilik ekip yeter / bunu kim yapacak |
| 2f | **Traction** (`traction.svg`, `traction` varsa) | Bu iş zaten çalıştığını kanıtladı |
| 2g | **Türkiye ve global etki** (`market_impact.svg`, `market_impact` varsa) | Pazarın gerçek/somut olduğunu örneklerle göster |
| 3 | Çözüm yol haritası (`journey.svg`) — tek slayt, tüm fazlar | Müşteri ne zaman ne alıyor, hepsi bir bakışta |
| n+1 | **Yatırım ve getiri** (`cost.svg`, `cost_estimate` varsa) | Maliyeti şeffaf koy, beklenen getiriyle yan yana göster |
| n+2 | **Büyüme projeksiyonu** (`growth.svg`, `growth_projection` varsa) | 3/6/12 ayda iş ne kadar büyüyor |
| n+3 | **Pazarlama ve reklam stratejisi** (`marketing.svg`, `marketing_strategy` varsa) | Büyümeyi nasıl tetikleyeceğiz |
| n+4 | **Örnek reklam içeriği** (`ad_creative.svg`, `marketing_strategy.color_palette` varsa) | Somut bir görselle "böyle görünecek" de |
| n+5 | Riskler ve yönetimi (`riskmatrix.svg`) | Riskleri gizlemeden, kontrol altında olduğunu göster |
| n+6 | **Teslim güvenilirliği** (`deadline.svg`, `deadline` varsa) | Bu tarihe yetişir mi, tamponu ne kadar |
| n+7 | Sonraki adım | Kapanış — vizyonu ve sloganı tekrar bağla |

1, 2, 3, 2e (Ekip — her zaman `team_size.svg` ile üretilir), n+5 ve son slayt zorunlu. Geri kalanların hepsi opsiyonel — sırasıyla `plan.json`'da `business_case`, `competitive_analysis`, `swot`, `traction`, `market_impact`, `cost_estimate`, `growth_projection`, `marketing_strategy` ve `deadline` alanları doluysa eklenir, boşsa slayt tamamen silinir (yarım doldurulmuş slayt göstermek boş slayttan kötüdür). Ama bunların hepsi **varsayılan olarak doldurulması beklenen** alanlardır — "opsiyonel" demek "atla" demek değildir, discovery'de aktif olarak araştır. `team_members` bu kuralın istisnasıdır: varsayılan değildir, sadece gerçek isim varsa doldurulur (`references/discovery.md`).

**Faz başına ayrı slayt yok.** `journey.svg` zaten her fazın adını, "bu aşama bitince ne oluyor"unu, kanıtını ve süresini tek bir görselde, tüm fazlar yan yana gösteriyor — bunu tekrar her faz için ayrı bir slaytta anlatmak hem yer kaplar hem de aynı bilgiyi iki kere sunar. Faz başına tam detay (bağımlılıklar, iş listesi, risk) zaten `roadmap.md`'de var; deck'e ikinci kez taşınmaz.

**KPI kartlarında dahili zamanlama/program referansı kullanma.** "Faz 3 sonu" (`success_metric.measured_at`) veya "Q1 Partner Program penceresi" gibi iç planlama etiketlerini bir KPI kartı olarak gösterme — bunlar plan içi referanslar, müşteri/yatırımcı için anlamsız veya gereksiz teknik detaydır. "Neden bu proje" ve "Fırsat" slaytları bu yüzden 2 kart kullanır (3 değil): büyüklük + hedef/etki, zamanlama kartı yok. Deadline'ın nedeni (`deadline.driver`) sadece **Teslim güvenilirliği** slaydında, tek yerde geçer — orada bağlamı açıklamak doğaldır, başka hiçbir slaytta tekrarlanmaz.

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
- Görsel kendi başına yeterince yoğunsa (örn. `riskmatrix.svg` — matris + azaltma listesi) altına ayrıca `.callout` ekleme; slayt yüksekliğini taşırır ve alt bilgiyle çakışır. `journey.svg`, `cost.svg`, `deadline.svg` gibi daha sade görsellerin altına tek callout/muted satır güvenle sığar.

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
| Slogan | Seçilen + alternatifler | Sadece seçilen, kapak slaydında |
| Büyüme projeksiyonu | Tablo, varsayımlarla | `growth.svg`, tek slayt |
| Türkiye ve global etki | Tam metin, kaynak notuyla | `market_impact.svg`, tek slayt |
| SWOT analizi | Tam liste (4 madde/kategori) | `swot.svg`, tek slayt (en fazla 5 madde/kategori) |
| Ekip | Boyut önerisi her zaman, isimli liste sadece gerçekse | `team_size.svg` (varsayılan) veya `team.svg` (gerçek isim varsa) |
| Traction | Tam liste + alıntı | `traction.svg`, tek slayt |
| Pazarlama ve reklam stratejisi | Tam liste, araç kaynak tarihiyle | `marketing.svg` + `ad_creative.svg`, iki slayt |
| Changelog | Var | Yok |

Sunumu `roadmap.md`'nin kısaltılmış hâli olarak üretme. Farklı işe hizmet ediyorlar: biri kanıt, biri ikna.
