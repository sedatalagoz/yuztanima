# 🔑 GitHub Token Oluşturma

## Hızlı Adımlar:

### 1. Token Oluştur
https://github.com/settings/tokens/new

### 2. Ayarlar:
- **Note:** Railway Deploy
- **Expiration:** 90 days
- **Select scopes:** ✅ **repo** (tümünü seç)

### 3. Generate token tıkla

### 4. Token'ı kopyala (bir daha gösterilmez!)

### 5. Push komutu:
```bash
git push -u origin main
```

**Username:** sedatalagoz
**Password:** TOKEN_BURAYA_YAPIŞTIR (şifre değil, token!)

---

## Alternatif: SSH Kullan (Daha Kolay)

```bash
# Remote'u değiştir
git remote set-url origin git@github.com:sedatalagoz/yuztanima.git

# SSH key yoksa oluştur
ssh-keygen -t ed25519 -C "sedatalagoz@gmail.com"

# Public key'i kopyala
cat ~/.ssh/id_ed25519.pub

# GitHub'a ekle
# https://github.com/settings/keys
# "New SSH key" tıkla, yapıştır

# Push
git push -u origin main
```
