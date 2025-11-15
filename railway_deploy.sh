#!/bin/bash

echo "=================================="
echo "🚂 Railway Deploy Hazırlığı"
echo "=================================="
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Git kontrolü
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git kurulu değil!${NC}"
    echo "Kurulum: brew install git"
    exit 1
fi

# GitHub repo bilgilerini al
echo -e "${YELLOW}GitHub kullanıcı adın:${NC}"
read GITHUB_USER

echo -e "${YELLOW}Repo adı (örn: yuztanima):${NC}"
read REPO_NAME

if [ -z "$GITHUB_USER" ] || [ -z "$REPO_NAME" ]; then
    echo -e "${RED}Kullanıcı adı ve repo adı gerekli!${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[1/4] Git repository başlatılıyor...${NC}"

# Git init
if [ ! -d .git ]; then
    git init
    echo -e "${GREEN}✅ Git başlatıldı${NC}"
else
    echo -e "${YELLOW}⚠️  Git zaten başlatılmış${NC}"
fi

# Dosyaları ekle
echo ""
echo -e "${BLUE}[2/4] Dosyalar ekleniyor...${NC}"
git add .
git commit -m "Initial commit for Railway deployment" 2>/dev/null || echo -e "${YELLOW}⚠️  Değişiklik yok veya zaten commit edilmiş${NC}"

# Remote ekle
echo ""
echo -e "${BLUE}[3/4] GitHub remote ekleniyor...${NC}"
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
git branch -M main

echo -e "${GREEN}✅ Remote eklendi${NC}"

# Push
echo ""
echo -e "${BLUE}[4/4] GitHub'a yükleniyor...${NC}"
echo ""
echo -e "${YELLOW}GitHub şifren veya token'ın istenecek${NC}"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=================================="
    echo "✅ GitHub'a Yükleme Tamamlandı!"
    echo "==================================${NC}"
    echo ""
    echo -e "${BLUE}Şimdi Railway'e deploy et:${NC}"
    echo ""
    echo "1. https://railway.app adresine git"
    echo "2. 'Login with GitHub' ile giriş yap"
    echo "3. 'New Project' tıkla"
    echo "4. 'Deploy from GitHub repo' seç"
    echo "5. '$REPO_NAME' repo'sunu seç"
    echo "6. 'Deploy Now' tıkla"
    echo ""
    echo "5-10 dakika sonra siteniz hazır! 🚀"
    echo ""
    echo -e "${YELLOW}Link örneği:${NC}"
    echo "https://$REPO_NAME-production.up.railway.app"
    echo ""
else
    echo ""
    echo -e "${RED}=================================="
    echo "❌ GitHub'a Yükleme Başarısız!"
    echo "==================================${NC}"
    echo ""
    echo -e "${YELLOW}Olası nedenler:${NC}"
    echo "1. GitHub'da repo oluşturmadın"
    echo "   → https://github.com/new adresine git"
    echo "   → Repo adı: $REPO_NAME"
    echo ""
    echo "2. Yanlış kullanıcı adı/şifre"
    echo "   → GitHub şifreni kontrol et"
    echo ""
    echo "3. Token gerekiyor"
    echo "   → https://github.com/settings/tokens"
    echo "   → 'Generate new token (classic)'"
    echo "   → 'repo' yetkisini seç"
    echo ""
fi
