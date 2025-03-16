import os
import yt_dlp
import json
import time
from flask import Flask, jsonify
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

JSON_FILE = "top100.json"

def update_top100():
    """YouTube Music Top 100 listesini her 3 günde bir günceller."""
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'sleep_interval': 10,  # Ban yememek için minimum 10 saniye bekle
        'max_sleep_interval': 40,  # Maksimum 40 saniye bekle
    }

    try:
        print("🔄 YouTube Music Top 100 listesi güncelleniyor...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
        
        tracks = []
        if 'entries' in info:
            for entry in info['entries']:
                title = entry.get('title', 'Bilinmeyen Şarkı')
                artist = entry.get('uploader', 'Bilinmeyen Sanatçı')
                audio_url = f"https://music.youtube.com/watch?v={entry.get('id', '')}"

                tracks.append({
                    'title': title,
                    'artist': artist,
                    'audioUrl': audio_url
                })

        # JSON olarak kaydet
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump({'tracks': tracks}, f, indent=4, ensure_ascii=False)

        print("✅ Top 100 listesi başarıyla güncellendi!")

    except Exception as e:
        print(f"❌ Güncelleme başarısız: {e}")

# Terminal kapanırsa bile en son veriyi döndür
@app.route('/top100', methods=['GET'])
def get_top100():
    """Son güncellenmiş Top 100 listesini döndürür."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Top 100 listesi bulunamadı!"})

# İlk çalıştırmada güncelleme yap
if not os.path.exists(JSON_FILE):
    update_top100()

# Her 3 günde bir çalıştır (Gece 03:00'te)
scheduler.add_job(id='three_day_update', func=update_top100, trigger='cron', day="*/3", hour=3)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
