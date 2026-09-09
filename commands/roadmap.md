---
description: Business hedefinden fazlara, milestone'lara ve risk planına kadar roadmap üretir
argument-hint: [hedef veya proje adı]
---

`roadmap-architect` skill'ini kullan. Müşteriye gidecek herhangi bir şey yazmadan önce `references/audience.md` oku — bu plan hem müşterinin hem teknik ekibin okuyacağı tek bir dokümandır.

Hedef/bağlam: $ARGUMENTS

Sırayla:

1. **Repo'yu tara** — README, bağımlılık manifestleri, klasör yapısı, CI config, migration'lar, son commit'ler. Teknik gerçekliği kendin çıkar.
2. **Discovery** — `references/discovery.md`. Hedef, başarı kriteri ve kısıtlar netleşmeden faz üretme. Bulgularını doğrulatmak için sor, sıfırdan bilgi toplamak için değil.
3. **Faz ve milestone** — `references/phasing-and-risk.md`. Dikey dilimler, katman değil. Yüksek riskli ve kritik bağımlı işleri erken doğrulamaya çevir (spike / walking skeleton / sözleşme testi) ve her birine karar noktası yaz.
4. **`plan.json` üret** — `assets/plan.template.json` şemasına göre. Tek veri kaynağı budur. Her faz için `customer_outcome`, müşteriye görünecek işler için `customer_name`, riskler için `customer_text` doldur. Müşteri tarafındaki işleri de (`owner: "customer"`) plana gir — bunlar çoğu zaman gerçek kritik yoldur.
5. **Hesapla** — `python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/scripts/plan_capacity.py plan.json`
6. **Görseller** — `python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/scripts/render_visuals.py plan.json --out docs/assets --audience customer`
7. **Çıktılar** — `docs/roadmap.md` (referans) + `docs/roadmap-deck.md` + `docs/roadmap-deck.pdf` (müşteri sunumu). PDF adımı için `/deck` komutundaki Marp çağrısını kullan.

Ölçeği effort toplamından kendin belirle (S/M/L/XL) ve yapının ağırlığını ona göre ayarla. Küçük projeye 12 slaytlık sunum üretme.

Bitirince sohbette 5 satırlık özet ver: hedef, faz sayısı, kritik yol, minimum sprint, önerilen agent sayısı ve bunu sınırlayan darboğaz.
