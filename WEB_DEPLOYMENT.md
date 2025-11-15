# 🌐 Ajans Fotoğraf Galerisi - Web Deployment

## 📋 Sistem Özellikleri

### Admin Paneli
- ✅ Güvenli giriş sistemi (username/password)
- ✅ Toplu fotoğraf yükleme
- ✅ Fotoğraf yönetimi (silme)
- ✅ İstatistikler (toplam fotoğraf, tarama, eşleşme)
- ✅ Otomatik yüz tanıma

### Oyuncu Arayüzü
- ✅ Selfie çekme veya fotoğraf yükleme
- ✅ Drag & drop desteği
- ✅ Otomatik yüz eşleştirme
- ✅ Benzerlik oranları ile sonuç gösterimi
- ✅ Fotoğraf indirme

## 🚀 Local Test (Geliştirme)

```bash
# 1. Bağımlılıkları yükle
pip3 install -r requirements_web.txt

# 2. Uygulamayı başlat
python3 web_app.py

# 3. Tarayıcıda aç
# Oyuncu: http://localhost:5001
# Admin: http://localhost:5001/admin/login
```

**Varsayılan Admin:**
- Kullanıcı: `admin`
- Şifre: `admin123`

## 🌍 Production Deployment

### Seçenek 1: VPS/Sunucu (DigitalOcean, AWS, Hetzner)

#### 1. Sunucu Hazırlığı
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nginx

# Python paketleri
pip3 install -r requirements_web.txt
pip3 install gunicorn
```

#### 2. Gunicorn ile Çalıştır
```bash
gunicorn -w 4 -b 0.0.0.0:5001 web_app:app
```

#### 3. Nginx Reverse Proxy
```nginx
# /etc/nginx/sites-available/photo-gallery
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /uploads {
        alias /path/to/uploads;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/photo-gallery /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Systemd Service (Otomatik Başlatma)
```ini
# /etc/systemd/system/photo-gallery.service
[Unit]
Description=Photo Gallery App
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/gunicorn -w 4 -b 127.0.0.1:5001 web_app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable photo-gallery
sudo systemctl start photo-gallery
```

### Seçenek 2: Heroku

```bash
# 1. Procfile oluştur
echo "web: gunicorn web_app:app" > Procfile

# 2. runtime.txt oluştur
echo "python-3.10.12" > runtime.txt

# 3. Deploy
heroku create your-app-name
git push heroku main
```

### Seçenek 3: Docker

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_web.txt .
RUN pip install --no-cache-dir -r requirements_web.txt

COPY . .

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "web_app:app"]
```

```bash
# Build ve çalıştır
docker build -t photo-gallery .
docker run -p 5001:5001 -v $(pwd)/uploads:/app/uploads photo-gallery
```

### Seçenek 4: Railway.app (Kolay & Ücretsiz)

1. GitHub'a push et
2. Railway.app'e git
3. "New Project" > "Deploy from GitHub"
4. Repository'yi seç
5. Otomatik deploy!

## 🔒 Güvenlik Önerileri

### 1. Admin Şifresini Değiştir
```python
# web_app.py içinde
admin_pass = hashlib.sha256('YENİ_GÜVENLİ_ŞİFRE'.encode()).hexdigest()
```

### 2. Secret Key Değiştir
```python
app.secret_key = 'rastgele-uzun-güvenli-key-buraya'
```

### 3. HTTPS Kullan (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 4. Dosya Boyutu Limiti
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### 5. Rate Limiting
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/upload_selfie', methods=['POST'])
@limiter.limit("10 per minute")
def upload_selfie():
    # ...
```

## 📊 Veritabanı Yönetimi

### SQLite (Varsayılan - Küçük/Orta Ölçek)
```bash
# Yedekleme
cp photo_gallery.db photo_gallery_backup.db

# Görüntüleme
sqlite3 photo_gallery.db
.tables
SELECT * FROM agency_photos;
```

### PostgreSQL'e Geçiş (Büyük Ölçek)
```bash
pip install psycopg2-binary
```

```python
# web_app.py içinde sqlite3 yerine
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="photo_gallery",
    user="postgres",
    password="password"
)
```

## 🎨 Özelleştirme

### Logo Ekleme
```html
<!-- templates/user_index.html -->
<img src="/static/logo.png" alt="Logo" style="max-width: 200px;">
```

### Renk Teması Değiştirme
```css
/* Gradient renklerini değiştir */
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### Email Bildirimleri
```bash
pip install flask-mail
```

```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'

mail = Mail(app)

# Eşleşme bulunduğunda email gönder
msg = Message('Fotoğrafların Bulundu!',
              sender='noreply@yourapp.com',
              recipients=['user@example.com'])
msg.body = f'{matches_count} fotoğraf bulundu!'
mail.send(msg)
```

## 📈 Performans Optimizasyonu

### 1. Fotoğraf Sıkıştırma
```python
from PIL import Image

def compress_image(filepath, max_size=(1920, 1080)):
    img = Image.open(filepath)
    img.thumbnail(max_size, Image.LANCZOS)
    img.save(filepath, optimize=True, quality=85)
```

### 2. Caching
```bash
pip install flask-caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/admin/stats')
@cache.cached(timeout=60)
def admin_stats():
    # ...
```

### 3. Background Jobs (Celery)
```bash
pip install celery redis
```

```python
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379/0')

@celery.task
def process_photo_async(filepath):
    # Yüz tanıma işlemini arka planda yap
    pass
```

## 🔍 Monitoring & Logs

### Application Logs
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app.logger.info('User uploaded photo')
```

### Error Tracking (Sentry)
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FlaskIntegration()]
)
```

## 💰 Maliyet Tahmini

### Küçük Ölçek (100-500 kullanıcı/ay)
- **Railway.app:** $0-5/ay (ücretsiz tier)
- **Heroku:** $7/ay (Hobby tier)
- **DigitalOcean:** $6/ay (Basic Droplet)

### Orta Ölçek (1000-5000 kullanıcı/ay)
- **DigitalOcean:** $12-24/ay
- **AWS EC2:** $15-30/ay
- **Hetzner:** €5-10/ay

### Büyük Ölçek (10000+ kullanıcı/ay)
- **AWS/GCP:** $50-200/ay
- **Dedicated Server:** $30-100/ay

## 📱 Mobil Uygulama (Bonus)

React Native veya Flutter ile mobil app:
- Kamera entegrasyonu
- Offline yüz tanıma
- Push notifications
- Fotoğraf galerisi

## 🆘 Sorun Giderme

### "Module not found" hatası
```bash
pip3 install -r requirements_web.txt
```

### "Permission denied" hatası
```bash
chmod 755 uploads/
chown -R www-data:www-data uploads/
```

### "Database locked" hatası
```python
# SQLite yerine PostgreSQL kullan
# veya WAL mode aktif et
conn.execute('PRAGMA journal_mode=WAL')
```

### Yavaş yüz tanıma
```python
# GPU desteği ekle (CUDA)
# veya encoding'leri cache'le
# veya background job kullan
```

## 📞 Destek

Sorularınız için:
- GitHub Issues
- Email: support@yourapp.com
- Discord: yourserver

---

**Başarılar! 🎉**
