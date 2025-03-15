from flask import Flask, jsonify, request
from ytmusicapi import YTMusic
import yt_dlp
import os

app = Flask(__name__)

# YouTube Music API'yi başlat
ytmusic = YTMusic("headers_auth.json")

# Çerez dosyasını kullanarak doğrulama
cookies_path = "cookies.txt"  # cookies.txt dosyanızın yolu

# MP3 olarak şarkı indirme fonksiyonu
def download_song(video_id, title):
    url = f"https://music.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "extract_audio": True,
        "audio_format": "mp3",
        "outtmpl": os.path.join("downloads", f"{title}.mp3"),
        "cookies": cookies_path,  # Çerez kullanarak giriş yap
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"✅ İndirildi: {title}"
    except Exception as e:
        return f"❌ {title} indirilemedi: {str(e)}"

@app.route('/download', methods=['GET'])
def download_playlist():
    playlist_id = request.args.get('playlist_id', default="PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR")  # Varsayılan Playlist ID
    try:
        playlist = ytmusic.get_playlist(playlist_id)
        tracks = []
        
        for track in playlist["tracks"]:
            video_id = track.get("videoId")
            title = track["title"]
            status = download_song(video_id, title)
            tracks.append({
                "title": title,
                "status": status
            })

        return jsonify({"tracks": tracks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
