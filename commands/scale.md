---
description: Kaç agent, kaç kişi — kritik yol ve darboğaz analizi
argument-hint: [opsiyonel: faz adı]
---

`roadmap-architect` skill'ini, özellikle `references/agent-sizing.md` bölümünü kullan.

Kapsam: $ARGUMENTS

1. `python3 ${CLAUDE_PLUGIN_ROOT}/skills/roadmap-architect/scripts/plan_capacity.py plan.json`
2. Stream ayrımını repo'nun gerçek modül sınırlarıyla karşılaştır. Paylaşılan şema, ortak tipler ve migration'lar tek stream'e ait olmalı — ayrıysa düzelt ve yeniden hesapla.
3. Faz bazlı tabloyu üret: paralel iş, önerilen agent, sınırlayan kısıt.

Cevabı üç cümleyle kur, sadece sayı verme:
1. Bu fazda N iş bağımsız yürüyebiliyor.
2. Bunu X'e düşüren şey: <darboğaz>.
3. X'i artırmak için yapılması gereken: <eylem>.

Sayı 8'i geçmesin; pratikte iyi çalışan aralık 2–4. Discovery ve walking skeleton fazlarında 1–2'de kal.
