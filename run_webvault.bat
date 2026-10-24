@echo off
title WebVault Runner - Kho Mau Website Cao Cap
cd /d "%~dp0"

echo ====================================================================
echo   WebVault - Thu Vien Mau Website Cao Cap (Dark Zeit Edition)
echo   Dang khoi chay may chu cuc bo an toan...
echo ====================================================================

python _Luu_Tru_Ky_Thuat\01_Scripts_Bo_Tro\run_server.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [-] Khong the khoi dong Python. Vui long kiem tra Python tren may.
    pause
)
