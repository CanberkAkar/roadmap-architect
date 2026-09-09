# Sunum ve PDF

İzleyici **müşteri ve teknik ekip birlikte**. Amaç bilgi aktarmak değil, karar aldırmak ve itiraz toplamak. `roadmap.md` referans dokümandır; PDF tartışma aracıdır. Aynı veriden gelirler ama aynı içeriği taşımazlar.

Dil kurallarını önce `references/audience.md` içinden oku. Sunumun tamamı müşteri diliyle yazılır; teknik derinlik `roadmap.md` içinde kalır.

## Üretim sırası

```bash
# 1. Hesap
python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmap-architect/scripts/plan_capacity.py plan.json

# 2. Görseller (müşteri diliyle)
python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmap-architect/scripts/render_visuals.py plan.json \
  --out docs/assets --audience customer

# 3. Slaytları yaz — assets/deck.template.md şablonundan, docs/roadmap-deck.md olarak

# 4. PDF
npx --yes @marp-team/marp-cli@latest docs/roadmap-deck.md \
  --theme ${CLAUDE_PLUGIN_ROOT}/skills/roadmap-architect/assets/theme.css \
  --allow-local-files --pdf -o docs/roadmap-deck.pdf
```

`--allow-local-files` olmadan SVG'ler PDF'e gömülmez, slaytlar boş çıkar.

**Tarayıcı yoksa** (CI, konteyner, sunucu): `--pdf` yerine `--html -o docs/roadmap-deck.html` kullan ve kullanıcıya söyle — HTML'i tarayıcıda açıp "PDF olarak yazdır" demesi yeterli, çıktı aynı. HTML `docs/assets/` klasörüne bağımlıdır, ikisini birlikte taşımak gerekir; PDF ise kendi kendine yeter.

`--pptx` de mümkün ama görseller tek parça resim olarak gömülür, düzenlenemez. Müşteri düzenlenebilir dosya istiyorsa ve ortamda `pptx` skill'i varsa onu kullan; yine de `roadmap-deck.md` kaynağını da yaz ki plan güncellendiğinde yeniden üretilebilsin.

## Görseller

`render_visuals.py` beşini de `plan.json`'dan üretir. Elle çizme, elle düzenleme — plan değişince yeniden üretilebilir kalmalı.

| Dosya | Ne anlatır | Hangi soruya cevap |
|---|---|---|
| `journey.svg` | Faz yolculuğu, her aşamanın müşteri çıktısı ve kanıtı | "Ne zaman ne alıyorum?" |
| `timeline.svg` | Sprint bazlı zaman şeridi, ekiplere göre renkli | "Sıra nasıl işliyor?" |
| `depgraph.svg` | Bağımlılık haritası, kritik yol kırmızı | "Neden bu sırayla?" |
| `riskmatrix.svg` | Etki × olasılık, karar noktalarıyla | "Ters giderse ne olur?" |
| `capacity.svg` | Faz bazında paralellik ve darboğaz | "Neden daha hızlı olmuyor?" |

`--audience delivery` ile teknik adları kullanan ikinci bir set üretilir; ekip içi toplantı için.

Görsellerin okunabilirliği `plan.json`'daki metin uzunluklarına bağlı. Faz adı 30, iş adı 40 karakteri geçerse kırpılır — plan yazarken bunu gözet.

## Slayt yapısı

Ölçeğe göre 8–14 slayt. Sıra bir argüman kurar, bozma:

| # | Slayt | Neden burada |
|---|---|---|
| 1 | Kapak + tek cümlelik hedef | Aynı şeyi mi konuşuyoruz |
| 2 | Neden bu proje (metrik kartları) | Problemi rakamla sabitle |
| 3 | **Bu planda YOK** | İtirazlar burada toplanır, sonra pahalı |
| 4 | Faz yolculuğu (`journey.svg`) | Müşteri ne zaman ne alıyor |
| 5..n | Faz detayları, faz başına bir slayt | Somutlaştır |
| n+1 | Zaman şeridi (`timeline.svg`) | Sıra ve yoğunluk |
| n+2 | Bağımlılık haritası (`depgraph.svg`) | Neden bu sırayla |
| n+3 | Neden daha hızlı olmuyor | Kritik yolu açıkla, kısaltma seçenekleri sun |
| n+4 | Riskler (`riskmatrix.svg`) | Ters giderse ne olur |
| n+5 | Paralellik (`capacity.svg`) + ekip | Kapasite tartışmasını darboğaza çevir |
| n+6 | **Sizden beklenenler** | Müşteri tarafındaki kritik yol |
| n+7 | **Bugün karar verilecekler** | Toplantıyı bitiren slayt |

3, n+6 ve n+7 zorunlu. Karar talebi olmayan sunum toplantıyı bitirmez, sadece durdurur.

## Slayt yazım kuralları

- Slayt başına tek fikir. İki fikir varsa iki slayt.
- Satır başına en fazla ~12 kelime, metin slaytında en fazla 6 satır.
- Görsel slaytlarında `<!-- _class: visual -->` kullan; görsel tam genişliğe yayılır, yanına metin koyma.
- Effort'u aralık göster (P50–P80). Tek sayı sahte kesinlik yaratır.
- Takvim tarihi yazma (istenmedikçe). Sprint numarası kullan.
- Sayıların yanına dayandığı varsayımı yaz: "4 kişi · 10 günlük sprint · 0.65 odak".
- Riski gizleme. En yüksek üç riski açıkça göster — sunumun güvenilirliği buradan gelir.
- `.callout` bloğunu slayt başına en fazla bir kez kullan; her yerde varsa hiçbir yerde vurgu kalmaz.

## Tema

`assets/theme.css`. Marp'a `--theme` ile verilir. Sağladığı sınıflar:

| Sınıf | Kullanım |
|---|---|
| `<!-- _class: lead -->` | Kapak slaytı |
| `<!-- _class: visual -->` | Tam genişlik görsel slaytı |
| `.kpi` | Yan yana metrik kartları (2–4 tane) |
| `.callout` | Vurgulanan tek paragraf |
| `.callout.risk` | Kırmızı kenarlı uyarı |
| `.callout.ask` | Turuncu kenarlı, müşteriden istenen |
| `.muted` `.risk` `.warn` `.ok` | Satır içi renk vurguları |

Renkleri değiştirmen gerekirse `theme.css` içindeki `:root` değişkenlerini ve `render_visuals.py` başındaki paleti **birlikte** güncelle; ikisi aynı renkleri kullanır.

## Sunum ve roadmap.md arasındaki iş bölümü

| | `roadmap.md` | PDF sunum |
|---|---|---|
| İzleyici | Teknik ekip + PM | Müşteri + ekip birlikte |
| Amaç | Referans, tek doğruluk kaynağı | Tartışma ve karar |
| Detay | Tam: her iş, her dependency | Faz seviyesi |
| Effort | İş bazında | Faz toplamı |
| Risk | Tam tablo | En kritik 3–5 |
| Changelog | Var | Yok (son değişiklikler tek slayt olabilir) |

Sunumu `roadmap.md`'nin kısaltılmış hâli olarak üretme. Farklı soruya cevap veriyorlar.
