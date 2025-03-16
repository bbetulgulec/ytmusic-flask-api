import os
import yt_dlp
from flask import Flask, jsonify

app = Flask(__name__)

# Render ortamında değişkenleri kontrol edelim
PROXY_URL = os.getenv("PROXY_URL", None)  # Proxy varsa kullan, yoksa None
COOKIES = os.getenv("COOKIES", None)  # Cookies varsa kullan, yoksa None

def get_top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"
    
    ydl_opts = {
        'quiet': False,
        'extract_flat': True,
        'force_generic_extractor': True,
        'sleep_interval': 5,
        'max_sleep_interval': 20,
    }

    # Proxy varsa ekleyelim
    if PROXY_URL:
        ydl_opts['proxy'] = PROXY_URL

    # Cookies varsa ekleyelim
    if COOKIES:
        ydl_opts['cookiefile'] = '-'
        ydl_opts['cookiesfromstring'] = COOKIES

    try:
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
        
        return {'tracks': tracks}

    except yt_dlp.utils.DownloadError as e:
        return {'error': 'YouTube engelledi mi?', 'details': str(e)}
    
    except Exception as e:
        return {'error': 'Bilinmeyen hata!', 'details': str(e)}

@app.route('/top100', methods=['GET'])
def top100():
    response = get_top100()
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
