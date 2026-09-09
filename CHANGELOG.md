# Changelog

## 0.7.0

- **journey.svg metin taşması düzeltildi** — faz kartlarındaki sabit y-koordinatları
  değişken satır sayısıyla çakışıp "BU AŞAMA BİTİNCE" ile "NASIL GÖRÜRÜZ" bloklarının
  üst üste binmesine yol açıyordu. Kart yüksekliği artık içerikteki en uzun metne göre
  dinamik hesaplanıyor; uzun aşama adı/açıklaması olan planlarda da taşma olmuyor.
- **Kapak tasarımı yenilendi** — koyu lacivert degrade zemin, büyük beyaz başlık,
  parlak mavi slogan, köşelerde yumuşak ışık aksanları. Daha çarpıcı ilk izlenim.
- **"Sonraki adım" slaydına slogan eklendi** — kapanışta slogan tekrar vurgulanıyor
  (`.tagline` sınıfı, kapak ve kapanışta ortak kullanılıyor), sunum kendi içinde
  slogan ile açılıp slogan ile kapanıyor.
- **Rakip analizi derinleştirildi** — her rakibe `pricing` (fiyatlandırma) ve
  `positioning` (pazar konumu) alanları eklendi; "Neden biz" tablosuna Fiyat sütunu,
  örnek plana üçüncü bir alternatif ("hiçbir şey yapmamak") eklendi.
- **Gerçek pazar araştırması zorunlu kılındı** — discovery'ye "Dış dünyayı da araştır"
  adımı eklendi: gerçek bir ürün/şirket/sektör söz konusuysa `business_case` ve
  `competitive_analysis` WebSearch ile araştırılan bilgiye dayanmalı, uydurulmamalı.

## 0.6.0

- **Rakip analizi ve işletme gideri artık varsayılan olarak beklenir** — teknik olarak
  hâlâ opsiyonel alanlardır ama discovery sırasında aktif olarak araştırılıp
  doldurulmaları beklenir; sadece gerçekten imkansızsa atlanır.
- **Büyüme projeksiyonu (`growth_projection`)** — yeni alan: hayata geçtikten sonra
  3/6/12 ayda birikmiş müşteri sayısı ve gelir. `plan_capacity.py` dönemler arası net
  artışı hesaplar; `render_visuals.py` bunu `growth.svg` (çift panelli **sütun grafik**)
  olarak çizer. Yeni "Büyüme projeksiyonu" slaydı, `cost_estimate`'ten sonra.
- **Slogan (`slogan`)** — yeni alan: kapak slaydı için seçilen slogan + alternatif
  öneriler. Kapak slaydında proje adının altında öne çıkan bir başlık olarak gösterilir;
  alternatifler `roadmap.md`'de referans olarak durur.
- **`cost.svg` pasta (donut) grafiğe çevrildi** — eskiden yatay çubuklardı, artık
  kalemlerin yüzdesel dağılımını merkezde toplam tutarla birlikte gösteren bir donut.
- **Tasarım sadeleştirmesi** — `journey.svg`, `riskmatrix.svg`, `deadline.svg`
  içindeki başlıklar Marp slaytının kendi başlığıyla çakıştığı için kaldırıldı, o alan
  grafiğe verildi (daha büyük, daha net görseller). İçerik slaytlarına köşe aksanı
  eklendi (boş alanı dolduran hafif dairesel vurgu). KPI kartları ve callout'lar
  büyütüldü, ince gölge eklendi.
- Risk slaydındaki görsel+callout kombinasyonunun taşma yaptığı düzeltildi — callout
  kaldırıldı (grafik zaten her risk için azaltma bilgisini taşıyor), risk matrisi
  daraltıldı.
- `references/discovery.md`, `references/deck.md`, `references/audience.md`,
  `SKILL.md`, `README.md` yeni alanlara ve varsayılan bekleme kuralına göre güncellendi.

## 0.5.0

- **Deck felsefesi değişti: toplantı dokümanından pitch'e.** Müşteriye/yatırımcıya sunulan
  PDF artık tek yönlü, ikna edici bir sunumdur — bir onay/karar toplama toplantısı dokümanı
  değil. Kaldırılanlar: "Bu planda YOK" (kapsam dışı), "Sizden beklenenler" (müşteriden
  istenen işler), "Bugün karar verilecekler" (karar/onay listesi). Bu içeriğin tamamı
  `roadmap.md`'de tam olarak kalıyor, sadece deck'ten çıktı.
- **Yeni "Yatırım ve getiri" slaydı** — `cost.svg` ile `business_case.expected_impact`'i
  yan yana gösterir; eskiden ayrı duran "İşletme gideri" slaydının yerini aldı.
- **"İş değeri" → "Fırsat"**, **"Neyin ters gidebileceği" → "Riskler ve yönetimi"** olarak
  yeniden adlandırıldı — endişe değil güven çerçevesi.
- Deck'ten `timeline.svg`, `depgraph.svg`, `capacity.svg` ve bunlara bağlı slaytlar
  ("Zaman şeridi", "Neyin neyi beklediği", "Neden daha hızlı olmuyor", "Ekip ve hız")
  çıkarıldı — bunlar yürütme/kapasite detayıdır, artık sadece `roadmap.md`'de ve
  `--audience delivery` görsel setinde yaşıyor.
- **Belirsizlik deck'te gösterilmiyor** — `success_metric.baseline` veya opsiyonel alanlar
  "bilinmiyor"/boşsa ilgili KPI kartı veya slayt tamamen çıkarılıyor, sahte bir değerle
  doldurulmuyor. `roadmap.md` belirsizliği hep tam gösteriyor.
- `references/deck.md`, `references/audience.md`, `references/discovery.md`,
  `commands/deck.md` bu felsefeye göre güncellendi.

## 0.4.0

- **Rakip analizi (`competitive_analysis`)** — opsiyonel alan: benzer ürünler/alternatifler
  (güçlü/zayıf yanları) ve bizim somut farkımız. Doldurulursa sunumda "Neden biz" slaydı ve
  `roadmap.md`'de karşılık bölümü otomatik açılır.
- **İşletme gideri (`cost_estimate`)** — opsiyonel alan: tek seferlik kurulum maliyeti ve
  aylık işletme gideri (sunucu/hosting, üçüncü parti servisler, reklam/pazarlama vb.).
  `plan_capacity.py` kalemleri toplayıp aylık/yıllık toplamı hesaplar; `render_visuals.py`
  bunu `cost.svg` olarak kalem kalem çizer.
- İkisi de girilmezse ilgili slayt/bölüm/görsel sessizce atlanır, mevcut planlar değişmeden
  çalışır.
- Discovery akışına "Rakip analizi ve işletme gideri" adımı eklendi. `references/discovery.md`
- Toplantı ve slayt sırası güncellendi: Neden biz ve İşletme gideri, İş değerinden sonra
  eklendi. `references/audience.md`, `references/deck.md`

## 0.3.0

- **İş değeri (`business_case`)** — opsiyonel alan: problem, fırsat, beklenen etki, yapılmazsa.
  Doldurulursa sunumda "İş değeri: neden şimdi" slaydı ve `roadmap.md`'de "İş değeri"
  bölümü otomatik açılır.
- **Teslim güvenilirliği (`deadline`)** — opsiyonel alan: elinizdeki süre (`days_available`)
  ve nedeni (`driver`). `plan_capacity.py` kritik yolla karşılaştırıp tampon gün/yüzde ve
  Rahat/Sıkışık/Riskli durumu hesaplar; `render_visuals.py` bunu `deadline.svg` olarak çizer.
  İkisi de girilmezse sessizce atlanır, mevcut planlar bozulmadan çalışmaya devam eder.
- Discovery akışına "Talebi analiz et" adımı eklendi: söylenen talep vs altında yatan ihtiyaç,
  `business_case`'in hammaddesi. `references/discovery.md`
- Toplantı sırası ve slayt sırası güncellendi: İş değeri (2. sıra) ve Teslim güvenilirliği
  (kritik yoldan sonra) eklendi. `references/audience.md`, `references/deck.md`

## 0.2.1

- Skill yeniden adlandırıldı: `skills/roadmap-architect/` → `skills/roadmaps/`, `SKILL.md` frontmatter'ı `name: roadmaps`. Plugin/repo adı `roadmap-architect` olarak kalıyor.

## 0.2.0

- **Ortak dil katmanı** — `plan.json` içinde `customer_outcome` / `customer_name` / `customer_text`
  alanları. Aynı plandan müşteri ve teknik ekip için iki görünüm üretiliyor.
  Kurallar ve terim çeviri tablosu: `references/audience.md`
- **Görselleştirici** — `render_visuals.py`, `plan.json`'dan beş SVG üretiyor:
  faz yolculuğu, sprint zaman şeridi, bağımlılık haritası (kritik yol vurgulu),
  risk matrisi, kapasite/paralellik
- **Sunum teması** — `assets/theme.css`, Marp ile görselli PDF
- `/deck` komutu eklendi
- Müşteri tarafındaki işler (`owner: "customer"`) artık kritik yol hesabına dahil

## 0.1.0

- İlk sürüm: discovery → faz/milestone → risk & dependency → sprint → ölçekleme → revizyon
- `plan_capacity.py`: kritik yol, paralelleşebilirlik indeksi, agent önerisi, sprint dağılımı
