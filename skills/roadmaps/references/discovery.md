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

## Talebi analiz et

Müşterinin söylediği şey ("bir dashboard lazım") ile aslında istediği şey ("elimde hangi müşterinin ne kadar risk taşıdığını her sabah görmek istiyorum") genelde farklıdır. İkisini ayrı ayrı yaz:

- **Söylenen talep** — müşterinin kelimeleri, aynen
- **Altında yatan ihtiyaç** — bu talebin çözdüğü asıl problem ne
- **Neden şimdi** — bu talep neden bugün gündemde (rekabet, kayıp fırsat, regülasyon, büyüme hedefi)

Bu analiz `business_case`'in (iş değeri) hammaddesidir. Müşteriye "iş değeri" slaydı göstermeyecek olsan bile bu analiz roadmap'in önceliklendirmesini değiştirir: en yüksek iş değerini taşıyan aşama erken faza gelmelidir.

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

## Rakip analizi ve işletme gideri

Müşteri genelde "neden size, neden şimdi bu parayı vereyim" sorusunu içinden sorar ama nadiren yüksek sesle sorar. İki bölüm bu soruyu önceden cevaplar:

**Rakip analizi** — 1-3 benzer çözümü (rakip ürün, mevcut süreç, "hiçbir şey yapmamak" dahil) kısaca değerlendir: neyi iyi yapıyor, neyi yapamıyor. Sonra kendi farkını yaz — iddia değil, somut fark ("2 gün vs 3 hafta", "mevcut kimlik sağlayıcıyla entegre"). Rakibi kötüleme, kendi farkını göster.

```json
"competitive_analysis": {
  "competitors": [
    {"name": "<rakip/alternatif>", "strengths": "<iyi yaptığı>", "weaknesses": "<yapamadığı>"}
  ],
  "our_advantages": ["<somut fark 1>", "<somut fark 2>"]
}
```

**İşletme gideri** — proje bittikten sonra sistemin **çalışır tutulmasının** aylık maliyeti: sunucu/hosting, üçüncü parti servisler (e-posta, SMS, izleme), reklam/pazarlama, lisans ücretleri. Tek seferlik kurulum maliyeti ayrı bir kalemdir (`one_time`), aylık işletme gideri ayrı (`recurring_monthly`). Kaba tahmindir demekten çekinme — rakam vermemekten daha güvenilirdir.

```json
"cost_estimate": {
  "currency": "USD",
  "one_time": [{"item": "<kurulum/geliştirme>", "amount": <sayı>, "note": "<nereden geldi>"}],
  "recurring_monthly": [{"item": "<sunucu/reklam/vb>", "amount": <sayı>, "note": "<varsayım>"}],
  "notes": "<tahminin ne kadar kaba olduğu>"
}
```

`amount` alanlarına tahmin bile olsa somut bir sayı yaz — `plan_capacity.py` bunları toplayıp aylık/yıllık toplamı ve `cost.svg` grafiğini otomatik üretir; elle toplama yapma.

## Kapsam dışını da yaz

Roadmap'in en çok tartışma çıkaran kısmı içine alınanlar değil, alınmayanlardır. Discovery çıktısında açık bir **"bu roadmap'te yok"** listesi tut. Ekip sunumunda buna ayrı slayt ver.

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
- <rakip/alternatif> → iyi yaptığı: <...> | yapamadığı: <...>
- Bizim farkımız: <somut, iddia değil>

## İşletme gideri (aylık)
- <kalem> → <tahmini tutar> | <varsayım>

## Kısıtlar
- <kısıt> → roadmap'e etkisi: <...>

## Kapsam dışı
- <madde> → nedeni: <...>

## Açık varsayımlar
- <varsayım> → yanlışsa: <plan nasıl değişir>
```

"Açık varsayımlar" bölümü boş kalmamalı. Boşsa yeterince derin sormamışsındır. Bu bölümdeki her madde ileride bir doğrulama işine (spike) veya bir karar noktasına dönüşecek.
