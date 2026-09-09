# Changelog

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
