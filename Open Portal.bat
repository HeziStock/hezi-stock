@echo off
cd /d "%~dp0"
echo HEZI STOCK - Starting portal...
python -c "import sys; print('Python:', sys.executable)" 2>nul || (echo Error: Python not found. Install Python. & pause & exit /b 1)
echo.
start "HEZI STOCK Server" python app.py
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000/app
echo.
echo Browser opened. Server runs in the "HEZI STOCK Server" window - do not close it.
echo To stop the site, close that window.
pause
