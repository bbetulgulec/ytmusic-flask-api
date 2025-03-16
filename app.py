import time
import random
from flask import Flask, jsonify
import yt_dlp

app = Flask(__name__)

# Çerez dosyasının yolu
COOKIES_FILE = "cookies.txt"

def get_audio_url(video_id):
    """YouTube Music'ten doğrudan ses URL'sini alır."""
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio',
        'extractor_args': {'youtube': {'po_token': 'web_music.gvs+XXX'}},  # PO Token Kullan
        'cookies': COOKIES_FILE  # Çerezleri Kullan
    }

    # Her istekte rastgele 3-10 saniye bekle
    delay = random.randint(3, 10)
    time.sleep(delay)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"https://music.youtube.com/watch?v={video_id}", download=False)
            if 'url' in info:
                return info['url']
            else:
                return None
        except yt_dlp.utils.DownloadError as e:
            # Eğer 403 hatası alırsak, engellenmiş olabiliriz
            if "HTTP Error 403" in str(e):
                return "BLOCKED"
            return None

@app.route('/track/<video_id>', methods=['GET'])
def track(video_id):
    """Belirli bir video için ses URL'sini döndüren API."""
    try:
        audio_url = get_audio_url(video_id)

        if audio_url == "BLOCKED":
            return jsonify({"error": "YouTube Music tarafından engellenmiş olabilirsin. Birkaç saat bekleyip tekrar dene."}), 403

        if audio_url:
            return jsonify({"audioUrl": audio_url})

        return jsonify({"error": "Ses dosyası bulunamadı"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
