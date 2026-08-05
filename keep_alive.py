import urllib.request
import time

url = "https://bca-face-attendance.onrender.com/"
print(f"Keep-Alive Service Started! Pinging {url} every 4 minutes to prevent Render sleep mode...")

while True:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            status = response.getcode()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Ping Success! HTTP Status: {status}")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Ping Notice: {e}")
    time.sleep(240) # 4 minutes
