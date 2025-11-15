# 🔄 PHP Versiyonu (Shared Hosting İçin)

## ⚠️ Önemli Not

Python yüz tanıma kütüphaneleri (face_recognition, dlib) shared hosting'de çalışmaz.

PHP versiyonu için **harici API** kullanmak gerekir.

---

## 🎯 API Seçenekleri

### 1. Face++ (Önerilen)
- **Ücretsiz:** 1000 istek/ay
- **Ücretli:** $0.0005/istek
- **Doğruluk:** %99+
- **Link:** https://www.faceplusplus.com

### 2. AWS Rekognition
- **Fiyat:** $0.001/resim
- **Doğruluk:** %99+
- **Link:** https://aws.amazon.com/rekognition/

### 3. Microsoft Azure Face API
- **Ücretsiz:** 30,000 istek/ay
- **Ücretli:** $1/1000 istek
- **Link:** https://azure.microsoft.com/face-api/

### 4. Kairos
- **Ücretsiz:** 500 istek/ay
- **Ücretli:** $99/ay
- **Link:** https://www.kairos.com

---

## 💰 Maliyet Karşılaştırması

### Senaryo: Ayda 1000 kullanıcı

**API Kullanımı (PHP):**
- Face++: Ücretsiz (1000 istek/ay)
- Mevcut hosting: $0
- **Toplam:** $0/ay

**VPS (Python):**
- Hetzner VPS: €4/ay
- **Toplam:** €4/ay (~$4.5)

**Sonuç:** Düşük kullanımda API daha ucuz!

---

## 🚀 Hızlı Karar Rehberi

### PHP + API Kullan (Mevcut Hosting)
✅ Ayda 1000'den az kullanıcı
✅ Ek maliyet istemiyorsun
✅ Basit kurulum istiyorsun
❌ Yavaş olabilir (API gecikme)
❌ İnternet bağımlı

### Python + VPS Al
✅ Ayda 1000+ kullanıcı
✅ Hızlı performans istiyorsun
✅ Tam kontrol istiyorsun
✅ Offline çalışmasını istiyorsun
❌ Aylık €4 maliyet

---

## 📝 PHP Versiyonu İster misin?

Eğer mevcut hostinginde çalışmasını istiyorsan, PHP versiyonunu yazabilirim:

**Özellikler:**
- ✅ PHP + MySQL
- ✅ Face++ API entegrasyonu
- ✅ Admin paneli
- ✅ Kullanıcı arayüzü
- ✅ cPanel ile kurulum

**Süre:** 1-2 saat

Söyle, PHP versiyonunu mu yazayım yoksa VPS mi alacaksın?

---

## 🎯 Önerim

**Eğer bütçen varsa:** Hetzner VPS al (€4/ay)
- Daha hızlı
- Daha güvenli
- Tam kontrol
- Offline çalışır

**Eğer bütçen yoksa:** PHP + Face++ API
- Mevcut hostingde çalışır
- Ücretsiz (1000 istek/ay)
- Basit kurulum

Ne dersin? 🤔
