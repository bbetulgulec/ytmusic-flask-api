from flask import Flask, jsonify
from ytmusicapi import YTMusic
import os

app = Flask(__name__)

# YTMusic kimlik doğrulaması (önceden oluşturulmuş headers_auth.json kullan)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUTH_FILE = os.path.join(BASE_DIR, "headers_auth.json")
ytmusic = YTMusic(AUTH_FILE)

@app.route("/")
def home():
    return "API Çalışıyor!"

@app.route("/top100", methods=["GET"])
def top100():
    try:
        playlist_id = "PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"
        playlist = ytmusic.get_playlist(playlist_id, limit=100)

        tracks = []
        for track in playlist['tracks']:
            title = track.get('title', 'Bilinmeyen Şarkı')
            artist = track['artists'][0]['name'] if track.get('artists') else 'Bilinmeyen Sanatçı'
            video_id = track.get('videoId', '')
            audio_url = f"https://music.youtube.com/watch?v={video_id}"  # Direkt oynatma URL’si değil, ama yt-dlp ile çekebiliriz

            tracks.append({
                'title': title,
                'artist': artist,
                'audioUrl': audio_url
            })

        return jsonify({'tracks': tracks})

    except Exception as e:
        return jsonify({"error": f"Hata: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)