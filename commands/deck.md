---
description: plan.json'dan müşteriye sunulabilir görsel PDF üretir
argument-hint: [opsiyonel: customer | delivery]
---

`roadmap-architect` skill'ini kullan. Önce `references/audience.md`, sonra `references/deck.md` oku.

Kitle: $ARGUMENTS (belirtilmemişse `customer`)

1. `plan.json` yoksa `/roadmap` çalıştırılması gerektiğini söyle ve dur.
2. Müşteri kitlesi için `customer_outcome`, `customer_name`, `customer_text` alanlarının dolu olduğunu doğrula. Eksikse önce onları yaz — boş bırakılırsa teknik adlar kullanılır ve sunum müşteriye kapalı hale gelir.
3. Hesap ve görseller:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/scripts/plan_capacity.py plan.json
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/scripts/render_visuals.py plan.json --out docs/assets --audience customer
   ```
4. `docs/roadmap-deck.md` yaz — `assets/deck.template.md` şablonundan, slayt sırasını bozmadan. "Bu planda YOK", "Sizden beklenenler" ve "Bugün karar verilecekler" slaytları zorunlu.
5. PDF:
   ```bash
   npx --yes @marp-team/marp-cli@latest docs/roadmap-deck.md \
     --theme ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/assets/theme.css \
     --allow-local-files --pdf -o docs/roadmap-deck.pdf
   ```
   Tarayıcı yoksa `--html` ile üret ve kullanıcıya tarayıcıdan "PDF olarak yazdır" demesini söyle.

Bitirince sohbette sunumun kaç slayt olduğunu ve hangi üç kararın talep edildiğini yaz.
