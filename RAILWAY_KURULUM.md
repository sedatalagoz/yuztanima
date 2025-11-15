# 🚂 Railway.app ile 5 Dakikada Deploy

## ✨ Neden Railway?

- ✅ **Ücretsiz** ($5 kredi/ay - yeterli)
- ✅ **Çok kolay** (GitHub'dan otomatik)
- ✅ **HTTPS** otomatik
- ✅ **Sabit link** (değişmiyor)
- ✅ **7/24 çalışır** (bilgisayarın kapalı olsa bile)

---

## 🚀 Adım Adım Kurulum

### ADIM 1: GitHub'a Yükle

```bash
# Proje klasöründe
git init
git add .
git commit -m "Initial commit"

# GitHub'da yeni repo oluştur (github.com/new)
# Sonra:
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
git branch -M main
git push -u origin main
```

**Not:** GitHub hesabın yoksa oluştur: https://github.com/signup

---

### ADIM 2: Railway'e Kaydol

1. https://railway.app adresine git
2. **"Login"** tıkla
3. **"Login with GitHub"** seç
4. GitHub ile giriş yap

---

### ADIM 3: Proje Oluştur

1. **"New Project"** tıkla
2. **"Deploy from GitHub repo"** seç
3. Repo'nu seç (yuztanima veya ne adlandırdıysan)
4. **"Deploy Now"** tıkla

Railway otomatik olarak:
- ✅ Python'u kurar
- ✅ Paketleri yükler
- ✅ Uygulamayı başlatır
- ✅ HTTPS link verir

**Süre:** 5-10 dakika

---

### ADIM 4: Domain Al

Deploy tamamlandıktan sonra:

1. **"Settings"** sekmesine git
2. **"Generate Domain"** tıkla
3. Link hazır! Örnek: `yuztanima-production.up.railway.app`

---

### ADIM 5: Test Et

Tarayıcıda aç:
```
https://yuztanima-production.up.railway.app
```

Admin panel:
```
https://yuztanima-production.up.railway.app/admin/login
Kullanıcı: admin
Şifre: admin123
```

---

## 🎯 Tamamlandı!

Artık:
- ✅ 7/24 çalışan bir site var
- ✅ HTTPS güvenli
- ✅ Sabit link
- ✅ Müşteriye gönderebilirsin

---

## 🔄 Güncelleme Yapmak

Kod değiştirdiğinde:

```bash
git add .
git commit -m "Güncelleme"
git push
```

Railway **otomatik** yeniden deploy eder! 🚀

---

## 💰 Maliyet

**Ücretsiz Plan:**
- $5 kredi/ay
- Küçük projeler için yeterli
- Kredi biterse $5/ay

**Kullanım:**
- Her saat çalışma: ~$0.01
- Ayda ~$3-5 tutar

---

## ⚙️ Environment Variables (Opsiyonel)

Railway'de **"Variables"** sekmesinden:

```
SECRET_KEY=rastgele-uzun-güvenli-key
ADMIN_PASSWORD=yeni-güvenli-şifre
```

---

## 🐛 Sorun Giderme

### Deploy başarısız oldu

**Logları kontrol et:**
1. Railway'de projeye tıkla
2. **"Deployments"** sekmesi
3. Son deployment'e tıkla
4. **"View Logs"** tıkla

**Yaygın hatalar:**
- `dlib` kurulum hatası → Bekle, uzun sürer (5-10 dk)
- Port hatası → `web_app.py` PORT değişkenini kontrol et
- Module not found → `requirements_web.txt` kontrol et

### Site yavaş

Railway ücretsiz planda:
- İlk istek yavaş olabilir (cold start)
- Sonraki istekler hızlı

### Database kayboldu

Railway her deploy'da sıfırlanır. Kalıcı database için:
- Railway PostgreSQL ekle (ücretsiz)
- Veya SQLite yerine PostgreSQL kullan

---

## 📊 İstatistikler

Railway dashboard'da:
- CPU kullanımı
- RAM kullanımı
- Network trafiği
- Deployment geçmişi

---

## 🎁 Bonus: Özel Domain

Kendi domain'ini bağlamak için:

1. Railway'de **"Settings"** > **"Custom Domain"**
2. Domain'ini gir (örn: `yuztanima.com`)
3. DNS kayıtlarını güncelle:
   ```
   CNAME: @ -> yuztanima-production.up.railway.app
   ```

---

## ✅ Checklist

Deploy öncesi kontrol:

- [ ] GitHub'a push edildi
- [ ] `requirements_web.txt` güncel
- [ ] `Procfile` var
- [ ] `runtime.txt` var
- [ ] `.gitignore` var
- [ ] Admin şifresi değiştirildi

---

## 🚀 Hemen Başla

```bash
# 1. GitHub'a yükle
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI/REPO.git
git push -u origin main

# 2. Railway'e git
# https://railway.app

# 3. Deploy from GitHub

# 4. 5 dakika bekle

# 5. Link hazır! 🎉
```

**Başarılar! 🚂**
