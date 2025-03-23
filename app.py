from flask import Flask, jsonify, send_file
import sqlite3

app = Flask(__name__)

DB_FILE = "C:/Users/gulec/Desktop/ytmusic-flask-api/SongData.db"
TOP100_DIR = "C:/Users/gulec/Desktop/ytmusic-flask-api/top100"

def get_songs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, artist, file_path, thumbnail_url FROM songs")
    songs = [{"id": row[0], "title": row[1], "artist": row[2], "file_path": row[3], "thumbnail_url": row[4]} for row in cursor.fetchall()]
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
        return send_file(song[0], mimetype="audio/mpeg")
    return jsonify({"error": "Şarkı bulunamadı"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
