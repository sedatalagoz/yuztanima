#!/bin/bash

echo "=================================="
echo "Yüz Tanıma - macOS Build Script"
echo "=================================="
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# PyInstaller kontrolü
if ! command -v pyinstaller &> /dev/null
then
    echo -e "${YELLOW}PyInstaller bulunamadı. Yükleniyor...${NC}"
    pip3 install pyinstaller
fi

# Eski build'leri temizle
echo -e "${YELLOW}Eski build dosyaları temizleniyor...${NC}"
rm -rf build dist *.spec.bak

# Build başlat
echo -e "${GREEN}Build başlatılıyor...${NC}"
pyinstaller build_macos.spec

# Kontrol et
if [ -d "dist/YuzTanima.app" ]; then
    echo ""
    echo -e "${GREEN}=================================="
    echo "✅ Build başarılı!"
    echo "==================================${NC}"
    echo ""
    echo "Uygulama konumu: dist/YuzTanima.app"
    echo ""
    echo "Çalıştırmak için:"
    echo "  open dist/YuzTanima.app"
    echo ""
    echo "Veya Finder'da dist klasörüne git ve YuzTanima.app'e çift tıkla"
    echo ""
    
    # Dosya boyutunu göster
    SIZE=$(du -sh dist/YuzTanima.app | cut -f1)
    echo "Dosya boyutu: $SIZE"
    echo ""
else
    echo -e "${RED}❌ Build başarısız!${NC}"
    echo "Hata detayları için yukarıdaki çıktıyı kontrol edin."
    exit 1
fi
