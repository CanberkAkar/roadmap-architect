# Discovery: hedefi ve beklenen sonucu netleştirme

Amaç, kullanıcıyı sorgulamaya boğmak değil. Çoğu kişi hedefi biliyordur ama çıktı diliyle anlatır ("bir dashboard lazım"). İşin, arkasındaki değişimi ortaya çıkarmak.

## Önce kendin çıkar

Repo erişimin varsa soru sormadan önce şunları oku:

- `README`, `docs/`, `CONTRIBUTING`
- Bağımlılık manifesti (`package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `Gemfile`)
- Klasör yapısı ve modül sınırları — bunlar ileride agent çakışma alanlarını belirleyecek
- CI/CD config, deploy script'leri — release mekanizması roadmap'in son fazını şekillendirir
- `migrations/`, şema dosyaları — veri modeli değişimi genelde en yüksek riskli dependency
- Son 20–30 commit ve açık PR'lar — ekibin şu an nerede olduğunu gösterir

Sonra bulgularını **doğrulatmak için** sor, sıfırdan bilgi toplamak için değil. "Auth şu an Keycloak üzerinden görünüyor, çok kiracılı yapıya geçişte bu kalacak mı?" — bu, "auth nasıl çalışıyor?" sorusundan çok daha verimlidir.

## Dış dünyayı da araştır

Repo içini incelemek yetmez — `business_case`, `competitive_analysis` ve `growth_projection` gerçek pazar bilgisine dayanmalı, uydurulmamalı. Kullanıcı gerçek bir ürün/şirket/sektör adı verdiğinde (ör. "X sektöründe Y'ye benzer bir ürün"), yazmadan önce **WebSearch/WebFetch ile araştır**:

- Bahsedilen rakip ürünler/şirketler — ne sunuyorlar, fiyatlandırmaları ne, hangi müşteri segmentine hitap ediyorlar
- Sektörün genel büyüklüğü, büyüme trendi, bilinen oyuncular
- Varsa ilgili haber, rapor veya pazar analizi

Bulduğun her rakamın/iddianın kaynağını `notes` alanlarına kısaca yaz (ör. "kaynak: X'in fiyatlandırma sayfası, 2026"). Araştırma sonuçsuz kalırsa ("bulamadım") bunu açıkça söyle ve kullanıcıdan doğrulama iste — uydurma rakamla doldurmaktansa "bilinmiyor, doğrulanmalı" demek daha güvenilirdir. Bu adım atlanırsa `competitive_analysis` ve `business_case` masa başında uydurulmuş gibi durur ve sunumun güvenilirliğini düşürür.

## Talebi analiz et

Müşterinin söylediği şey ("bir dashboard lazım") ile aslında istediği şey ("elimde hangi müşterinin ne kadar risk taşıdığını her sabah görmek istiyorum") genelde farklıdır. İkisini ayrı ayrı yaz:

- **Söylenen talep** — müşterinin kelimeleri, aynen
- **Altında yatan ihtiyaç** — bu talebin çözdüğü asıl problem ne
- **Neden şimdi** — bu talep neden bugün gündemde (rekabet, kayıp fırsat, regülasyon, büyüme hedefi)

Bu analiz `business_case`'in (iş değeri) hammaddesidir. Müşteriye "iş değeri" slaydı göstermeyecek olsan bile bu analiz roadmap'in önceliklendirmesini değiştirir: en yüksek iş değerini taşıyan aşama erken faza gelmelidir.

### İş fikrini derinlemesine analiz etmeden faza geçme

Roadmap üretimi bir faz listesi çıkarmaktan ibaret değildir — önce fikrin kendisini sorgula. Aşağıdakileri cevapsız bırakıp faza geçme:

- **Problem gerçek mi, kim hissediyor, ne sıklıkla?** — "birinin işine yarar" yetmez, somut bir kişi/rol ve somut bir an tarif et
- **Hedef kitle/segment net mi?** — "herkes" bir segment değildir; kim önce, kim sonra
- **Neden şimdi, neden bu şekilde işe yarayacak?** — zamanlamayı ve yaklaşımı haklı çıkaran ne (teknolojik olgunluk, regülasyon, rakip boşluğu, maliyet düşüşü)
- **Pazar bağlamı araştırıldı mı?** — Türkiye ve global ölçekte bu fikrin karşılığı var mı (bkz. "Dış dünyayı da araştır" ve aşağıdaki "Türkiye ve global etki")
- **Alternatifler/rakipler incelendi mi?** — kimse bunu hiç denememişse bu bir bulgudur, nedenini sorgula (pazar yok mu, yoksa henüz kimse denemedi mi)

Bu sorulardan biri cevapsızsa roadmap kağıt üstünde iyi görünüp gerçekte temelsiz kalır. Cevapsız kalan soruyu "açık varsayım" olarak yaz, tahmin ederek kapatma.

## Netleşmesi gereken üç şey

### 1. Business hedefi
Tek cümle, ölçülebilir bir değişim içermeli.

- Zayıf: "Mobil uygulama yapmak"
- İyi: "Mevcut web müşterilerinin sipariş tekrarını mobilde artırmak"

Kullanıcı çıktı diliyle konuşuyorsa iki kez "bu ne sağlayacak?" diye sor. Üçüncüde bırak ve varsayımını açıkça yazıp doğrulat.

### 2. Beklenen sonuç
Metrik + yön + kaba eşik + ölçüm zamanı. Eşik bilinmiyorsa "baseline'ı bilmiyoruz" bir bulgudur ve **ölçümü kurmak roadmap'in ilk fazıdır**.

### 3. Kısıtlar
Sorulmazsa sonradan roadmap'i çöpe atan şeyler:

- Sabit tarih var mı, varsa neye bağlı (fuar, sözleşme, regülasyon yürürlük tarihi)?
- Ekip: kaç kişi, hangi roller, ne kadarı bu projeye ayrılmış?
- Dokunulamayacak sistemler, dondurulmuş dönemler (code freeze), migration yasakları
- Uyum/regülasyon: KVKK/GDPR, PCI, sektörel denetim
- Bütçe ve satın alma süreci — lisans/servis alımı çoğu zaman haftalar süren gizli bir dependency

Sabit tarih varsa **bugünden o tarihe kaç iş günü kaldığını** say — bu sayı `plan.json`'daki `deadline.days_available` alanına gider ve kritik yolla otomatik karşılaştırılır. Tarihe bağlı gerekçeyi de yaz (`deadline.driver`): "neden bu tarih" sorusuna müşteriye karşı cevapsız kalınmaz.

## İş değeri ve deadline'ı plana yaz

"Talebi analiz et" bölümündeki bulgular `plan.json`'a iki alan olarak girer, ikisi de opsiyoneldir ama girilirse sunumda otomatik birer slayt/görsel açar:

```json
"business_case": {
  "problem": "<bugün ne oluyor ve somut maliyeti>",
  "opportunity": "<talep büyüklüğü — kaç aday, kaç kullanıcı, hangi pazar>",
  "expected_impact": "<ölçülebilir, mümkünse rakamlı beklenen etki>",
  "cost_of_inaction": "<yapılmazsa ne olur>"
},
"deadline": {
  "days_available": <bugünden deadline'a iş günü>,
  "driver": "<tarih neye bağlı>",
  "customer_text": "<müşterinin kendi ifadesiyle deadline>"
}
```

Rakam yoksa tahmin etme — "bilinmiyor" yaz ve bunu bir açık varsayım olarak kaydet. Sahte kesinlik, gerçek belirsizlikten daha kötüdür.

## Rakip analizi ve işletme gideri — varsayılan olarak doldur

Müşteri genelde "neden size, neden şimdi bu parayı vereyim" sorusunu içinden sorar ama nadiren yüksek sesle sorar. Aşağıdaki bölümler teknik olarak opsiyonel alanlardır ama pitch deck'te **varsayılan olarak beklenir** — "veri yoksa atlanır" istisnası, "sormaya üşendim" değildir. Discovery'de bunları aktif olarak araştır/tahmin et; sadece gerçekten hiçbir dayanak bulunamıyorsa alanı boş bırak.

**Rakip analizi** — en az 2-3 benzer çözümü (rakip ürün, mevcut süreç, "hiçbir şey yapmamak" dahil) **detaylı** değerlendir, tek cümlelik yüzeysel değerlendirme yetmez:

- **Fiyatlandırma** — bulabildiğin kadar somut (aylık/yıllık, kullanıcı başı, kurulum ücreti)
- **Pazar konumu** — kime hitap ediyor (KOBİ mi kurumsal mı, hangi sektör), ne kadar yerleşik
- **Güçlü yanı** — gerçekten iyi yaptığı şey, küçümsemeden
- **Zayıf yanı** — somut, doğrulanabilir eksik (iddia değil: "SSO desteklemiyor" evet, "kötü ürün" hayır)

Sonra kendi farkını yaz — iddia değil, somut fark ("2 gün vs 3 hafta", "mevcut kimlik sağlayıcıyla entegre"). Rakibi kötüleme, kendi farkını göster. Bilgi "Dış dünyayı da araştır" adımındaki WebSearch bulgularına dayanmalı; tahminse `note` alanında belirt.

```json
"competitive_analysis": {
  "competitors": [
    {
      "name": "<rakip/alternatif>",
      "pricing": "<bulunabildiyse somut fiyat, yoksa 'bilinmiyor'>",
      "positioning": "<kime hitap ediyor, pazardaki yeri>",
      "strengths": "<iyi yaptığı>",
      "weaknesses": "<yapamadığı>"
    }
  ],
  "our_advantages": ["<somut fark 1>", "<somut fark 2>", "<somut fark 3>"]
}
```

## SWOT analizi — varsayılan olarak doldur

Şu ana kadarki analizi (talep, iş değeri, rakipler) dört başlıkta sentezle — bu, "fikri gerçekten düşündük mü" sorusunun somut kanıtıdır. **Dürüst ol**: zayıf yön ve tehdit maddeleri kozmetik olursa ("en büyük zayıf yönümüz çok çalışkan olmamız" gibi) SWOT tüm sunumun güvenilirliğini düşürür.

- **Güçlü yönler** (`strengths`) — bizim elimizdeki somut avantaj (genelde `competitive_analysis.our_advantages` ile örtüşür)
- **Zayıf yönler** (`weaknesses`) — gerçekten eksik olduğumuz yer (küçük ekip, marka bilinirliği yok, referans müşteri yok — ne ise)
- **Fırsatlar** (`opportunities`) — dışarıdaki, bizim lehimize olan boşluk/trend (genelde `business_case.opportunity` ve `market_impact` ile beslenir)
- **Tehditler** (`threats`) — dışarıdaki, bize karşı işleyebilecek risk (rakip hamlesi, pazar değişimi, regülasyon)

Her başlıkta en fazla 3-5 madde — uzun liste okunmaz, en çarpıcı olanı seç.

```json
"swot": {
  "strengths": ["<madde 1>", "<madde 2>"],
  "weaknesses": ["<madde 1>", "<madde 2>"],
  "opportunities": ["<madde 1>", "<madde 2>"],
  "threats": ["<madde 1>", "<madde 2>"]
}
```

`render_visuals.py` bunu `swot.svg` (2x2 renkli panel) olarak çizer; en az bir kategori doluysa görsel üretilir.

## Türkiye ve global etki — varsayılan olarak doldur

Müşteri fikrin sadece kendi ofisinde değil, gerçek bir pazarda karşılığı olduğunu görmek ister. Türkiye ve global ölçekte ayrı ayrı, örneklerle göster — soyut "büyük bir pazar" ifadesi ikna etmez, somut isim ve rakam ikna eder:

- **Pazar büyüklüğü** — bulabildiğin kadar somut rakam (WebSearch ile), yoksa "bilinmiyor, tahmini yaklaşım: ..." de
- **Özet** — o pazarda bugün durum ne (oyuncu sayısı, doygunluk, büyüme trendi)
- **Örnekler** — en az 1-2 isimli girişim/şirket her bölge için (Türkiye'de benzer bir şey yapan, global ölçekte kategori lideri/öne çıkan oyuncu). İsim bulamazsan "bilinen bir örnek bulunamadı" yaz, icat etme.

```json
"market_impact": {
  "turkey": {
    "market_size": "<rakam, kaynağıyla>",
    "summary": "<Türkiye'de bugün durum>",
    "examples": ["<isimli girişim/şirket 1>", "<isimli girişim/şirket 2>"]
  },
  "global": {
    "market_size": "<rakam, kaynağıyla>",
    "summary": "<global pazarda bugün durum>",
    "examples": ["<isimli şirket 1>", "<isimli şirket 2>"]
  },
  "notes": "<rakamların kaynağı/güvenilirlik derecesi>"
}
```

`render_visuals.py` bunu `market_impact.svg` (iki panelli, örnekli kart görseli) olarak çizer; yalnızca `turkey` veya `global` alanlarından biri bile doluysa görsel üretilir.

## Ekip ve Traction — varsayılan olarak doldur

**Ekip** — özellikle SWOT'ta "küçük ekip" veya "referans yok" gibi bir zayıf yön çıktıysa, bunu dengeleyen somut bir karşı ağırlıktır. Her üye için gerçek bir deneyim/başarı cümlesi yaz — "yetenekli ekip" gibi boş sıfatlar değil, "X yıl Y alanında, önceki işinde Z'yi yaptı" gibi doğrulanabilir bir cümle.

```json
"team_members": [
  {"name": "<isim>", "role": "<rol>", "highlight": "<somut deneyim/başarı cümlesi>"}
]
```

**Traction** — `growth_projection` **gelecek tahminidir**; traction **şu anki gerçek kanıttır** — ikisi farklı işe hizmet eder, biri diğerinin yerine geçmez. Pilot kullanıcı sayısı, bekleme listesi, niyet mektubu (LOI), varsa gerçek bir kullanıcı alıntısı. Veri yoksa alan tamamen boş kalır — "henüz traction yok" diye bir kart uydurma, sadece atla.

```json
"traction": {
  "metrics": [{"label": "<ne>", "value": "<sayı>"}],
  "quote": {"text": "<gerçek bir kullanıcı ifadesi, varsa>", "source": "<kim>"}
}
```

`render_visuals.py` bunları `team.svg` (kart dizisi) ve `traction.svg` (stat kartları + alıntı) olarak çizer.

**İşletme gideri** — proje bittikten sonra sistemin **çalışır tutulmasının** aylık maliyeti: sunucu/hosting, üçüncü parti servisler (e-posta, SMS, izleme), reklam/pazarlama, lisans ücretleri. Tek seferlik kurulum maliyeti ayrı bir kalemdir (`one_time`), aylık işletme gideri ayrı (`recurring_monthly`). Kaba tahmindir demekten çekinme — rakam vermemekten daha güvenilirdir.

```json
"cost_estimate": {
  "currency": "USD",
  "one_time": [{"item": "<kurulum/geliştirme>", "amount": <sayı>, "note": "<nereden geldi>"}],
  "recurring_monthly": [{"item": "<sunucu/reklam/vb>", "amount": <sayı>, "note": "<varsayım>"}],
  "notes": "<tahminin ne kadar kaba olduğu>"
}
```

`amount` alanlarına tahmin bile olsa somut bir sayı yaz — `plan_capacity.py` bunları toplayıp aylık/yıllık toplamı ve `cost.svg` (pasta grafik) görselini otomatik üretir; elle toplama yapma.

## Büyüme projeksiyonu — varsayılan olarak doldur

Hayata geçtikten sonra 3/6/12 ay içinde ne kadar müşteri ve gelire ulaşılacağı, aynı `business_case.opportunity` (pipeline büyüklüğü) ve `cost_estimate` (reklam/satış gideri) rakamlarından türetilir — kafadan atma, dayandığın varsayımı `notes`'a yaz. Rakamlar **birikmiş (cumulative)** toplamdır: "6. ayda toplam 40 müşteri", o ay içinde kazanılan değil.

```json
"growth_projection": {
  "currency": "USD",
  "milestones": [
    {"months_after_launch": 3, "customers": <sayı>, "revenue": <sayı>},
    {"months_after_launch": 6, "customers": <sayı>, "revenue": <sayı>},
    {"months_after_launch": 12, "customers": <sayı>, "revenue": <sayı>}
  ],
  "notes": "<varsayım — nereden geldi bu sayılar>"
}
```

`plan_capacity.py` dönemler arası net artışı (`customers_added`, `revenue_added`) otomatik hesaplar; `render_visuals.py` bunu `growth.svg` (iki panelli sütun grafik) olarak çizer.

## Pazarlama ve reklam stratejisi — varsayılan olarak doldur, araçları güncel araştır

`growth_projection`'daki sayılara nasıl ulaşılacağının somut karşılığıdır — "büyüyeceğiz" demek yetmez, nasıl büyüneceğini göster.

**Kampanya fikirleri** — 2-3 tane, her biri için kanal + mesaj açısı + neden bu kanal:

```json
"campaigns": [
  {"channel": "<nerede>", "angle": "<hangi mesajla>", "why": "<bu kitleye neden uygun>"}
]
```

**Renk paleti** — markanın/kampanyanın kullanacağı renkler ve **her birinin psikolojik anlamı** (ne tetiklediği). Bilinen pazarlama renk psikolojisi kalıplarını kullan, icat etme:

| Renk ailesi | Genelde tetiklediği |
|---|---|
| Mavi | Güven, teknoloji, güvenilirlik — kurumsal/finansal ürünlerde güçlü |
| Yeşil | Büyüme, olumluluk, sağlık/sürdürülebilirlik |
| Turuncu/Sarı | Aciliyet, sıcaklık, harekete geçirme (CTA'larda etkili) |
| Kırmızı | Enerji, aciliyet, dikkat çekme — aşırı kullanımda ucuzluk hissi verebilir |
| Mor | Premium, yaratıcılık, farklılık |
| Siyah/Lacivert | Lüks, ciddiyet, otorite |

Seçtiğin paleti deck'in kendi temasıyla (`theme.css`/`render_visuals.py` paleti) tutarlı tut — genelde aynı renkleri kullanmak markayı sunumla bütünleştirir:

```json
"color_palette": [
  {"hex": "<#renk>", "name": "<ad>", "meaning": "<ne tetikliyor, bu projeyle neden uyumlu>"}
]
```

**AI içerik araçları — WebSearch ile güncel araştır, ezbere yazma.** Bu alan çok hızlı eskir; plan yazarken **her seferinde** "en iyi AI reklam/içerik araçları [bu yıl]" gibi bir WebSearch yap ve konuya uygun 2-4 aracı gerekçesiyle yaz. Aracın ne için kullanılacağını (görsel, video, metin, sosyal gönderi) ve bu projeye neden uygun olduğunu belirt:

```json
"marketing_strategy": {
  "content_style": "<önerilen içerik tarzı/formatı — kısa video, kullanıcı hikayesi, vb.>",
  "campaigns": [...],
  "color_palette": [...],
  "ai_tools": [{"name": "<araç>", "use_case": "<ne için>", "why": "<neden bu projeye uygun>"}],
  "notes": "<araştırma tarihi — bu alan ne zaman güncellendi>"
}
```

`render_visuals.py` bunu iki görsele döker: `marketing.svg` (kampanya + palet + araçlar, üç kolon) ve `ad_creative.svg` (paletle ve sloganla üretilmiş **somut bir örnek reklam kartı mockup'ı** — soyut açıklama değil, gerçek bir görsel).

## Slogan — birkaç öneriyle gel

Kapak slaydı için kısa, cesur bir slogan gerekir — "ne yaptığımız" değil, "ne değiştiği" hissini versin. Her zaman **birden fazla öneri** üret (en az 2-3), birini `chosen` olarak seç, kalanını `alternatives`'ta bırak; müşteri/ekip başka birini tercih edebilir.

```json
"slogan": {
  "chosen": "<seçilen, kapak slaydında görünen>",
  "alternatives": ["<öneri 2>", "<öneri 3>"]
}
```

İyi bir slogan somut bir farkı ya da sonucu ima eder ("Haftalar değil, günler"), soyut bir vaat değil ("En iyi çözüm").

## Kapsam dışını da yaz

Roadmap'in en çok tartışma çıkaran kısmı içine alınanlar değil, alınmayanlardır. Discovery çıktısında açık bir **"bu roadmap'te yok"** listesi tut. Bu liste `roadmap.md`'de tam kalır; müşteriye/yatırımcıya sunulan pitch deck'te ayrı bir slayt olarak gösterilmez (`references/deck.md`) — soru gelirse oradan sözlü cevaplanır.

## Discovery çıktı formatı

```markdown
## Hedef
<tek cümle>

## Başarı kriteri
- Metrik: <ad> | Baseline: <değer veya "bilinmiyor"> | Hedef: <değer> | Ölçüm: <ne zaman, nasıl>

## İş değeri
- Problem: <bugün ne oluyor, maliyeti>
- Fırsat: <talep büyüklüğü>
- Beklenen etki: <ölçülebilir>
- Yapılmazsa: <maliyet>

## Deadline
- Elinizdeki süre: <gün veya "bilinmiyor"> | Neden bu tarih: <...>

## Rakip analizi
- <rakip/alternatif> → fiyat: <...> | pazar konumu: <...> | iyi yaptığı: <...> | yapamadığı: <...>
- Bizim farkımız: <somut, iddia değil>

## SWOT
- Güçlü: <...> | Zayıf: <...> | Fırsat: <...> | Tehdit: <...>

## Türkiye ve global etki
- Türkiye: <pazar büyüklüğü> | özet: <...> | örnekler: <isim, isim>
- Global: <pazar büyüklüğü> | özet: <...> | örnekler: <isim, isim>

## Ekip
- <isim> → <rol> | <somut deneyim/başarı>

## Traction
- <metrik>: <değer> | ... | alıntı: "<...>" — <kaynak>

## İşletme gideri (aylık)
- <kalem> → <tahmini tutar> | <varsayım>

## Büyüme projeksiyonu (birikmiş)
- 3. ay: <müşteri> müşteri, <gelir> | 6. ay: <...> | 12. ay: <...>

## Pazarlama ve reklam stratejisi
- Kampanya: <kanal> → <mesaj açısı>
- Renk paleti: <renk/anlam çiftleri>
- AI araçları (WebSearch ile güncel): <araç> → <kullanım>

## Slogan
- Seçilen: <...>
- Alternatifler: <...>, <...>

## Kısıtlar
- <kısıt> → roadmap'e etkisi: <...>

## Kapsam dışı
- <madde> → nedeni: <...>

## Açık varsayımlar
- <varsayım> → yanlışsa: <plan nasıl değişir>
```

"Açık varsayımlar" bölümü boş kalmamalı. Boşsa yeterince derin sormamışsındır. Bu bölümdeki her madde ileride bir doğrulama işine (spike) veya bir karar noktasına dönüşecek.
