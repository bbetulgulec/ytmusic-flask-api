from flask import Flask, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Cookie dosyasının yolu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_FILE = os.path.join(BASE_DIR, "cookies.txt")

@app.route("/")
def home():
    return "API Çalışıyor!"

@app.route("/top100", methods=["GET"])
def top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'extract_flat': False,
        'noplaylist': False,
        'force_generic_extractor': False,
        'sleep_interval': 3,
        'max_sleep_interval': 7,
        'cookiefile': COOKIE_FILE,  # Cookie dosyasını kullan
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
                audio_url = entry.get('url', '')

                tracks.append({
                    'title': title,
                    'artist': artist,
                    'audioUrl': audio_url
                })

        return jsonify({'tracks': tracks})

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"Download Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Bilinmeyen Hata: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)