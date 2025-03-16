import yt_dlp
import json
import time
import threading
from flask import Flask, jsonify

app = Flask(__name__)

JSON_FILE = "top100.json"

def get_top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"

    ydl_opts = {
        'quiet': False,
        'format': 'bestaudio/best',
        'extract_flat': False,
        'noplaylist': False,
        'force_generic_extractor': False,
        'sleep_interval': 3,
        'max_sleep_interval': 7,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)

        tracks = []
        if 'entries' in playlist_info:
            for entry in playlist_info['entries']:
                if entry is None:
                    continue

                title = entry.get('title', 'Bilinmeyen Şarkı')
                artist = entry.get('uploader', 'Bilinmeyen Sanatçı')

                ydl_opts_audio = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
                    audio_info = ydl_audio.extract_info(entry['url'], download=False)
                
                audio_url = audio_info.get('url', '')

                tracks.append({'title': title, 'artist': artist, 'audioUrl': audio_url})

        # JSON dosyasına kaydet
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(tracks, f, ensure_ascii=False, indent=4)

        return {'message': 'JSON dosyası güncellendi!', 'tracks': tracks}

    except yt_dlp.utils.DownloadError as e:
        return {'error': 'YouTube engelledi mi?', 'details': str(e)}
    
    except Exception as e:
        return {'error': 'Bilinmeyen hata!', 'details': str(e)}

# Flask API'si, JSON dosyasını okur
@app.route('/top100', methods=['GET'])
def top100():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify({'tracks': data})
    except FileNotFoundError:
        return jsonify({'error': 'JSON dosyası bulunamadı!'}), 404

# 3 günde bir çalıştıran zamanlayıcı fonksiyonu
def schedule_updates():
    while True:
        get_top100()
        print("JSON dosyası güncellendi, 3 gün bekleniyor...")
        time.sleep(3 * 24 * 60 * 60)  # 3 gün (saniye cinsinden)

# Zamanlayıcıyı başlat
threading.Thread(target=schedule_updates, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
