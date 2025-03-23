from flask import Flask, jsonify, send_file, request
import sqlite3
import os

app = Flask(__name__)

# Render için uygun yol tanımlaması
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "SongData.db")
TOP100_DIR = os.path.join(BASE_DIR, "top100")

def get_songs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, artist, file_path, thumbnail_url FROM songs")
    songs = [
        {
            "id": row[0],
            "title": row[1],
            "artist": row[2],
            "file_path": f"/play/{row[0]}",  # Dinamik URL kullan
            "thumbnail_url": row[4]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return songs

@app.route("/songs", methods=["GET"])
def songs():
    return jsonify(get_songs())

@app.route("/play/<int:song_id>", methods=["GET"])
def play_song(song_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM songs WHERE id = ?", (song_id,))
    song = cursor.fetchone()
    conn.close()
    if song:
        return send_file(song[0], mimetype="audio/mpeg", as_attachment=False)
    return jsonify({"error": "Şarkı bulunamadı"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render için port değişkeni
    app.run(debug=False, host="0.0.0.0", port=port)
