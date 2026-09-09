---
description: Mevcut plan.json'dan sprint planı çıkarır
argument-hint: [opsiyonel: sprint sayısı veya faz adı]
---

`roadmap-architect` skill'ini, özellikle `references/sprint-planning.md` bölümünü kullan.

Kapsam: $ARGUMENTS

1. `plan.json`'ı oku. Yoksa önce `/roadmap` çalıştırılması gerektiğini söyle ve dur.
2. `python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmaps/scripts/plan_capacity.py plan.json --json > .roadmap/capacity.json`
3. Sprint kartlarını üret. Her sprintin bir **kanıtı** olmalı — yazılamıyorsa o sprint yanlış kurulmuş.
4. İlk sprint kapasitesinin en az yarısını riskli spike'lara, uzun lead time'lı dış bağımlılıkların tetiklenmesine ve ortam/CI'ın çalışır hale gelmesine ayır.
5. Kapasitenin %15–20'sini planlanmamış bırak.
6. Script'in "dependency zinciri bağlıyor" uyarısı verdiği sprintlerde boşta kalan kapasite için somut öneri yaz.

Çıktı: `docs/sprints.md` + sohbette ilk sprintin özeti.
