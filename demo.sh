#!/bin/bash

echo "=================================="
echo "🎬 Demo Başlatılıyor..."
echo "=================================="
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ngrok kontrolü
if ! command -v ngrok &> /dev/null
then
    echo -e "${YELLOW}ngrok bulunamadı!${NC}"
    echo ""
    echo "Kurulum:"
    echo "  macOS: brew install ngrok"
    echo "  veya: https://ngrok.com/download"
    echo ""
    exit 1
fi

# Uygulamayı başlat
echo -e "${YELLOW}[1/2] Uygulama başlatılıyor...${NC}"
python3 web_app.py > /dev/null 2>&1 &
APP_PID=$!

# Başlamasını bekle
sleep 4

# Kontrol et
if ps -p $APP_PID > /dev/null; then
    echo -e "${GREEN}✅ Uygulama başladı!${NC}"
else
    echo -e "${RED}❌ Uygulama başlatılamadı!${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}[2/2] Tunnel açılıyor...${NC}"
echo ""
echo -e "${BLUE}=================================="
echo "📡 DEMO LİNKİ HAZIRLANIYOR..."
echo "==================================${NC}"
echo ""
echo -e "${GREEN}Müşteriye göndereceğin link aşağıda görünecek!${NC}"
echo ""

# ngrok başlat
ngrok http 5001

# Temizlik (ngrok kapandığında)
echo ""
echo -e "${YELLOW}Demo sonlandırılıyor...${NC}"
kill $APP_PID 2>/dev/null
echo -e "${GREEN}✅ Temizlendi!${NC}"
