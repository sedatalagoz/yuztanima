@echo off
echo ==================================
echo Windows Installer Olusturuluyor
echo ==================================
echo.

REM Inno Setup kontrolu
set INNO_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if not exist %INNO_PATH% (
    echo Hata: Inno Setup bulunamadi!
    echo.
    echo Lutfen Inno Setup'i indirin ve kurun:
    echo https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

REM Uygulama kontrolu
if not exist "dist\YuzTanima.exe" (
    echo Hata: dist\YuzTanima.exe bulunamadi!
    echo Once build_windows.bat calistirin.
    echo.
    pause
    exit /b 1
)

REM Installer klasoru olustur
if not exist "installer" mkdir installer

REM Installer olustur
echo Installer olusturuluyor...
%INNO_PATH% installer_windows.iss

if exist "installer\YuzTanima-Setup.exe" (
    echo.
    echo ==================================
    echo Installer basariyla olusturuldu!
    echo ==================================
    echo.
    echo Dosya: installer\YuzTanima-Setup.exe
    echo.
    echo Kullanim:
    echo 1. YuzTanima-Setup.exe dosyasina cift tikla
    echo 2. Kurulum sihirbazini takip et
    echo 3. Kurulum tamamlandiktan sonra uygulamayi ac
    echo.
) else (
    echo Installer olusturulamadi!
    pause
    exit /b 1
)

pause
