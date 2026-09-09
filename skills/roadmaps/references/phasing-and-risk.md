# Fazlama, dependency ve risk

## Faz nedir

Bir faz, ürünün bir **durumundan** diğerine geçişidir. Testi basit: fazın adını okuyan biri, o faz bittiğinde ürünün ne yapabildiğini anlıyor mu?

- Katman bölmesi (kötü): "Faz 2: API katmanı"
- Durum bölmesi (iyi): "Faz 2: Tek ülkede uçtan uca ödeme alınabiliyor"

Katman bölmesinin sorunu, riskin sona toplanmasıdır — entegrasyon problemleri ancak her şey bittiğinde görünür.

### Faz sayısı
3–6 arası tut. 8'i geçiyorsa ya fazları task seviyesine indirmişsindir ya da proje ayrı roadmap'lere bölünmelidir. 2'nin altındaysa faz yapısına gerek yoktur, düz bir plan yaz.

## Her faz için doldurulacak alanlar

| Alan | Nasıl yazılır |
|---|---|
| Amaç | Faz sonundaki ürün durumu, tek cümle |
| Milestone | Demo edilebilir/ölçülebilir kanıt. "Kod merge edildi" milestone değildir. |
| Öncelik | P0 hedefe ulaşmak için zorunlu · P1 hedefi belirgin güçlendirir · P2 iyi olur |
| Dependency | İç fazlar + dış aktörler + teknik önkoşullar |
| Effort | P50–P80 aralığı, ideal insan-günü |
| Risk | Seviye + tür + neden + doğrulama yolu |
| Çıktı | Kim ne alıyor (kullanıcı, iç ekip, satış, denetim) |

## Effort tahmini

İdeal insan-günü kullan (toplantı, izin, bağlam değişimi hariç). Takvime çevirmeyi kapasite hesabı yapar — burada karıştırma.

Aralık ver, tek sayı verme:
- **P50** — işler beklendiği gibi giderse
- **P80** — makul aksilikler dahil

`P80 / P50 > 2` ise bu iş bir tahmin değil, bir belirsizliktir. İki seçenek: ya önüne bir spike koy, ya da işi belirsiz kısmı ayrılacak şekilde böl.

Referans noktası olmadan tahmin yapma. Repo'daki benzer geçmiş işlere bak (PR boyutu, açık-kapalı arası süre) veya kullanıcıya "daha önce yaptığınız hangi işe benziyor?" diye sor.

## Dependency

Üç tür var, üçünü de ara:

1. **İç** — faz/iş arası sıra zorunluluğu
2. **Dış** — başka ekip, satın alma, hukuk/uyum onayı, üçüncü parti API erişimi, müşteri verisi
3. **Teknik önkoşul** — altyapı, migration, ortam kurulumu, veri temizliği

Dış bağımlılıklar en çok atlanan ve en çok geciktiren gruptur. Her biri için **lead time** (talep edilmesiyle kullanılabilir olması arası süre) yaz ve **kimin talep edeceğini** belirt. Lead time'ı uzun olan dış bağımlılık, işin kendisi geç başlasa bile roadmap'in ilk gününde tetiklenmelidir.

Dependency'leri `plan.json` içine `deps` alanı olarak gir; kritik yolu script hesaplayacak.

## Risk

### Sınıflandırma
- **Teknik** — yaklaşım işe yarayacak mı, performans/ölçek tutacak mı
- **Bağımlılık** — dış taraf zamanında ve vaat ettiği gibi verecek mi
- **Ürün** — yaptığımız şey hedefe gerçekten hizmet edecek mi
- **Operasyonel** — canlıya alma, veri göçü, geri dönüş (rollback), destek yükü

### Seviye
`Etki × Olasılık`. Ama asıl önemlisi üçüncü boyut: **ne zaman öğreniyoruz?** Geç öğrenilen orta risk, erken öğrenilen yüksek riskten daha tehlikelidir. Risk sıralamasını bu eksene göre yap.

### Erken doğrulama
Yüksek riskli işi erkene çekmek "o işi önce yapalım" demek değildir — genelde işin tamamını yapmaya gerek yoktur. Doğrulama biçimleri:

| Biçim | Ne zaman | Süre |
|---|---|---|
| **Spike** | Teknik belirsizlik, "yapılabilir mi?" | 1–3 gün, zaman kutulu |
| **Walking skeleton** | Çok entegrasyonlu mimari | 3–8 gün, uçtan uca en ince dilim |
| **Sözleşme testi** | Dış API/servis bağımlılığı | 1–2 gün |
| **Prototip + kullanıcı testi** | Ürün belirsizliği | 3–5 gün |
| **Yük/performans denemesi** | Ölçek riski | 2–4 gün |

Her doğrulama işi iki şey içermeli:
1. **Zaman kutusu** — süre dolduğunda sonuç ne olursa olsun durulur
2. **Karar noktası** — "Sonuç X ise şu fazı böyle değiştiririz"

Karar noktası yazılmamış bir spike, sadece geciktirilmiş bir iştir.

### Risk tablosu formatı

```markdown
| # | Risk | Tür | Etki | Olasılık | Ne zaman öğreniriz | Doğrulama | Karar noktası |
|---|---|---|---|---|---|---|---|
| R1 | Legacy şema çok kiracılı yapıyı kaldırmayabilir | Teknik | Yüksek | Orta | Faz 1 | 3 günlük spike | Kaldırmıyorsa Faz 2'ye şema göçü eklenir, +15 gün |
```

`plan.json` içinde riskli işleri `"risk": "high"` ile işaretle — kapasite script'i bunları öne çeker.

## Faz sırası

Sıralamayı belirleyen dört şey, bu öncelikle:

1. **Dependency** — teknik olarak imkânsız sıralar elenir
2. **Öğrenme değeri** — belirsizliği en çok azaltan iş öne
3. **Hedefe katkı** — P0'lar P1'lerden önce
4. **Paralelleşebilirlik** — bir sonraki adımı en çok açan iş öne

Üç ve dördüncü kriter çakışırsa öğrenme değerini seç. Erken öğrenilen bir "hayır", geç kazanılan bir "evet"ten daha değerlidir.
