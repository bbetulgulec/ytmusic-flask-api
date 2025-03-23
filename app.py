from flask import Flask, jsonify, send_file, request
import sqlite3
import os

app = Flask(__name__)

# Temel yol tanımlamaları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "SongData.db")
SONGS_DIR = os.path.join(BASE_DIR, "songs")  # Şarkı dosyalarının bulunduğu klasör

# Şarkı listesini çeken fonksiyon
def get_songs():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, artist, file_path, thumbnail_url FROM songs")
        songs = [
            {
                "id": row[0],
                "title": row[1],
                "artist": row[2],
                "file_path": f"/play/{row[0]}",  # Dinamik URL
                "thumbnail_url": row[4]
            }
            for row in cursor.fetchall()
        ]
        conn.close()
        return songs
    except sqlite3.Error as e:
        return {"error": f"Veritabanı hatası: {str(e)}"}

# Şarkı listesini döndüren route
@app.route("/songs", methods=["GET"])
def songs():
    song_data = get_songs()
    if isinstance(song_data, dict) and "error" in song_data:
        return jsonify(song_data), 500
    return jsonify(song_data)

# Şarkıyı çalan route
@app.route("/play/<int:song_id>", methods=["GET"])
def play_song(song_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT file_path FROM songs WHERE id = ?", (song_id,))
        song = cursor.fetchone()
        conn.close()

        if song:
            # Dosya yolunu tam path'e çevir
            song_path = os.path.join(SONGS_DIR, os.path.basename(song[0]))
            if os.path.exists(song_path):
                return send_file(song_path, mimetype="audio/mpeg", as_attachment=False)
            return jsonify({"error": "Şarkı dosyası sunucuda bulunamadı"}), 404
        return jsonify({"error": "Şarkı veritabanında bulunamadı"}), 404
    except sqlite3.Error as e:
        return jsonify({"error": f"Veritabanı hatası: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Beklenmeyen hata: {str(e)}"}), 500

# Uygulamayı başlat
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render için port
    app.run(debug=False, host="0.0.0.0", port=port)