@echo off
cd /d "C:\Users\hezima\stock-tracker"
echo Starting Stock Tracker portal...
start /B python app.py
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000
echo Browser opened. Keep this window open while using the portal.
pause
