---
marp: true
theme: roadmap
paginate: true
size: 16:9
header: ''
footer: '{{Proje adı}} · yol haritası · {{tarih}}'
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _footer: '' -->

# {{Proje adı}}

## {{Müşterinin diliyle tek cümlelik hedef}}

<span class="muted">{{tarih}} · sürüm {{n}} · Bu bir tartışma dokümanıdır — onay ve itiraz için</span>

---

## Neden bu proje

<div class="kpi">
<div><div class="n">{{3 hafta}}</div><div class="l">Bugün: yeni müşteri devreye alma süresi</div></div>
<div><div class="n">{{2 gün}}</div><div class="l">Hedef</div></div>
<div><div class="n">{{Aşama 4}}</div><div class="l">Bu farkı ne zaman ölçeriz</div></div>
</div>

<div class="callout">
{{Bugün ne oluyor ve bunun somut maliyeti ne — tek paragraf, teknik terim yok}}
</div>

---

## Bu planda YOK

| Kapsam dışı | Neden |
|---|---|
| {{madde}} | {{gerekçe}} |
| {{madde}} | {{gerekçe}} |

<div class="callout ask">
İtirazınız varsa bu slaytta söyleyin. Sonraki aşamalarda kapsam eklemek planı en çok geciktiren şeydir.
</div>

---

<!-- _class: visual -->

## Ürün hangi aşamalardan geçiyor

![](assets/journey.svg)

---

## Aşama {{n}} · {{Müşteri diliyle aşama adı}}

### Bu aşama bitince
{{Müşterinin yapabildiği yeni şey — tek cümle}}

### Nasıl görürüz
{{Demo, ölçüm veya rapor — somut kanıt}}

| | |
|---|---|
| Süre | {{18–26}} iş günü |
| Sizden gereken | {{şey ve ne zaman — yoksa "yok"}} |
| Ana risk | <span class="risk">{{risk, müşteri diliyle}}</span> |

---

<!-- _class: visual -->

## Zaman şeridi

![](assets/timeline.svg)

---

<!-- _class: visual -->

## Neyin neyi beklediği

![](assets/depgraph.svg)

---

## Neden daha hızlı olmuyor

<div class="callout">
Kırmızı zincir <strong>kritik yol</strong>: sırayla yapılması zorunlu işler.
Toplam <strong>{{40}} iş günü</strong>. Bu zincir kısalmadan proje daha hızlı bitmez —
ekibe kişi eklemek de kısaltmaz.
</div>

### Zinciri kısaltmanın yolları
- {{somut seçenek 1 — kazanç ve bedeliyle}}
- {{somut seçenek 2}}

---

<!-- _class: visual -->

## Neyin ters gidebileceği

![](assets/riskmatrix.svg)

---

<!-- _class: visual -->

## Aynı anda kaç iş yürüyebilir

![](assets/capacity.svg)

---

## Ekip ve hız

<div class="callout">
Bu aşamada birbirinden bağımsız yürüyebilecek <strong>{{5}}</strong> iş var.
Aynı anda <strong>{{3}}</strong> tanesini yürütüyoruz, çünkü {{darboğaz — sade dille}}.
Dördüncüye çıkmak için {{gereken somut şey}}.
</div>

| Aşama | Paralel iş | Yürütülen | Sınırlayan |
|---|---|---|---|
| {{Aşama 1}} | {{1.8}} | {{2}} | {{işin sırası}} |
| {{Aşama 3}} | {{3.1}} | {{3}} | {{ekip sayısı}} |

---

## Sizden beklenenler

| Ne | Ne zaman | Gecikirse |
|---|---|---|
| {{şey}} | Sprint {{n}} | {{plan ne kadar kayar}} |
| {{şey}} | Sprint {{n}} | {{...}} |

<span class="muted">Bu maddeler kritik yol hesabına dahildir — gecikmeleri doğrudan teslim tarihine yansır.</span>

---

## Bugün karar verilecekler

1. **{{Karar}}** — kim: {{rol}}
2. **{{Onay}}** — kim: {{rol}}
3. **{{Aksiyon}}** — kim: {{rol}}, ne zaman: {{Sprint 1}}

<div class="callout ask">
Yol haritası her iki haftada bir güncellenir. Değişiklikler üç satırlık özetle paylaşılır:
ne değişti · plana etkisi · sizden gereken.
</div>
