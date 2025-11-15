# 🎁 Yüz Tanıma - Kurulumlu Uygulama

Uygulamanızı macOS ve Windows için **standalone executable** (kurulumlu uygulama) haline getirin!

## 🚀 Hızlı Başlangıç

### macOS için:
```bash
# 1. PyInstaller'ı yükle
pip3 install pyinstaller

# 2. Build script'ini çalıştır
./build_macos.sh

# 3. Uygulamayı çalıştır
open dist/YuzTanima.app
```

### Windows için:
```cmd
# 1. PyInstaller'ı yükle
pip install pyinstaller

# 2. Build script'ini çalıştır
build_windows.bat

# 3. Uygulamayı çalıştır
dist\YuzTanima.exe
```

## 📦 Ne Elde Edersiniz?

✅ **Tek dosya uygulama** - Python kurulumu gerektirmez
✅ **Otomatik tarayıcı açma** - Uygulama başladığında tarayıcı otomatik açılır
✅ **Taşınabilir** - Herhangi bir bilgisayarda çalışır
✅ **Kolay dağıtım** - ZIP'leyip paylaşın

## 📊 Dosya Boyutları

- **macOS:** ~200-300 MB (YuzTanima.app)
- **Windows:** ~200-300 MB (YuzTanima.exe)

Tüm Python kütüphaneleri ve bağımlılıklar dahil!

## 🎯 Kullanım

1. **Uygulamayı çalıştır:**
   - macOS: `YuzTanima.app` dosyasına çift tıkla
   - Windows: `YuzTanima.exe` dosyasına çift tıkla

2. **Tarayıcı otomatik açılacak** (http://127.0.0.1:5001)

3. **Uygulamayı kullan:**
   - Klasör seç
   - Fotoğraf yükle
   - Eşleştir!

4. **Kapatmak için:** Terminal/Konsol penceresini kapat

## ⚠️ İlk Çalıştırma Uyarıları

### macOS
"Tanımlanamayan geliştirici" uyarısı alabilirsiniz:
- Sağ tıklayıp **"Aç"** seçin
- Veya: **Sistem Ayarları > Gizlilik ve Güvenlik > "Yine de Aç"**

### Windows
"Windows korumalı PC'nizi korudu" uyarısı alabilirsiniz:
- **"Daha fazla bilgi"** tıklayın
- **"Yine de çalıştır"** seçin

## 📁 Veri Depolama

Yüklenen fotoğraflar:
- **macOS:** `~/.yuz_tanima/uploads/`
- **Windows:** `C:\Users\[Kullanici]\.yuz_tanima\uploads\`

## 🎨 Özelleştirme

### Özel İkon Eklemek

1. 512x512 PNG ikon oluştur
2. macOS için `.icns`, Windows için `.ico` formatına çevir
3. Spec dosyasında `icon='icon.icns'` veya `icon='icon.ico'` ekle
4. Yeniden build et

### Konsol Penceresini Gizlemek

Spec dosyasında `console=True` yerine `console=False` yap.

## 🔧 Sorun Giderme

### "Module not found" hatası
```bash
pip install --upgrade pyinstaller
```

### macOS: "App is damaged"
```bash
xattr -cr dist/YuzTanima.app
```

### Windows: dlib kurulum hatası
Önceden derlenmiş wheel kullanın:
```cmd
pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp38-cp38-win_amd64.whl
```

## 📤 Dağıtım

### Basit Yöntem (ZIP)
```bash
# macOS
zip -r YuzTanima-macOS.zip dist/YuzTanima.app

# Windows
# dist\YuzTanima.exe dosyasını sağ tıklayıp "Sıkıştır" seçin
```

### Profesyonel Installer

**macOS - DMG:**
```bash
brew install create-dmg
create-dmg --volname "Yüz Tanıma" YuzTanima-Installer.dmg dist/YuzTanima.app
```

**Windows - Inno Setup:**
- Inno Setup indir: https://jrsoftware.org/isdl.php
- `BUILD_INSTRUCTIONS.md` dosyasındaki örnek script'i kullan

## 📋 Detaylı Dokümantasyon

Daha fazla bilgi için `BUILD_INSTRUCTIONS.md` dosyasına bakın.

## ✨ Özellikler

- 🔒 Tamamen offline çalışır
- 🚀 Hızlı ve kolay kurulum
- 💻 Cross-platform (macOS & Windows)
- 🎯 Kullanıcı dostu arayüz
- 📦 Tek dosya dağıtım
- 🔄 Otomatik tarayıcı açma

## 🎉 Başarılar!

Artık uygulamanızı herkesle paylaşabilirsiniz - Python kurulumu gerektirmeden!
