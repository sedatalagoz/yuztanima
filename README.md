# 🔍 Yüz Tanıma Uygulaması

Tamamen local ve offline çalışan Python tabanlı yüz tanıma uygulaması.

## 📋 Kurulum Adımları

### 1. Python Kurulumu
Python 3.8 veya üzeri gereklidir. Kontrol etmek için:
```bash
python3 --version
```

### 2. Proje Klasörüne Git
```bash
cd /path/to/project
```

### 3. Virtual Environment Oluştur (Önerilen)
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 4. Gerekli Paketleri Yükle
```bash
pip install -r requirements.txt
```

**Not:** `face-recognition` paketi kurulurken `dlib` kütüphanesi de kurulacaktır. Bu işlem birkaç dakika sürebilir.

macOS'ta sorun yaşarsanız:
```bash
brew install cmake
pip install dlib
pip install -r requirements.txt
```

## 🚀 Çalıştırma

### Uygulamayı Başlat
```bash
python3 app.py
```

### Tarayıcıda Aç
Uygulama başladıktan sonra tarayıcınızda şu adresi açın:
```
http://127.0.0.1:5000
```
veya
```
http://localhost:5000
```

## 📖 Kullanım

1. **Klasör Yolu Gir:** Taranacak fotoğrafların bulunduğu klasörün tam yolunu girin
   - Örnek: `/Users/kullanici/Desktop/fotograflar`

2. **Fotoğraf Yükle:** Eşleştirilecek fotoğrafı seçin (.jpg, .jpeg, .png)

3. **Eşleştir:** Butona tıklayın ve sonuçları bekleyin

4. **Sonuçlar:** Eşleşen fotoğraflar benzerlik oranlarıyla birlikte gösterilecektir

## ✨ Özellikler

- ✅ Tamamen offline çalışır
- ✅ Hiçbir API veya internet bağlantısı gerektirmez
- ✅ Yüz olmayan fotoğraflarda hata vermez
- ✅ Sadece .jpg, .jpeg, .png formatlarını kabul eder
- ✅ Bootstrap ile modern ve şık arayüz
- ✅ Benzerlik oranlarını gösterir
- ✅ Grid şeklinde sonuç gösterimi

## 🛑 Uygulamayı Durdurma

Terminal'de `Ctrl + C` tuşlarına basın.

## 📁 Proje Yapısı

```
project/
├── app.py              # Ana Flask uygulaması
├── requirements.txt    # Python bağımlılıkları
├── templates/
│   └── index.html     # Web arayüzü
└── static/
    └── uploads/       # Yüklenen fotoğraflar
```

## ⚠️ Notlar

- İlk kurulumda `face-recognition` paketi biraz zaman alabilir
- Büyük klasörlerde tarama işlemi uzun sürebilir
- En iyi sonuçlar için net ve yüksek kaliteli fotoğraflar kullanın
