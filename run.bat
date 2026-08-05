@echo off
title Starting BCA Face Recognition Attendance System...
echo =========================================================
echo 1. Cleaning up any old background server processes...
echo =========================================================
taskkill /F /IM python.exe 2>nul
timeout /t 1 /nobreak >nul

echo =========================================================
echo 2. Starting Django Web Server on http://localhost:8000
echo =========================================================
start /b python manage.py runserver 8000

echo =========================================================
echo 3. Opening Website in your Browser Automatically...
echo =========================================================
timeout /t 3 /nobreak >nul
start http://localhost:8000

echo =========================================================
echo SUCCESS! System is active. Close this window to stop server.
echo =========================================================
pause
