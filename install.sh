#!/bin/bash

# Yüz Tanıma Web Uygulaması - Otomatik Kurulum Scripti
# Ubuntu/Debian için

set -e

echo "=================================="
echo "Yüz Tanıma Web App - Kurulum"
echo "=================================="
echo ""

# Root kontrolü
if [ "$EUID" -ne 0 ]; then 
    echo "Bu script root olarak çalıştırılmalı!"
    echo "Kullanım: sudo bash install.sh"
    exit 1
fi

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Domain adı sor
echo -e "${YELLOW}Domain adınızı girin (örn: example.com):${NC}"
read DOMAIN

if [ -z "$DOMAIN" ]; then
    echo -e "${RED}Domain adresi boş olamaz!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Kurulum başlıyor...${NC}"
echo ""

# 1. Sistem güncellemesi
echo -e "${YELLOW}[1/10] Sistem güncelleniyor...${NC}"
apt update && apt upgrade -y

# 2. Gerekli paketleri kur
echo -e "${YELLOW}[2/10] Gerekli paketler kuruluyor...${NC}"
apt install -y python3 python3-pip python3-venv build-essential cmake nginx

# 3. Proje klasörü oluştur
echo -e "${YELLOW}[3/10] Proje klasörü oluşturuluyor...${NC}"
mkdir -p /var/www/photo-gallery
cd /var/www/photo-gallery

# 4. Virtual environment
echo -e "${YELLOW}[4/10] Virtual environment oluşturuluyor...${NC}"
python3 -m venv venv
source venv/bin/activate

# 5. Python paketleri
echo -e "${YELLOW}[5/10] Python paketleri yükleniyor (bu uzun sürebilir)...${NC}"
pip install --upgrade pip
pip install Flask==3.0.0 face-recognition==1.3.0 Pillow==10.1.0 opencv-python==4.8.1.78 Werkzeug==3.0.1 gunicorn

# 6. Klasör izinleri
echo -e "${YELLOW}[6/10] Klasör izinleri ayarlanıyor...${NC}"
mkdir -p uploads/agency uploads/users
chown -R www-data:www-data /var/www/photo-gallery
chmod -R 755 /var/www/photo-gallery
chmod -R 777 uploads/

# 7. Systemd service
echo -e "${YELLOW}[7/10] Systemd service oluşturuluyor...${NC}"
cat > /etc/systemd/system/photo-gallery.service << EOF
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
EOF

systemctl daemon-reload
systemctl enable photo-gallery
systemctl start photo-gallery

# 8. Nginx config
echo -e "${YELLOW}[8/10] Nginx yapılandırılıyor...${NC}"
cat > /etc/nginx/sites-available/photo-gallery << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /uploads {
        alias /var/www/photo-gallery/uploads;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

ln -sf /etc/nginx/sites-available/photo-gallery /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# 9. Firewall
echo -e "${YELLOW}[9/10] Firewall ayarlanıyor...${NC}"
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# 10. SSL (Let's Encrypt)
echo -e "${YELLOW}[10/10] SSL sertifikası kuruluyor...${NC}"
apt install -y certbot python3-certbot-nginx

echo ""
echo -e "${GREEN}SSL sertifikası için email adresinizi girin:${NC}"
read EMAIL

if [ ! -z "$EMAIL" ]; then
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m $EMAIL --redirect
else
    echo -e "${YELLOW}Email girilmedi, SSL atlandı. Manuel kurulum:${NC}"
    echo "sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
fi

# Durum kontrolü
echo ""
echo "=================================="
echo -e "${GREEN}✅ Kurulum Tamamlandı!${NC}"
echo "=================================="
echo ""
echo "Siteniz: https://$DOMAIN"
echo "Admin Panel: https://$DOMAIN/admin/login"
echo ""
echo "Varsayılan Admin:"
echo "  Kullanıcı: admin"
echo "  Şifre: admin123"
echo ""
echo -e "${RED}ÖNEMLİ: Admin şifresini değiştirin!${NC}"
echo "  nano /var/www/photo-gallery/web_app.py"
echo ""
echo "Yönetim Komutları:"
echo "  Yeniden başlat: sudo systemctl restart photo-gallery"
echo "  Logları gör: sudo journalctl -u photo-gallery -f"
echo "  Durum: sudo systemctl status photo-gallery"
echo ""
echo -e "${GREEN}Başarılar! 🎉${NC}"
