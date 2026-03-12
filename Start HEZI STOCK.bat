@echo off
title HEZI STOCK
cd /d "%~dp0"

REM Start the server in its own window (user closes that window to stop the server)
start "HEZI STOCK Server" python app.py

REM Wait for the server to be ready
timeout /t 3 /nobreak >nul

REM Open the portal in the default browser
start "" http://127.0.0.1:5000

exit
