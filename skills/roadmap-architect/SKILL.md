---
name: roadmap-architect
description: Bir urun veya projeyi business hedefinden baslayip fazlara, milestone'lara, sprint planina ve agent/ekip olceklendirmesine kadar planlar; sonucu hem musterinin hem teknik ekibin ayni masada okuyabilecegi gorsel bir PDF ve Markdown olarak uretir; mevcut roadmap'i yeni feedback, teknik bulgu veya oncelik degisikligine gore gunceller. Kullanici "roadmap", "yol haritasi", "faz", "milestone", "sprint plani", "kapasite", "kac agent", "kac kisi", "projeyi planla", "musteriye sunum", "teklif", "proje plani", "nereden baslayalim", "bu isi nasil boleriz" gibi seylerden bahsettiginde MUTLAKA bu skill'i kullan. Ayrica buyuk bir feature veya sifirdan bir proje icin uygulama sirasi, oncelik ya da musteriyle hizalanma soruldugunda da kullan; kullanici "roadmap" kelimesini kullanmasa bile. Sadece tek bir task'in nasil yapilacagi soruluyorsa kullanma.
---

# Roadmap Architect

Roadmap bir task listesi değildir. Ürünün hangi aşamalardan geçerek business hedefine ulaşacağını gösteren üst seviye bir plandır, sabit değil yaşayan bir dokümandır.

**Bu skill'in asıl işi iki tarafı aynı sayfada buluşturmak:** müşteri "ne alacağım, ne zaman, neden bu sırayla" görür; teknik ekip aynı plandan çalışır. Bu yüzden iki ayrı doküman üretilmez — tek bir `plan.json` üretilir, iki dille sunulur. Dil kuralları ve teknik terim → müşteri dili çevirisi: `references/audience.md`. Müşteriye gidecek herhangi bir şey yazmadan önce bu dosyayı oku.

## Modlar

| Mod | Ne zaman | Nereye bak |
|---|---|---|
| **Discovery** | Hedef net değil, roadmap yok | `references/discovery.md` |
| **Planla** | Hedef net, faz/milestone çıkarılacak | `references/phasing-and-risk.md` |
| **Sprint'e dök** | Roadmap var, icra planı isteniyor | `references/sprint-planning.md` |
| **Sun** | Müşteri/ekip toplantısı için PDF | `references/deck.md` |
| **Güncelle** | Roadmap var, gerçeklik değişti | `references/revision.md` |

Ölçeklendirme ve agent sayısı her modda devreye girer: `references/agent-sizing.md`.

## Temel kural: hedef netleşmeden faz çıkarma

Aşağıdaki üçü elinde yoksa faz üretmeye başlama. Tahmin etme, sor:

1. **Business hedefi** — ne değişecek? ("checkout conversion'ı artırmak", "on-prem müşterilere satabilmek")
2. **Beklenen sonuç / başarı metriği** — nasıl ölçeceğiz, hangi eşikte başarılı sayıyoruz?
3. **Kısıtlar** — deadline, ekip, bütçe, uyum/regülasyon, dokunulmaz sistemler

"Bir e-ticaret sitesi yapalım" bir hedef değil, bir çıktı tanımıdır. Hedefi bunun arkasında ara.

Repo'ya erişimin varsa discovery'yi boş sayfadan başlatma: `README`, bağımlılık manifestleri, klasör yapısı, migration'lar, CI config ve varsa `docs/` altını oku. Teknik gerçekliği kendin çıkar, sonra doğrulat.

## Akış

### 1. Hedefi ve sonucu netleştir
`references/discovery.md`. Çıktı: tek cümlelik hedef + ölçülebilir başarı kriteri + kısıt listesi + kapsam dışı + açık varsayımlar.

### 2. Fazlara ve milestone'lara böl
Her faz bir **durum değişikliği** anlatmalı ("ödeme akışı canlıda, tek ülke"), bir iş yığını değil ("backend işleri"). Her faz için zorunlu alanlar:

- **Amaç** (`purpose`) — teknik ekibe: bu faz bittiğinde sistem hangi noktada
- **Müşteri çıktısı** (`customer_outcome`) — müşteriye: bu aşama bitince ne yapabilir hale geliyor
- **Milestone** — bittiğini nasıl anlarız; demo edilebilir veya ölçülebilir kanıt
- **Öncelik** — hedefe katkı × aciliyet
- **Dependency** — hangi fazlara / dış aktörlere bağlı
- **Effort** — ideal insan-günü, aralık olarak (P50–P80)
- **Risk** — teknik / bağımlılık / ürün belirsizliği, seviye + neden
- **Beklenen çıktı** — kim ne alacak

Detay ve risk sınıflandırması: `references/phasing-and-risk.md`.

### 3. Riskli ve kritik bağımlı işleri öne çek
Bu adım atlanırsa roadmap kâğıt üstünde kalır. Yüksek riskli veya kritik bağımlı işleri tam implementasyon olarak değil, **doğrulama işi** olarak erken fazlara koy: spike (ön çalışma), walking skeleton, sözleşme testi.

Her doğrulama işine bir **karar noktası** yaz: sonuç negatif çıkarsa roadmap nasıl değişir? Yazılmadıysa doğrulama işi eksiktir — ve bu, müşteriye anlatılacak en değerli cümledir.

**Müşteri tarafındaki işleri de plana gir** (`owner: "customer"`). SSO bilgisi, test kullanıcısı, içerik, onay — bunlar çoğu zaman gerçek kritik yoldur ama plana yazılmadıkları için görünmezler.

### 4. Planı makine-okunur hale getir
`assets/plan.template.json` şemasına göre `plan.json` üret. Bu dosya sprint planının, kapasite hesabının, görsellerin ve sunumun tek kaynağıdır — sayıları elle ikinci kez yazma.

Müşteriye gidecek her faz ve her yüksek riskli iş için `customer_outcome`, `customer_name`, `customer_text` alanlarını doldur. Boş bırakılırsa teknik ad kullanılır ve sunum müşteriye kapalı hale gelir.

### 5. Kapasite, sprint ve agent sayısını hesapla
Aritmetiği kafadan yapma:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmap-architect/scripts/plan_capacity.py plan.json
```

Toplam effort, kritik yol, paralelleşebilirlik indeksi, önerilen eşzamanlı agent sayısı, minimum sprint sayısı ve sprint dağılımı verir. Yorumlaması `references/agent-sizing.md`.

Sayıyı olduğu gibi aktarma — **neden** o sayı olduğunu ve neyin onu değiştireceğini yaz.

### 6. Görselleri üret
Müşteriyle hizalanma tabloyla değil şekille olur:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmap-architect/scripts/render_visuals.py plan.json \
  --out docs/assets --audience customer
```

Beş SVG üretir: `journey` (faz yolculuğu), `timeline` (sprint zaman şeridi), `depgraph` (bağımlılık + kritik yol), `riskmatrix` (etki × olasılık), `capacity` (paralellik ve agent). `--audience delivery` aynı plandan teknik adlarla ikinci bir set üretir.

### 7. Çıktıları üret
Her zaman üçü birden:

**a) `docs/roadmap.md`** — `assets/roadmap.template.md`. Referans doküman, repo'da versiyonlanır. Tabloları tek satırda tut, diff'lenebilir kalsın.

**b) `docs/roadmap-deck.md`** — `assets/deck.template.md` (Marp). Görselleri gömer.

**c) `docs/roadmap-deck.pdf`** — sunum PDF'i:

```bash
npx --yes @marp-team/marp-cli@latest docs/roadmap-deck.md \
  --theme ${CLAUDE_PLUGIN_ROOT}/skills/roadmap-architect/assets/theme.css \
  --allow-local-files --pdf -o docs/roadmap-deck.pdf
```

`--allow-local-files` olmadan SVG'ler gömülmez. PDF üretimi tarayıcı gerektirir; ortamda yoksa `--html` ile HTML üret ve kullanıcıya tarayıcıdan "PDF olarak yazdır" demesi gerektiğini söyle. Sunum yapısı ve slayt kuralları: `references/deck.md`.

### 8. Roadmap'i yaşayan tut
`references/revision.md`. Değişikliği `docs/roadmap.md` changelog'una yaz, `plan.json`'ı güncelle, script'leri yeniden çalıştır. Eski fazı sessizce silme — durumunu değiştir ve nedenini bırak.

Müşteriye giden güncelleme özeti üç satırı geçmesin: **ne değişti · plana etkisi · sizden gereken**.

## Ölçek

Projenin boyutuna göre ne kadar yapı kuracağını ayarla. Yanlış ölçek planı işe yaramaz hale getirir:

| Ölçek | Toplam effort | Faz | Sprint | Çıktı |
|---|---|---|---|---|
| **S** | < 20 insan-günü | 1–2 | Sprint yok | Tek sayfa MD, `journey` görseli, PDF yok |
| **M** | 20–80 | 3–4 | 1 hafta | MD + 8–10 slayt PDF |
| **L** | 80–300 | 4–6 | 2 hafta | MD + tam PDF + stream bazlı sprint dağılımı |
| **XL** | > 300 | 5–8 | 2 hafta | Yukarıdakiler + faz bazlı ayrı plan dosyaları |

Ölçeği kullanıcıya sorma, effort toplamından kendin çıkar; sınırdaysa hangi tarafa yuvarladığını belirt.

## Sık yapılan hatalar

- **İki ayrı doküman üretmek** — müşteri sunumu ve teknik plan ayrılırsa biri güncellenir diğeri unutulur, iki taraf farklı gerçekliklerde yaşamaya başlar. Tek `plan.json`, iki görünüm.
- **Sadeleştirmeyi saklamakla karıştırmak** — riskler, belirsizlik ve müşteriden beklenenler müşteri görünümünde aynen durur. Riski önceden söylemiş olmak, gerçekleştiğinde tartışmayı "neden olmadı"dan "hangi seçeneği seçiyoruz"a çevirir.
- **Faz yerine katman bölmek** — "Faz 1: veritabanı, Faz 2: API, Faz 3: UI". Hiçbiri tek başına hedefe yaklaştırmaz ve risk son fazda toplanır. Dikey dilimlere böl.
- **Effort'u tek sayı vermek** — belirsizliği gizler. Aralık ver; aralığın genişliği zaten risk sinyalidir.
- **Dependency'yi sadece iç işler arasında aramak** — dış ekip onayı, satın alma, yasal inceleme, müşteriden gelecek bilgi çoğu zaman gerçek kritik yoldur.
- **Tarih vermek** — istenmedikçe takvim tarihi yazma. Sprint numarası ve effort ver; tarihe çevirmek birlikte alınacak bir karardır.
- **Agent sayısını effort'a bölerek bulmak** — kritik yol ve çakışma sınırı hesaba katılmazsa çıkan sayı yanlıştır. Script'i çalıştır.
