#!/bin/bash

echo "=================================="
echo "DMG Installer Oluşturuluyor"
echo "=================================="
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# create-dmg kontrolü
if ! command -v create-dmg &> /dev/null
then
    echo -e "${YELLOW}create-dmg bulunamadı. Yükleniyor...${NC}"
    brew install create-dmg
fi

# Uygulama kontrolü
if [ ! -d "dist/YuzTanima.app" ]; then
    echo -e "${RED}Hata: dist/YuzTanima.app bulunamadı!${NC}"
    echo "Önce ./build_macos.sh çalıştırın."
    exit 1
fi

# DMG oluştur
echo -e "${GREEN}DMG oluşturuluyor...${NC}"

create-dmg \
  --volname "Yüz Tanıma" \
  --volicon "dist/YuzTanima.app/Contents/Resources/icon-windowed.icns" \
  --window-pos 200 120 \
  --window-size 800 450 \
  --icon-size 100 \
  --icon "YuzTanima.app" 200 190 \
  --hide-extension "YuzTanima.app" \
  --app-drop-link 600 185 \
  --no-internet-enable \
  "YuzTanima-Installer.dmg" \
  "dist/YuzTanima.app" 2>/dev/null

if [ -f "YuzTanima-Installer.dmg" ]; then
    echo ""
    echo -e "${GREEN}=================================="
    echo "✅ DMG Installer başarıyla oluşturuldu!"
    echo "==================================${NC}"
    echo ""
    echo "Dosya: YuzTanima-Installer.dmg"
    SIZE=$(du -sh YuzTanima-Installer.dmg | cut -f1)
    echo "Boyut: $SIZE"
    echo ""
    echo "Kullanım:"
    echo "1. DMG dosyasına çift tıkla"
    echo "2. YuzTanima.app'i Applications klasörüne sürükle"
    echo "3. Launchpad'den veya Applications'dan aç"
    echo ""
else
    echo -e "${RED}❌ DMG oluşturulamadı!${NC}"
    exit 1
fi
