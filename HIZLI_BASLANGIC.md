# ⚡ Hızlı Başlangıç - Hostinge Kurulum

## 🎯 3 Adımda Kurulum

### 1️⃣ Dosyaları Sunucuya Yükle

**SSH ile bağlan:**
```bash
ssh root@sunucu-ip-adresi
```

**Proje klasörü oluştur:**
```bash
cd /var/www/
git clone https://github.com/kullanici/repo.git photo-gallery
# veya
mkdir photo-gallery
cd photo-gallery
# Dosyaları FTP/SCP ile yükle
```

### 2️⃣ Otomatik Kurulum Scriptini Çalıştır

```bash
cd /var/www/photo-gallery
sudo bash install.sh
```

Script şunları soracak:
- Domain adınız (örn: example.com)
- Email adresiniz (SSL için)

**Kurulum 10-15 dakika sürer.**

### 3️⃣ Tamamlandı! 🎉

Siteniz hazır:
- **Ana Sayfa:** https://yourdomain.com
- **Admin Panel:** https://yourdomain.com/admin/login

**Varsayılan Admin:**
- Kullanıcı: `admin`
- Şifre: `admin123`

---

## 🔒 İlk Yapılacaklar

### 1. Admin Şifresini Değiştir
```bash
nano /var/www/photo-gallery/web_app.py
```

Şu satırı bul:
```python
admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
```

Değiştir:
```python
admin_pass = hashlib.sha256('YENİ_GÜVENLİ_ŞİFRE'.encode()).hexdigest()
```

Kaydet ve yeniden başlat:
```bash
sudo systemctl restart photo-gallery
```

### 2. Secret Key Değiştir
```bash
nano /var/www/photo-gallery/web_app.py
```

Şu satırı bul:
```python
app.secret_key = 'your-secret-key-change-this-in-production'
```

Değiştir:
```python
app.secret_key = 'rastgele-çok-uzun-güvenli-key-123456789'
```

---

## 📱 Manuel Kurulum (Script Kullanmadan)

Detaylı adım adım kurulum için:
```bash
cat HOSTING_KURULUM.md
```

---

## 🔧 Yönetim Komutları

```bash
# Uygulamayı yeniden başlat
sudo systemctl restart photo-gallery

# Logları görüntüle
sudo journalctl -u photo-gallery -f

# Durumu kontrol et
sudo systemctl status photo-gallery

# Nginx yeniden başlat
sudo systemctl restart nginx
```

---

## 🐛 Sorun mu Var?

### Site açılmıyor
```bash
# Servis çalışıyor mu?
sudo systemctl status photo-gallery

# Nginx çalışıyor mu?
sudo systemctl status nginx

# Logları kontrol et
sudo journalctl -u photo-gallery -n 50
```

### 502 Bad Gateway
```bash
sudo systemctl restart photo-gallery
sudo systemctl restart nginx
```

### Fotoğraflar yüklenmiyor
```bash
sudo chmod -R 777 /var/www/photo-gallery/uploads/
sudo systemctl restart photo-gallery
```

---

## 💡 İpuçları

### DNS Ayarları
Domain sağlayıcında A kaydı ekle:
```
A Record: @ -> SUNUCU-IP
A Record: www -> SUNUCU-IP
```

### Güvenlik
```bash
# Firewall kontrol
sudo ufw status

# SSL yenileme testi
sudo certbot renew --dry-run
```

### Performans
```bash
# Daha fazla worker (CPU x 2)
sudo nano /etc/systemd/system/photo-gallery.service
# -w 4 yerine -w 8 yap
```

---

## 📞 Yardım

Detaylı dokümantasyon:
- `HOSTING_KURULUM.md` - Tam kurulum rehberi
- `WEB_DEPLOYMENT.md` - Deployment seçenekleri

**Başarılar! 🚀**
