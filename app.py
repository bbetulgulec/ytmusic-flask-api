import os
import time
from flask import Flask, jsonify, send_from_directory
from ytmusicapi import YTMusic
import yt_dlp

app = Flask(__name__)
ytmusic = YTMusic()

# 📌 MP3 dosyalarını saklayacak klasör (Render içinde)
music_folder = "/tmp/music"
os.makedirs(music_folder, exist_ok=True)

# 📌 Playlist ID
playlist_id = "PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"

def download_song(video_id, title):
    """YouTube Music'ten MP3 indirir ve sunucuda saklar."""
    url = f"https://music.youtube.com/watch?v={video_id}"
    file_path = os.path.join(music_folder, f"{title}.mp3")

    if os.path.exists(file_path):
        print(f"⏩ {title} zaten indirildi, atlanıyor.")
        return file_path

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "extract_audio": True,
        "audio_format": "mp3",
        "outtmpl": file_path,
        "noplaylist": True,
        "cookies": "cookies.txt" if os.path.exists("cookies.txt") else None,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✅ İndirildi: {title}")
        return file_path
    except Exception as e:
        print(f"❌ {title} indirilemedi: {str(e)}")
        return None

@app.route('/top100', methods=['GET'])
def get_top100():
    """Şarkıları indirir ve indirilebilir linkleri döndürür."""
    try:
        playlist = ytmusic.get_playlist(playlist_id)
        all_songs = playlist.get("tracks", [])
        downloads = []

        for song in all_songs:
            title = song["title"]
            video_id = song["videoId"]
            file_path = download_song(video_id, title)

            if file_path:
                downloads.append({
                    "title": title,
                    "download_url": f"/download/{title}.mp3"
                })

            time.sleep(10)  # YouTube engellemesin diye bekleme süresi

        return jsonify({"downloads": downloads})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """İndirilebilir MP3 dosyası linki döndürür."""
    return send_from_directory(music_folder, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
