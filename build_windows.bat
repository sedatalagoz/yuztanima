@echo off
echo ==================================
echo Yuz Tanima - Windows Build Script
echo ==================================
echo.

REM PyInstaller kontrolu
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller bulunamadi. Yukleniyor...
    pip install pyinstaller
)

REM Eski build'leri temizle
echo Eski build dosyalari temizleniyor...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build baslat
echo Build baslatiliyor...
pyinstaller build_windows.spec

REM Kontrol et
if exist "dist\YuzTanima.exe" (
    echo.
    echo ==================================
    echo Build basarili!
    echo ==================================
    echo.
    echo Uygulama konumu: dist\YuzTanima.exe
    echo.
    echo Calistirmak icin:
    echo   dist\YuzTanima.exe
    echo.
    echo Veya Explorer'da dist klasorune git ve YuzTanima.exe'ye cift tikla
    echo.
) else (
    echo Build basarisiz!
    echo Hata detaylari icin yukaridaki ciktiyi kontrol edin.
    exit /b 1
)

pause
