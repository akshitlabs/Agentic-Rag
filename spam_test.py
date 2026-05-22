import urllib.request
import urllib.error

print("⚔️ Spam Attack Shuru ho raha hai...\n")

for i in range(8): # Hum 8 baar jaldi-jaldi request bhejenge
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8000/health")
        print(f"Request {i+1}: ✅ Pass ho gayi (Status 200)")
    except urllib.error.HTTPError as e:
        print(f"Request {i+1}: 🛑 BLOCKED! (Status {e.code})")