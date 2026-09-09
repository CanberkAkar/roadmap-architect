# Changelog

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
