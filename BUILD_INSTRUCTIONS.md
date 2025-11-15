# 📦 Yüz Tanıma Uygulaması - Kurulum Paketi Oluşturma

Bu rehber, uygulamayı macOS ve Windows için standalone executable (çalıştırılabilir) dosya haline getirme adımlarını içerir.

## 🍎 macOS için Build

### 1. Gerekli Paketleri Yükle
```bash
pip3 install -r requirements_build.txt
```

### 2. Uygulamayı Test Et
```bash
python3 app_desktop.py
```
Tarayıcı otomatik açılmalı ve uygulama çalışmalı.

### 3. Executable Oluştur
```bash
pyinstaller build_macos.spec
```

### 4. Sonuç
Build tamamlandığında `dist/YuzTanima.app` dosyası oluşacak.

**Kullanım:**
- `YuzTanima.app` dosyasına çift tıkla
- Tarayıcı otomatik açılacak
- Uygulamayı kullan
- Kapatmak için terminal penceresini kapat

**Dağıtım:**
- `YuzTanima.app` dosyasını ZIP'le
- Diğer Mac kullanıcılarına gönder
- Hiçbir Python kurulumu gerektirmez!

---

## 🪟 Windows için Build

### 1. Gerekli Paketleri Yükle
```cmd
pip install -r requirements_build.txt
```

**Not:** Windows'ta `dlib` kurulumu için Visual Studio Build Tools gerekebilir:
- https://visualstudio.microsoft.com/downloads/
- "Build Tools for Visual Studio" indir ve kur
- "Desktop development with C++" seçeneğini işaretle

Alternatif olarak, önceden derlenmiş dlib wheel dosyası kullan:
```cmd
pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp38-cp38-win_amd64.whl
```

### 2. Uygulamayı Test Et
```cmd
python app_desktop.py
```

### 3. Executable Oluştur
```cmd
pyinstaller build_windows.spec
```

### 4. Sonuç
Build tamamlandığında `dist/YuzTanima.exe` dosyası oluşacak.

**Kullanım:**
- `YuzTanima.exe` dosyasına çift tıkla
- Tarayıcı otomatik açılacak
- Uygulamayı kullan
- Kapatmak için konsol penceresini kapat

**Dağıtım:**
- `YuzTanima.exe` dosyasını ZIP'le
- Diğer Windows kullanıcılarına gönder
- Hiçbir Python kurulumu gerektirmez!

---

## 📝 Önemli Notlar

### Dosya Boyutu
- macOS: ~200-300 MB
- Windows: ~200-300 MB
- Tüm Python kütüphaneleri ve bağımlılıklar dahil

### İlk Çalıştırma
- **macOS:** "Tanımlanamayan geliştirici" uyarısı alabilirsiniz
  - Sağ tıklayıp "Aç" seçin
  - Veya: Sistem Ayarları > Gizlilik ve Güvenlik > "Yine de Aç"
  
- **Windows:** "Windows korumalı PC'nizi korudu" uyarısı alabilirsiniz
  - "Daha fazla bilgi" tıklayın
  - "Yine de çalıştır" seçin

### Veri Depolama
Yüklenen fotoğraflar şu konumda saklanır:
- **macOS:** `~/.yuz_tanima/uploads/`
- **Windows:** `C:\Users\[Kullanıcı]\.yuz_tanima\uploads\`

### Performans
- İlk açılış 5-10 saniye sürebilir
- Sonraki açılışlar daha hızlı olacaktır

---

## 🔧 Sorun Giderme

### Build Hatası: "Module not found"
```bash
pip install --upgrade pyinstaller
```

### macOS: "App is damaged"
```bash
xattr -cr dist/YuzTanima.app
```

### Windows: dlib kurulum hatası
Önceden derlenmiş wheel dosyasını kullanın (yukarıda belirtildi)

### Uygulama açılmıyor
- Antivirüs yazılımını geçici olarak devre dışı bırakın
- Firewall'da port 5001'i açın

---

## 🚀 Gelişmiş Özellikler

### Özel İkon Eklemek

**macOS:**
1. 512x512 PNG ikon oluştur
2. `iconutil` ile .icns'e çevir
3. `build_macos.spec` içinde `icon='icon.icns'` ekle

**Windows:**
1. 256x256 PNG ikon oluştur
2. Online araçla .ico'ya çevir
3. `build_windows.spec` içinde `icon='icon.ico'` ekle

### Konsol Penceresini Gizlemek

Spec dosyasında `console=True` yerine `console=False` yap.

**Not:** Hata ayıklama için konsol açık bırakılması önerilir.

---

## 📦 Otomatik Installer Oluşturma

### macOS - DMG Oluşturma
```bash
# create-dmg aracını kur
brew install create-dmg

# DMG oluştur
create-dmg \
  --volname "Yüz Tanıma" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --app-drop-link 600 185 \
  "YuzTanima-Installer.dmg" \
  "dist/YuzTanima.app"
```

### Windows - Inno Setup
1. Inno Setup indir: https://jrsoftware.org/isdl.php
2. Aşağıdaki script'i `installer.iss` olarak kaydet:

```iss
[Setup]
AppName=Yüz Tanıma
AppVersion=1.0
DefaultDirName={pf}\YuzTanima
DefaultGroupName=Yüz Tanıma
OutputDir=installer
OutputBaseFilename=YuzTanima-Setup

[Files]
Source: "dist\YuzTanima.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Yüz Tanıma"; Filename: "{app}\YuzTanima.exe"
Name: "{commondesktop}\Yüz Tanıma"; Filename: "{app}\YuzTanima.exe"
```

3. Inno Setup Compiler ile derle

---

## ✅ Test Checklist

Build sonrası test et:

- [ ] Uygulama açılıyor
- [ ] Tarayıcı otomatik açılıyor
- [ ] Klasör seçimi çalışıyor
- [ ] Fotoğraf yükleme çalışıyor
- [ ] Yüz tanıma çalışıyor
- [ ] Sonuçlar gösteriliyor
- [ ] Uygulama düzgün kapanıyor

---

## 📧 Destek

Sorun yaşarsanız:
1. `app_desktop.py` dosyasını direkt Python ile çalıştırıp test edin
2. Konsol çıktısını kontrol edin
3. Log dosyalarını inceleyin

İyi kullanımlar! 🎉
