# Ortak dil: müşteri ve teknik ekip aynı plana bakar

Bu skill'in asıl amacı iki tarafı aynı sayfada buluşturmak. Bunun için iki ayrı doküman üretilmez — **tek bir `plan.json`** üretilir, iki dille sunulur.

İki doküman üretmek en sık yapılan hatadır: birbirinden kopar, biri güncellenip diğeri unutulur ve iki taraf farklı gerçekliklerde yaşamaya başlar. Aynı veriden iki görünüm üret.

## Ayrım nerede

| | Müşteri görünümü | Teknik görünüm |
|---|---|---|
| Soru | "Ne alacağım, ne zaman, neden bu sırayla?" | "Ne yapacağım, neye bağlı, ne kadar sürer?" |
| Faz adı | `customer_outcome` | `purpose` |
| İş adı | `customer_name` | `name` |
| Risk metni | `customer_text` | `text` |
| Effort | Faz toplamı, "iş günü" | İş bazında, P50–P80 |
| Bağımlılık | Sadece müşteriyi ilgilendirenler | Tamamı |

`render_visuals.py --audience customer|delivery` aynı plandan iki görsel seti üretir. `plan.json`'a `customer_*` alanlarını yazmak zorunlu değildir; yoksa teknik ad kullanılır — ama müşteriye gidecek her faz ve her yüksek riskli iş için yazılmalıdır.

## Yazım kuralı: mekanizmayı değil sonucu adlandır

Müşteri, ne yaptığınızı değil ne değiştiğini anlamak ister.

| Teknik ad | Müşteriye |
|---|---|
| Kiracı izolasyon spike (RLS vs şema-başı) | Verileri müşteri bazında ayırma yöntemini seçiyoruz |
| İstek bağlamında kiracı çözümleme | Her kullanıcı otomatik olarak kendi şirketinin verisini görüyor |
| Şema migration | Mevcut veriler yeni yapıya taşınıyor |
| Sözleşme testi | Tedarikçinin vaat ettiğini gerçekten yaptığını doğruluyoruz |
| Walking skeleton | En basit haliyle baştan sona çalışan ilk sürüm |
| Regresyon paketi | Eski özelliklerin bozulmadığını otomatik kontrol |
| Rollback prosedürü | Bir sorun çıkarsa eski hale dönme planı |
| Yük testi | Kaç eşzamanlı kullanıcıyı kaldırdığını ölçüyoruz |
| Teknik borç | Sonradan yavaşlatacak birikmiş düzeltmeler |
| Refactor | Görünürde değişiklik yok, sonraki işleri hızlandırıyor |

Bu tablo örnektir, ezber değil. Kural şu: **cümlenin öznesi kullanıcı veya sistem davranışı olsun**, kod veya araç değil.

### "Ee, yani?" testi
Her müşteri-yönlü satırı okuduktan sonra "ee, yani?" diye sor. Cevap veremiyorsan satır teknik kalmıştır.

- "Kiracı veri modeli kuruluyor" → *Ee, yani?* → **"Her müşterinin verisi birbirinden ayrılıyor"**
- "CI hattı kuruluyor" → *Ee, yani?* → **"Her değişiklik otomatik test edilip aynı gün canlıya çıkabiliyor"**

### Yasak kelime listesi (müşteri görünümünde)
`refactor`, `migration`, `endpoint`, `middleware`, `schema`, `deploy`, `pipeline`, `stack`, `sprint velocity`, `story point`, `spike` (yerine "ön çalışma"), `PoC` (yerine "küçük ölçekli deneme").

Sprint kelimesi kalabilir — çoğu müşteri artık biliyor — ama ilk kullanımda bir kez açıkla: "iki haftalık çalışma dilimi".

## Gizlenmeyecek şeyler (roadmap.md'de)

Sadeleştirme, saklama değildir. Aşağıdakiler `roadmap.md`'de **her zaman aynen** durur:

- **Riskler** — tam liste, etki/olasılık/azaltma
- **Belirsizlik** — effort aralık olarak verilir; "bilinmiyor" olduğu yerde öyle yazılır
- **Müşteriden beklenenler** — SSO bilgisi, test kullanıcısı, onay, içerik. Gecikirse planın nasıl kayacağıyla birlikte.
- **Kapsam dışı** — en çok tartışma çıkaran ve en çok atlanan bölüm
- **Karar noktaları** — "X çıkarsa plan Y olur"

Pitch deck'te bunlardan sadece **riskler** görünür — "ters giderse ne olur" endişesiyle değil, "bunu biliyoruz ve yönetiyoruz" güveniyle: her riskin yanında azaltma planı olur (`references/deck.md`). Diğer dördü müşteriye/yatırımcıya sunulan PDF'te slayt olmaz; soru gelirse `roadmap.md`'den sözlü cevaplanır.

Riski `roadmap.md`'den bile gizlemek, ilk aksilikte tüm güvenilirliği kaybettirir. Deck'te göstermemek gizlemek değildir — deck zaten farklı bir işe hizmet eder (ikna), varlığı inkar edilmez, sadece slayt formatına taşınmaz.

## Müşteriden beklenenleri işe dönüştür

Müşteri tarafındaki işler çoğu zaman gerçek kritik yoldur ama plana yazılmadıkları için görünmezler. Her birini `plan.json`'a normal bir iş gibi gir:

```json
{
  "id": "C01",
  "name": "SSO metadata ve test kullanıcıları",
  "customer_name": "Sizden: kimlik sistemi bilgileri ve 2 test kullanıcısı",
  "effort": 1,
  "owner": "customer",
  "lead_time_days": 10,
  "risk": "high",
  "stream": "musteri"
}
```

Böylece kritik yol hesabına dahil olurlar ve zaman şeridinde görünürler. Müşteri kendi işini planın içinde görünce sahiplenir; e-postada gördüğünde ertelenir.

## Effort ve süre dili

- Müşteriye **"iş günü"** de, adam/gün veya story point deme
- Takvim tarihi verme, **sprint numarası** ver — tarihe çevirmek müşteriyle birlikte alınacak bir karardır
- Aralık ver: "18–26 iş günü". Aralığın genişliği, belirsizliğin dürüst ölçüsüdür. Pitch deck'te yer kısıtlı olduğu için aralık tek bir yuvarlak sayıya inebilir ("~20 iş günü") — bu bir taahhüt değil büyüklük hissi vermek içindir; `roadmap.md`'de aralık tam kalır.
- "Kritik yol" terimini kullanabilirsin ama bir kez tanımla: **"sırayla yapılması zorunlu işler zinciri — bu zincir kısalmadan proje daha hızlı bitmez"**

## Agent ve ekip sayısını anlatmak (roadmap.md ve sözlü)

Pitch deck'te bunun için ayrı bir slayt yok (`capacity.svg` deck'e girmez) — bu bir yürütme detayı, ikna malzemesi değil. Ama soru gelirse ("neden daha hızlı olmuyor") ya da `roadmap.md`'de teknik ekiple konuşurken üçlü cümleyi bu dile çevir:

> Bu aşamada birbirinden bağımsız yürüyebilecek **5** iş var. Ama aynı anda **3** tanesini yürütebiliyoruz, çünkü hepsi aynı bölüme dokunuyor ve tek bir kişi kontrol ediyor. Dördüncüye çıkmak için kontrol tarafına bir kişi daha gerekiyor.

Bu, "daha fazla kaynak verin" pazarlığını "şu darboğazı birlikte kaldıralım" konuşmasına çevirir.

## Sunum akışı

Pitch bu sırayla ilerlemeli — bir argüman kurar, karar istemeden ikna eder (`references/deck.md`):

1. **Hedef ve başarı kriteri** (kapakta slogan) → aynı şeyi mi konuşuyoruz?
2. **Fırsat** (varsa) → bu neden şimdi, büyüklüğü ne
3. **Neden biz** (varsa) → alternatiflere karşı somut fark
4. **Çözüm yol haritası** → müşteri ne zaman ne alıyor
5. **Yatırım ve getiri** (varsa) → maliyet ve beklenen getiri yan yana, şeffaf
6. **Büyüme projeksiyonu** (varsa) → 3/6/12 ayda iş ne kadar büyüyor
7. **Riskler ve yönetimi** → ne biliniyor, nasıl kontrol ediliyor — endişe değil güven
8. **Teslim güvenilirliği** (varsa) → bu tarihe yetişir mi, tampon ne kadar
9. **Sonraki adım** → vizyonu ve sloganı tekrar bağla, kapanış

Kapanışta karar/onay listesi yok — bu bir onay toplama seansı değil, bir ikna anıdır. Soru ve itirazlar doğal olarak gelir; cevapları `roadmap.md`'dedir, ayrı bir slaytları yoktur.

## Fırsat, getiri ve teslim güvenilirliği dili

`business_case`, `competitive_analysis`, `cost_estimate`, `growth_projection` ve `deadline`, `plan.json`'a girildiğinde otomatik birer slayt/görsel açar — girilmezse o slaytlar sessizce atlanır, boş bırakılmaz. Bunlar teknik olarak opsiyonel ama pitch'te varsayılan olarak beklenir (`references/discovery.md`).

- **Fırsat** slaydı zaten müşterinin kendi işiyle ilgili olduğu için ayrıca "müşteri diline çevrilmez" — doğrudan onun terimleriyle yazılır (gelir, aday sayısı, pazar). Rakam yoksa slayttan o kartı çıkar; "bilinmiyor" yazma, icat etme.
- **Teslim güvenilirliği** için "tampon" kelimesini bir kez tanımla: **"kritik yol bittiğinde elinizde kalan boş gün — büyüdükçe gecikme riski düşer"**. Durumu üç kelimeden fazla açıklama: Rahat / Sıkışık / Riskli. "Riskli" çıkarsa hemen ardından seçenek sun (kapsamı daralt / tarihi ertele / kaynak ekle) — sadece "riskli" deyip bırakmak güven kırar.
- **Neden biz** slaydında rakibi kötüleme, iddiadan uzak dur. "En iyisi biziz" değil, ölçülebilir fark: "2 gün vs 3 hafta", "ekstra lisans yok". Fark yazamıyorsan slaydı sil, icat etme.
- **Yatırım ve getiri** rakamlarını tahmin olarak sun ama sayı ver — "değişken" veya "duruma göre" gibi kaçamak ifadeler güven kırar. Tahminin dayandığı varsayımı yaz (kaç kullanıcı, hangi bulut sağlayıcı): rakam değişirse müşteri nedenini görsün.
- **Büyüme projeksiyonu** birikmiş (cumulative) rakamlardır, dönemlik değil — "12. ayda 90 müşteri" demek "12 ay içinde toplam 90 müşteri kazandık" demektir, "12. ayda 90 yeni müşteri" değil. İkisini karıştırma, dinleyici anlık hızla toplamı ayırt edemez.
- **Slogan** somut bir sonucu ima etsin, soyut bir vaat değil. "En iyi çözüm" değil, "haftalar değil, günler". Her zaman birden fazla öneriyle gel; seçilen tek slogan kapak slaydında görünür, diğerleri `roadmap.md`'de referans olarak durur.

## Revizyonda ortak dil

Güncelleme yaparken müşteri tarafına giden özet üç satırı geçmesin:

```
Ne değişti: <olgu, teknik terim olmadan>
Plana etkisi: <hangi aşama ne kadar kaydı>
Sizden gereken: <varsa; yoksa "yok" yaz>
```

"Sizden gereken: yok" satırını atlamayın. Müşteri her güncellemede kendisinden bir şey isteneceğini varsayar; istenmediğini söylemek güven kurar.
