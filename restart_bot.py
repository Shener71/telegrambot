import subprocess
import time

while True:
    try:
        print("Bot başlatılıyor...")
        subprocess.run(["python", "bot.py"])  # Botun ana dosyasını çalıştır
    except Exception as e:
        print(f"Bot hata aldı: {e}")
    
    print("Bot çöktü! 5 saniye sonra tekrar başlatılıyor...")
    time.sleep(5)  # Bot çöktüğünde 5 saniye bekleyip tekrar çalıştır
