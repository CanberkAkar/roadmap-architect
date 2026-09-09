# Ölçeklendirme: kaç agent, kaç kişi

İki ayrı soru var ve aynı matematiği paylaşıyorlar:

- **İnsan ekip** — kaç kişi, hangi rollerde, sprint kapasitesi ne
- **Claude subagent** — aynı anda kaç paralel iş akışı çalıştırılabilir

Ortak nokta: ikisinin de üst sınırını **işin yapısı** belirler, kaynak miktarı değil. Paralelleşmeyen işe adam eklemek süreyi kısaltmaz, koordinasyon maliyetini artırır.

## Temel büyüklükler

Script (`scripts/plan_capacity.py`) bunları `plan.json`'dan hesaplar:

- **E** — toplam effort (insan-günü)
- **C** — kritik yol: dependency zinciri boyunca en uzun effort toplamı. Sonsuz kaynak verilse bile proje bundan kısa sürmez.
- **PI** — paralelleşebilirlik indeksi = `E / C`. Ortalama kaç iş aynı anda yürüyebilir.
- **S** — çakışmayan iş akışı (stream) sayısı. Aynı modüle yazan iki akış paralel sayılmaz.

## İnsan ekip

```
Sprint kapasitesi = kişi × sprint_gün × odak_faktörü
Minimum sprint    = max( tavan(E / kapasite), tavan(C / sprint_gün) )
```

**Odak faktörü** — ideal insan-günün ne kadarı gerçekten işe gidiyor:

| Durum | Faktör |
|---|---|
| Deneyimli ekip, bilinen kod tabanı, az toplantı | 0.75 |
| Tipik ürün ekibi | 0.65 |
| Yeni ekip / yeni domain / yüksek destek yükü | 0.50 |
| Kısmi tahsis (kişi başka projede de var) | 0.35 |

Ekibin geçmiş verisi varsa faktörü tahmin etme, ölç: son birkaç sprintte planlanan vs. tamamlanan.

**Üst sınır:** `kişi > PI` ise fazla kişi boşta kalır veya birbirini bekler. Kişi sayısı `PI`'yi belirgin aşıyorsa doğru öneri "işi paralelleşecek şekilde yeniden böl" veya "ekibi küçült ve sırayla ilerle"dir; ikisi de mümkün değilse kalan kapasiteyi teknik borç ve test altyapısına yönlendir.

## Claude subagent sayısı

```
Önerilen = min( tavan(PI), S, İncelemeKapasitesi, 8 )
```

Dört sınırın hepsi bağlayıcı. Hangisinin bağladığını **açıkça yaz** — asıl bilgi sayının kendisi değil, darboğazın nerede olduğudur.

### 1. `tavan(PI)` — işin yapısal sınırı
Kritik yol uzun ve dar bir projede 6 agent açmak anlamsızdır.

### 2. `S` — yazma çakışması sınırı
İki agent aynı dosyaya/modüle yazarsa kazandığın zamanı merge çözümünde kaybedersin. Stream'leri repo'nun gerçek sınırlarına göre ayır: ayrı servisler, ayrı paketler, ayrı modüller, `frontend/` vs `api/` gibi. Paylaşılan şema, ortak tip tanımları ve migration dosyaları **tek bir stream'e** ait olmalı — bunlar sessiz çakışma kaynağıdır.

Stream ayrımı net değilse agent sayısını değil, önce mimari sınırları netleştir.

### 3. İnceleme kapasitesi
Her agent iş üretir; üretilen iş **bir insan tarafından okunmadan** birikirse plan çöker. Kaba oran: bir kişi günde 2–3 anlamlı değişikliği gerçekten inceleyebilir. Tek gözden geçiren varsa 3'ten fazla agent açma.

### 4. Sabit tavan (8)
Bunun ötesinde bağlam senkronizasyonu, çelişen kararlar ve entegrasyon maliyeti kazancı yer. Pratikte iyi çalışan aralık **2–4**.

### Agent tipi ayrımı
Sayıyı verirken hepsini aynı işe koşma. Tipik dağılım:

- **Uygulama agent'ları** — stream başına bir tane, esas işi yapar
- **Entegrasyon agent'ı** — stream'lerin buluştuğu yeri sağlam tutar. 3+ uygulama agent'ı varsa ayır.
- **Doğrulama agent'ı** — test, sözleşme kontrolü, regresyon. Kendi işini kendi doğrulayan agent zayıf bir kontroldür.

## Faz bazında değişir

Tek bir agent sayısı verme. Fazlar farklı şekillere sahiptir:

- **Discovery / spike fazı** — 1–2 agent. Belirsizlik yüksekken paralelleştirmek boşa iş üretir.
- **Walking skeleton** — 1 agent. Uçtan uca tutarlılık paralellikten önemlidir.
- **Yatay genişleme fazı** — en yüksek agent sayısı. İskelet var, üstüne bağımsız parçalar ekleniyor.
- **Sertleştirme / release** — 1–2 agent + yoğun inceleme. Bu fazda hız değil, kararlılık istenir.

Bunu bir tabloyla ver:

```markdown
| Faz | Paralel iş | Önerilen agent | Sınırlayan | Not |
|---|---|---|---|---|
| Faz 1 · Doğrulama | 2 | 2 | işin yapısı | spike'lar bağımsız |
| Faz 2 · İskelet | 1 | 1 | dependency | uçtan uca tek akış |
| Faz 3 · Genişleme | 5.2 | 4 | stream sayısı | api/web/worker/veri |
| Faz 4 · Sertleştirme | 3 | 2 | inceleme kapasitesi | tek reviewer |
```

## Sunumda nasıl anlatılır

"4 agent" bir karar değil, bir sonuçtur. Şu üç cümleyi kur:

1. Bu fazda **N** iş birbirinden bağımsız yürüyebiliyor.
2. Bunu **X**'e düşüren şey: <darboğaz>.
3. **X**'i artırmak istiyorsak yapılması gereken: <darboğazı kaldıracak eylem>.

Üçüncü cümle, ölçeklendirme tartışmasını "daha fazla kaynak isteyelim"den "şu sınırı kaldıralım"a çevirir. Asıl değer orada.
