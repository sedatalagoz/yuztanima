# 🌐 Kendi Hostingine Kurulum Rehberi

## 📋 Gereksinimler

### Hosting Özellikleri
- **SSH Erişimi** (zorunlu)
- **Python 3.8+** desteği
- **En az 2GB RAM**
- **En az 10GB disk alanı**
- **Root veya sudo yetkisi**

### Uyumlu Hosting Sağlayıcıları
✅ **VPS/Cloud Sunucular:**
- DigitalOcean
- Linode
- Vultr
- AWS EC2
- Google Cloud
- Hetzner
- Contabo

✅ **Shared Hosting (Python destekli):**
- A2 Hosting
- PythonAnywhere
- Hostinger (VPS)

❌ **Uygun Değil:**
- Sadece PHP destekli shared hosting
- cPanel-only hosting (Python desteği yoksa)

---

## 🚀 Kurulum Adımları

### ADIM 1: Dosyaları Sunucuya Yükle

#### SSH ile Bağlan
```bash
ssh kullanici@sunucu-ip-adresi
# Örnek: ssh root@185.123.45.67
```

#### Proje Klasörü Oluştur
```bash
cd /var/www/
mkdir photo-gallery
cd photo-gallery
```

#### Dosyaları Yükle (3 Yöntem)

**Yöntem 1: Git ile (Önerilen)**
```bash
# GitHub'a push et
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/kullanici/repo.git
git push -u origin main

# Sunucuda çek
git clone https://github.com/kullanici/repo.git .
```

**Yöntem 2: SCP ile**
```bash
# Local bilgisayarından
scp -r /path/to/proje/* kullanici@sunucu-ip:/var/www/photo-gallery/
```

**Yöntem 3: FTP/SFTP**
- FileZilla veya WinSCP kullan
- Tüm dosyaları `/var/www/photo-gallery/` klasörüne yükle

---

### ADIM 2: Sunucu Hazırlığı

#### Python ve Gerekli Paketleri Kur

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y
sudo apt install build-essential cmake -y
sudo apt install nginx -y
```

**CentOS/RHEL:**
```bash
sudo yum update -y
sudo yum install python3 python3-pip -y
sudo yum install gcc gcc-c++ cmake -y
sudo yum install nginx -y
```

---

### ADIM 3: Virtual Environment Oluştur

```bash
cd /var/www/photo-gallery

# Virtual environment oluştur
python3 -m venv venv

# Aktif et
source venv/bin/activate

# Pip güncelle
pip install --upgrade pip
```

---

### ADIM 4: Python Paketlerini Yükle

```bash
# Gerekli paketleri yükle
pip install -r requirements_web.txt

# Production için gunicorn ekle
pip install gunicorn
```

**Not:** `dlib` kurulumu uzun sürebilir (5-10 dakika). Sabırlı ol!

---

### ADIM 5: Klasör İzinlerini Ayarla

```bash
# Uploads klasörü oluştur
mkdir -p uploads/agency uploads/users

# İzinleri ayarla
sudo chown -R www-data:www-data /var/www/photo-gallery
sudo chmod -R 755 /var/www/photo-gallery
sudo chmod -R 777 uploads/
```

---

### ADIM 6: Admin Şifresini Değiştir

```bash
nano web_app.py
```

Şu satırı bul ve şifreyi değiştir:
```python
# Varsayılan admin ekle (username: admin, password: admin123)
admin_pass = hashlib.sha256('YENİ_GÜVENLİ_ŞİFRE'.encode()).hexdigest()
```

Secret key'i de değiştir:
```python
app.secret_key = 'rastgele-çok-uzun-güvenli-key-buraya-yaz-123456789'
```

Kaydet: `Ctrl+O`, Çık: `Ctrl+X`

---

### ADIM 7: Test Et

```bash
# Virtual environment aktif olmalı
source venv/bin/activate

# Test çalıştır
python3 web_app.py
```

Tarayıcıda aç: `http://sunucu-ip:5001`

Çalışıyorsa `Ctrl+C` ile durdur.

---

### ADIM 8: Gunicorn ile Production Çalıştır

#### Systemd Service Oluştur

```bash
sudo nano /etc/systemd/system/photo-gallery.service
```

Şu içeriği yapıştır:
```ini
[Unit]
Description=Photo Gallery Web Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/photo-gallery
Environment="PATH=/var/www/photo-gallery/venv/bin"
ExecStart=/var/www/photo-gallery/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 web_app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Kaydet ve çık.

#### Service'i Başlat

```bash
# Service'i yükle
sudo systemctl daemon-reload

# Başlat
sudo systemctl start photo-gallery

# Otomatik başlatmayı aktif et
sudo systemctl enable photo-gallery

# Durumu kontrol et
sudo systemctl status photo-gallery
```

---

### ADIM 9: Nginx Reverse Proxy Ayarla

#### Nginx Config Oluştur

```bash
sudo nano /etc/nginx/sites-available/photo-gallery
```

Şu içeriği yapıştır:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Dosya yükleme limiti
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static dosyalar için
    location /uploads {
        alias /var/www/photo-gallery/uploads;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Not:** `yourdomain.com` yerine kendi domain'ini yaz!

#### Nginx'i Aktif Et

```bash
# Symlink oluştur
sudo ln -s /etc/nginx/sites-available/photo-gallery /etc/nginx/sites-enabled/

# Varsayılan siteyi kaldır (opsiyonel)
sudo rm /etc/nginx/sites-enabled/default

# Config test et
sudo nginx -t

# Nginx'i yeniden başlat
sudo systemctl restart nginx
```

---

### ADIM 10: Domain Ayarları

#### DNS Kayıtlarını Güncelle

Domain sağlayıcında (GoDaddy, Namecheap, vb.):

```
A Record:
Name: @
Value: SUNUCU-IP-ADRESİ
TTL: 3600

A Record:
Name: www
Value: SUNUCU-IP-ADRESİ
TTL: 3600
```

DNS yayılması 1-24 saat sürebilir.

---

### ADIM 11: SSL Sertifikası (HTTPS)

#### Let's Encrypt ile Ücretsiz SSL

```bash
# Certbot kur
sudo apt install certbot python3-certbot-nginx -y

# SSL sertifikası al
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Email adresini gir
# Terms'i kabul et
# Redirect seçeneğini seç (2)
```

Otomatik yenileme:
```bash
# Test et
sudo certbot renew --dry-run

# Cron job zaten kurulu, kontrol et
sudo systemctl status certbot.timer
```

---

### ADIM 12: Firewall Ayarları

```bash
# UFW kur (Ubuntu)
sudo apt install ufw -y

# Kuralları ekle
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Aktif et
sudo ufw enable

# Durumu kontrol et
sudo ufw status
```

---

## ✅ Kurulum Tamamlandı!

Artık siteniz çalışıyor:
- **Ana Sayfa:** https://yourdomain.com
- **Admin Panel:** https://yourdomain.com/admin/login

---

## 🔧 Yönetim Komutları

### Uygulamayı Yeniden Başlat
```bash
sudo systemctl restart photo-gallery
```

### Logları Görüntüle
```bash
# Uygulama logları
sudo journalctl -u photo-gallery -f

# Nginx logları
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Uygulamayı Durdur/Başlat
```bash
sudo systemctl stop photo-gallery
sudo systemctl start photo-gallery
sudo systemctl status photo-gallery
```

### Kod Güncellemesi
```bash
cd /var/www/photo-gallery
git pull origin main
sudo systemctl restart photo-gallery
```

---

## 🐛 Sorun Giderme

### "502 Bad Gateway" Hatası
```bash
# Gunicorn çalışıyor mu?
sudo systemctl status photo-gallery

# Çalışmıyorsa başlat
sudo systemctl start photo-gallery

# Logları kontrol et
sudo journalctl -u photo-gallery -n 50
```

### "Permission Denied" Hatası
```bash
sudo chown -R www-data:www-data /var/www/photo-gallery
sudo chmod -R 755 /var/www/photo-gallery
sudo chmod -R 777 uploads/
```

### "Module not found" Hatası
```bash
cd /var/www/photo-gallery
source venv/bin/activate
pip install -r requirements_web.txt
sudo systemctl restart photo-gallery
```

### Fotoğraflar Yüklenmiyor
```bash
# Uploads klasörü izinleri
sudo chmod -R 777 uploads/

# Nginx config kontrol
sudo nginx -t

# Nginx yeniden başlat
sudo systemctl restart nginx
```

### Yavaş Çalışıyor
```bash
# Daha fazla worker ekle
sudo nano /etc/systemd/system/photo-gallery.service

# -w 4 yerine -w 8 yap (CPU sayısı x 2)
ExecStart=/var/www/photo-gallery/venv/bin/gunicorn -w 8 -b 127.0.0.1:5001 web_app:app

# Yeniden başlat
sudo systemctl daemon-reload
sudo systemctl restart photo-gallery
```

---

## 📊 Performans İyileştirme

### 1. Redis Cache Ekle
```bash
sudo apt install redis-server -y
pip install flask-caching redis

# web_app.py'ye ekle:
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})
```

### 2. Fotoğraf Sıkıştırma
```python
# web_app.py'de upload fonksiyonuna ekle
from PIL import Image

def compress_image(filepath):
    img = Image.open(filepath)
    img.thumbnail((1920, 1080), Image.LANCZOS)
    img.save(filepath, optimize=True, quality=85)
```

### 3. CDN Kullan
- Cloudflare (ücretsiz)
- BunnyCDN
- AWS CloudFront

---

## 💰 Tahmini Maliyetler

### Küçük Ölçek (100-500 kullanıcı/ay)
- **DigitalOcean Droplet:** $6/ay
- **Hetzner VPS:** €4/ay
- **Vultr:** $5/ay

### Orta Ölçek (1000-5000 kullanıcı/ay)
- **DigitalOcean:** $12-24/ay
- **Hetzner:** €8-15/ay
- **AWS EC2:** $15-30/ay

### Domain & SSL
- **Domain:** $10-15/yıl
- **SSL:** Ücretsiz (Let's Encrypt)

---

## 📞 Destek

Sorun yaşarsan:
1. Logları kontrol et: `sudo journalctl -u photo-gallery -f`
2. Nginx logları: `sudo tail -f /var/log/nginx/error.log`
3. Permissions kontrol et: `ls -la /var/www/photo-gallery`

**Başarılar! 🎉**
