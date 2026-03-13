@echo off
cd /d "%~dp0"
title HEZI STOCK Portal
echo.
echo ============================================
echo   HEZI STOCK - Starting portal...
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found. Add Python to PATH or run from Anaconda prompt.
    echo.
    pause
    exit /b 1
)

echo Python: 
python -c "import sys; print('  ', sys.executable)"
echo.
echo Opening browser in 3 seconds. Keep this window open.
echo Dashboard: http://127.0.0.1:5000/app
echo.
start "" http://127.0.0.1:5000/app
timeout /t 3 /nobreak >nul

python app.py
echo.
echo Server stopped. If you see an error above, fix it and run again.
pause
