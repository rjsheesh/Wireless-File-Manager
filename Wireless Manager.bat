@echo off
title fabiTECH - Wireless Scrcpy ^& File Manager
color 0A

:: Setting up the custom paths for ADB and SCRCPY
set "ADB_PATH=C:\Users\nuLL\Desktop\Capcut Project\CapCut\Videos\platform-tools"
set "SCRCPY_PATH=C:\Users\nuLL\Desktop\Capcut Project\CapCut\Videos\scrcpy-win64-v3.3.4"
set "PATH=%ADB_PATH%;%SCRCPY_PATH%;%PATH%"

echo ==========================================
echo        fabiTECH Wireless Manager
echo ==========================================
echo.
echo Make sure your phone is connected via USB first!
echo.

:: IP বের করার কোড
echo [*] Searching for phone's Wi-Fi IP address...
set "ip="
for /f "tokens=2 delims= " %%A in ('adb shell ip addr show wlan0 ^| find "inet "') do (
    for /f "tokens=1 delims=/" %%B in ("%%A") do set "ip=%%B"
)

if "%ip%"=="" (
    echo [!] Could not find IP automatically.
    set /p ip="Please enter your phone's Wi-Fi IP manually: "
) else (
    echo [+] Auto-detected IP: %ip%
)

echo.
echo [+] Enabling TCP/IP port 5555...
adb tcpip 5555
timeout /t 3 >nul

echo [+] Connecting to %ip%...
adb connect %ip%:5555
timeout /t 2 >nul

echo.
echo [!] Connected successfully!
echo You can unplug the USB cable now.
pause

:MENU
cls
echo ==========================================
echo        fabiTECH - Main Menu
echo        Device IP: %ip%
echo ==========================================
echo [1] Start Scrcpy (Screen Mirroring)
echo [2] Download Alight Motion Video to PC
echo [3] Send a File to Mobile (Download Folder)
echo [4] Disconnect ^& Exit
echo ==========================================
set /p choice="Choose an option (1-4): "

if "%choice%"=="1" goto SCRCPY
if "%choice%"=="2" goto PULL
if "%choice%"=="3" goto PUSH
if "%choice%"=="4" goto EXIT

:: অপশনগুলো ভুল চাপলে আবার মেনুতে ফেরত যাবে
goto MENU

:SCRCPY
echo.
echo [+] Starting Scrcpy...
scrcpy -s %ip%:5555
pause
goto MENU

:PULL
echo.
echo [+] Downloading Video from /sdcard/Movies/Alight Motion...
:: Space থাকার কারণে কোটেশন মার্ক দেওয়া হয়েছে
adb -s %ip%:5555 pull "/sdcard/Movies/Alight Motion" "C:\Users\nuLL\Desktop\Capcut Project\CapCut\Videos\Downloads"
echo.
echo [+] Done! Check the "Videos" folder on your PC.
pause
goto MENU

:PUSH
echo.
echo [+] Select the file from your PC that you want to send.
echo [!] Just DRAG AND DROP the file into this CMD window, then press Enter:
set /p filepath="File path: "
:: Drag and drop করলে ফাইলের নামের দুইপাশে " " চলে আসে, সেটা সরানোর জন্য:
set filepath=%filepath:"=%
echo.
echo [+] Sending file to your phone's Download folder...
adb -s %ip%:5555 push "%filepath%" /sdcard/Download/
echo.
echo [+] Done! Check the "Download" folder on your mobile.
pause
goto MENU

:EXIT
echo.
echo [+] Disconnecting Device...
adb disconnect %ip%:5555
echo [+] Goodbye!
timeout /t 2 >nul
exit