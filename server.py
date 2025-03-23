from flask import Flask, jsonify
import os
import sqlite3
import yt_dlp
import shutil

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "SongData.db")
TOP100_DIR = os.path.join(BASE_DIR, "top100")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")


def log_message(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")


def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            audio_data BLOB NOT NULL,
            thumbnail_url TEXT
        )
    ''')
    conn.commit()
    conn.close()


def download_and_save_songs():
    playlist_url = "https://www.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': os.path.join(TOP100_DIR, '%(title)s - %(uploader)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    song_list = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=True)
        for entry in playlist_info['entries']:
            title = entry.get("title", "Unknown")
            artist = entry.get("uploader", "Unknown")
            thumbnails = entry.get("thumbnails", [])
            thumbnail_url = thumbnails[-1]["url"] if thumbnails else ""
            file_name = f"{title} - {artist}.mp3"
            file_path = os.path.join(TOP100_DIR, file_name)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    audio_data = f.read()
                song_list.append((title, artist, audio_data, thumbnail_url))
    except Exception as e:
        log_message(f"Hata: {str(e)}")
    return song_list

def clear_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        log_message("Mevcut veritabanı silindi.")
    create_database()


def save_to_db(song_list):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for title, artist, audio_data, thumbnail_url in song_list:
        cursor.execute('''
            INSERT INTO songs (title, artist, audio_data, thumbnail_url)
            VALUES (?, ?, ?, ?)
        ''', (title, artist, sqlite3.Binary(audio_data), thumbnail_url))
    conn.commit()
    conn.close()


@app.route("/download_songs", methods=["GET"])
def download_songs():
    log_message("Yeni indirme işlemi başlatıldı.")

    # Veritabanını temizle
    clear_database()

    # Klasörü temizle
    if os.path.exists(TOP100_DIR):
        shutil.rmtree(TOP100_DIR)
    os.makedirs(TOP100_DIR, exist_ok=True)

    songs = download_and_save_songs()
    save_to_db(songs)

    return jsonify({"status": "OK", "message": f"{len(songs)} şarkı indirildi ve kaydedildi."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
