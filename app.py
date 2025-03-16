import os
import json
import time
import yt_dlp
from flask import Flask, jsonify

app = Flask(__name__)

# JSON dosya yolu
TOP100_JSON = "top100.json"
UPDATE_INTERVAL = 3 * 24 * 60 * 60  # 3 gün (saniye cinsinden)

# YouTube Music Top 100 Playlist URL
PLAYLIST_URL = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"

def needs_update():
    """JSON dosyasının güncellenmesi gerekip gerekmediğini kontrol eder."""
    if not os.path.exists(TOP100_JSON):
        return True
    last_updated = os.path.getmtime(TOP100_JSON)
    return (time.time() - last_updated) > UPDATE_INTERVAL

def get_audio_url(video_id):
    """Verilen video ID'sinden doğrudan ses dosyası URL'sini çeker."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://music.youtube.com/watch?v={video_id}", download=False)
        return info.get('url', '')

def update_top100():
    """YouTube Music Top 100 listesini günceller ve JSON dosyasına kaydeder."""
    ydl_opts = {
        'quiet': False,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(PLAYLIST_URL, download=False)
    
    tracks = []
    if 'entries' in info:
        for entry in info['entries']:
            video_id = entry.get('id', '')
            audio_url = get_audio_url(video_id) if video_id else ''

            tracks.append({
                'title': entry.get('title', 'Bilinmeyen Şarkı'),
                'artist': entry.get('uploader', 'Bilinmeyen Sanatçı'),
                'audioUrl': audio_url
            })
    
    with open(TOP100_JSON, 'w', encoding='utf-8') as f:
        json.dump({'tracks': tracks}, f, ensure_ascii=False, indent=2)

@app.route('/top100', methods=['GET'])
def top100():
    """JSON dosyasından Top 100 listesini döndürür."""
    if needs_update():
        update_top100()

    with open(TOP100_JSON, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
