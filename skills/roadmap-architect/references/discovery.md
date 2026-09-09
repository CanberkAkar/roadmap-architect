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

## Kapsam dışını da yaz

Roadmap'in en çok tartışma çıkaran kısmı içine alınanlar değil, alınmayanlardır. Discovery çıktısında açık bir **"bu roadmap'te yok"** listesi tut. Ekip sunumunda buna ayrı slayt ver.

## Discovery çıktı formatı

```markdown
## Hedef
<tek cümle>

## Başarı kriteri
- Metrik: <ad> | Baseline: <değer veya "bilinmiyor"> | Hedef: <değer> | Ölçüm: <ne zaman, nasıl>

## Kısıtlar
- <kısıt> → roadmap'e etkisi: <...>

## Kapsam dışı
- <madde> → nedeni: <...>

## Açık varsayımlar
- <varsayım> → yanlışsa: <plan nasıl değişir>
```

"Açık varsayımlar" bölümü boş kalmamalı. Boşsa yeterince derin sormamışsındır. Bu bölümdeki her madde ileride bir doğrulama işine (spike) veya bir karar noktasına dönüşecek.
