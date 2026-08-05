Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\ELCOT\.gemini\antigravity\scratch\bca-face-attendance-django"
WshShell.Run "cmd /c taskkill /F /IM python.exe 2>nul & python manage.py runserver 0.0.0.0:8000", 0, False
