# roadmap-architect

Claude Code eklentisi. Business hedefinden fazlara, milestone'lara, sprint planına ve agent/ekip ölçeklendirmesine kadar bir yol haritası üretir — ve gerçeklik değiştikçe günceller.

**Amacı müşteriyle teknik ekibi aynı plana bakmaya getirmek.** İki ayrı doküman üretmez: tek bir `plan.json`'dan hem repo'da versiyonlanan teknik Markdown, hem müşterinin okuyabileceği görsel bir PDF çıkar. Biri güncellenip diğeri unutulamaz, çünkü ikisi de aynı veriden türer.

Roadmap'i task listesi olarak değil, ürünün hangi aşamalardan geçerek hedefe ulaşacağını gösteren üst seviye bir plan olarak ele alır. Sabit değil, yaşayan bir doküman olarak kurgulanmıştır.

## Kurulum

Claude Code içinde:

```
/plugin marketplace add CanberkAkar/roadmap-architect
/plugin install roadmap-architect@roadmap-architect
```

Yerel geliştirme için repo'yu klonlayıp klasör yolunu vermek de yeterli:

```
/plugin marketplace add ~/kod/roadmap-architect
```

Sadece skill'i (komutlar olmadan, Claude.ai dahil) kullanmak isterseniz `skills/roadmaps/`
klasörünü `~/.claude/skills/` altına kopyalayın ya da yayınlanan `.skill` dosyasını yükleyin.

## Komutlar

| Komut | Ne yapar |
|---|---|
| `/roadmap <hedef>` | Discovery'den başlayıp faz, milestone, risk, `plan.json`, `docs/roadmap.md` ve sunumu üretir |
| `/sprint` | `plan.json`'dan sprint planı çıkarır |
| `/scale [faz]` | Kritik yol, paralellik ve önerilen agent sayısını darboğazıyla birlikte verir |
| `/deck [customer\|delivery]` | Görselli sunum PDF'i üretir |
| `/roadmap-update <ne değişti>` | Yeni bulguya göre planı revize eder, changelog'a yazar |

Komut kullanmadan da çalışır — "şu projeyi nasıl planlarız", "bu işi kaç kişiyle böleriz" gibi sorularda skill kendiliğinden devreye girer.

## Çıktılar

| Dosya | Ne için |
|---|---|
| `plan.json` | Tek veri kaynağı. Diğer her şey bundan türer. |
| `docs/roadmap.md` | Referans doküman, changelog'lu, diff'lenebilir |
| `docs/roadmap-deck.md` | Sunum kaynağı (Marp) |
| `docs/roadmap-deck.pdf` | Müşteri sunumu, görselli |
| `docs/assets/*.svg` | Otomatik üretilen altı görsel (`team_size.svg` dahil, isim gerekmez) + opsiyonel `deadline.svg`, `cost.svg`, `growth.svg`, `market_impact.svg`, `swot.svg`, `traction.svg`, `marketing.svg`, `ad_creative.svg`, `team.svg` (sadece gerçek isim varsa) |
| `docs/sprints.md` | Sprint kartları |

```bash
python3 skills/roadmaps/scripts/render_visuals.py plan.json --out docs/assets --audience customer
npx --yes @marp-team/marp-cli@latest docs/roadmap-deck.md \
  --theme skills/roadmaps/assets/theme.css \
  --allow-local-files --pdf -o docs/roadmap-deck.pdf
```

`--allow-local-files` olmadan görseller PDF'e gömülmez. PDF üretimi tarayıcı gerektirir; ortamda yoksa `--html` ile üretip tarayıcıdan "PDF olarak yazdır" deyin, çıktı aynıdır.

## İki kitle, tek plan

`plan.json` içindeki `customer_*` alanları müşteri diline, diğerleri teknik ekibe hizmet eder:

| Alan | Müşteri görünümü | Teknik görünüm |
|---|---|---|
| Faz | `customer_outcome` | `purpose` |
| İş | `customer_name` | `name` |
| Risk | `customer_text` | `text` |

`render_visuals.py --audience customer|delivery` aynı plandan iki görsel seti üretir.

Sadeleştirme saklamak değildir: riskler, effort belirsizliği, müşteriden beklenenler ve kapsam dışı listesi müşteri görünümünde de aynen durur. Kurallar ve teknik terim → müşteri dili çeviri tablosu `references/audience.md` içinde.

## İş değeri, rakip analizi, pazar etkisi, deadline, maliyet ve büyüme

`plan.json`'a bu alanlar eklenirse sunumda ve `roadmap.md`'de otomatik birer bölüm/slayt açılır. Teknik olarak opsiyoneldir ama pitch deck'te **varsayılan olarak beklenir** — discovery sırasında aktif olarak (gerekirse WebSearch ile) doldurulur, sadece gerçekten imkansızsa boş kalır ve o zaman ilgili slayt/görsel sessizce atlanır:

| Alan | Ne anlatır | Otomatik çıktı |
|---|---|---|
| `slogan` | Seçilen slogan + alternatifler | Kapak ve kapanış slaydı |
| `business_case` | Problem, fırsat, beklenen etki, yapılmazsa | "Fırsat" slaydı/bölümü |
| `competitive_analysis` | Rakip başına fiyat, pazar konumu, güçlü/zayıf yanlar + bizim farkımız | "Neden biz" slaydı/bölümü |
| `swot` | Güçlü/zayıf yönler, fırsatlar/tehditler — dürüst | `swot.svg` (2x2 panel) |
| `team_members` *(sadece gerçek isim varsa — asla uydurma)* | Ekip, rol, doğrulanabilir deneyim | `team.svg` (kart dizisi) |
| `traction` | Gerçekleşmiş kanıt: pilot/LOI/bekleme listesi/alıntı | `traction.svg` (stat + alıntı) |
| `market_impact` | Türkiye ve global pazar büyüklüğü, isimli örnek girişimler/şirketler | `market_impact.svg` (iki panel) |
| `cost_estimate` | Kurulum + aylık işletme gideri (sunucu, reklam, vb.) | `cost.svg` (pasta grafik) + toplam hesabı |
| `growth_projection` | 3/6/12 ay sonra birikmiş müşteri sayısı ve gelir | `growth.svg` (sütun grafik) |
| `marketing_strategy` | Kampanya fikirleri, renk paleti (anlamıyla), güncel AI içerik araçları | `marketing.svg` (üç kolon) + `ad_creative.svg` (örnek mockup) |
| `deadline` | Elinizdeki süre, neden bu tarih | `deadline.svg` + teslim güvenilirliği hesabı |

```bash
python3 skills/roadmaps/scripts/plan_capacity.py plan.json   # Teslim güvenilirliği, işletme gideri ve büyüme bölümlerini de basar
```

## Görseller

`plan.json`'dan otomatik üretilir, elle çizilmez. Grafik türleri kasıtlı çeşitlendirilmiştir:

| Görsel | Tür | Hangi soruya cevap verir |
|---|---|---|
| `journey.svg` | Kart dizisi | Ne zaman ne alıyorum? |
| `timeline.svg` | Zaman şeridi | Sıra nasıl işliyor? (ekip içi) |
| `depgraph.svg` | Ağ diyagramı | Neden bu sırayla? (ekip içi) |
| `riskmatrix.svg` | Matris + liste | Ters giderse ne olur, nasıl yönetiyoruz? |
| `capacity.svg` | Çubuk | Neden daha hızlı olmuyor? (ekip içi) |
| `swot.svg` | **2x2 panel** | Fikir sağlam mı, nereden vurulabilir? (opsiyonel) |
| `team_size.svg` | **Sütun (3 senaryo)** | Kaç kişilik ekip yeter? (isim gerekmez, her zaman üretilir) |
| `team.svg` | **Kart dizisi** | Bunu kim yapacak, neden güvenilir? (opsiyonel, sadece gerçek isim varsa) |
| `traction.svg` | **Stat + alıntı** | Bu iş zaten çalıştığını kanıtladı mı? (opsiyonel) |
| `market_impact.svg` | **İki panel kart** | Bu pazarın Türkiye ve global karşılığı var mı? (opsiyonel) |
| `deadline.svg` | Gauge | Bu tarihe yetişir mi? (opsiyonel) |
| `cost.svg` | **Pasta (donut)** | Bu sistemin işletme gideri ne? (opsiyonel) |
| `growth.svg` | **Sütun (çift panel)** | Bu iş büyür mü, ne kadar? (opsiyonel) |
| `marketing.svg` | **Üç kolon** | Büyümeyi nasıl tetikleyeceğiz? (opsiyonel) |
| `ad_creative.svg` | **Mockup kart** | Reklam görseli nasıl görünecek? (opsiyonel) |

`timeline.svg`, `depgraph.svg`, `capacity.svg` sadece `roadmap.md` ve ekip içi (`--audience delivery`) kullanım için üretilir; müşteri pitch deck'ine girmez (`skills/roadmaps/references/deck.md`).

## Kapasite hesabı

Agent sayısı ve süre tahminleri kafadan değil, `plan.json`'daki dependency grafiğinden hesaplanır:

```bash
python3 skills/roadmaps/scripts/plan_capacity.py plan.json
python3 skills/roadmaps/scripts/plan_capacity.py plan.json --json --estimate p80
```

Hesapladıkları:

- **Kritik yol** — sonsuz kaynak verilse bile altına inilemeyecek süre
- **Paralelleşebilirlik indeksi** (`toplam effort / kritik yol`) — ortalama kaç iş aynı anda yürüyebilir
- **Önerilen agent sayısı** — `min(PI, çakışmayan akış sayısı, inceleme kapasitesi, 8)` ve hangisinin bağladığı
- **Minimum sprint sayısı** — kapasite ve kritik yol sınırlarının büyüğü
- **Sprint dağılımı** — riskli işler önde, dependency'lere ve sprint takvimine saygılı

Bağımlılığı yok, sadece Python 3 standart kütüphanesi.

### Neden bu formül

Paralelleşmeyen işe agent eklemek süreyi kısaltmaz, koordinasyon ve merge maliyetini artırır. Dört sınırın hangisinin bağladığını bilmek, "kaç agent" sorusunu "hangi darboğazı kaldıralım" sorusuna çevirir — asıl değer orada.

## Ölçek

| Ölçek | Toplam effort | Faz | Çıktı |
|---|---|---|---|
| S | < 20 gün | 1–2 | Tek sayfa roadmap, PDF yok |
| M | 20–80 | 3–4 | MD + 8–10 slayt PDF |
| L | 80–300 | 4–6 | MD + deck + stream bazlı sprint dağılımı |
| XL | > 300 | 5–8 | Yukarıdakiler + faz bazlı ayrı plan dosyaları |

Skill ölçeği effort toplamından kendi belirler ve süreç ağırlığını ona göre ayarlar.

## Yapı

```
roadmap-architect/
├── .claude-plugin/plugin.json
├── commands/            roadmap · sprint · scale · roadmap-update
└── skills/roadmaps/
    ├── SKILL.md
    ├── references/      discovery · phasing-and-risk · sprint-planning
    │                    agent-sizing · audience · deck · revision
    ├── assets/          plan.template.json · roadmap.template.md
    │                    deck.template.md · theme.css
    └── scripts/         plan_capacity.py · render_visuals.py
```


## Katkı

`plan.json` şeması, görseller ve kapasite formülü birbirine bağlı — birini değiştirirken diğerlerini
kontrol edin:

- Yeni bir `plan.json` alanı → `plan_capacity.flatten_items` ve `assets/plan.template.json`
- Renk değişikliği → `assets/theme.css` içindeki `:root` **ve** `render_visuals.py` başındaki palet
- Yeni görsel → `render_visuals.py` + `references/deck.md` tablosu + `assets/deck.template.md`

CI (`.github/workflows/validate.yml`) her push'ta JSON geçerliliğini, frontmatter'ları, referans
edilen dosyaların varlığını ve iki script'in çalıştığını kontrol eder.

Test için:

```bash
python3 skills/roadmaps/scripts/plan_capacity.py skills/roadmaps/assets/plan.template.json
python3 skills/roadmaps/scripts/render_visuals.py skills/roadmaps/assets/plan.template.json --out /tmp/vis
```

## Lisans

MIT
