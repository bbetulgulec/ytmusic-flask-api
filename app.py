import os
from flask import Flask, jsonify, request
from ytmusicapi import YTMusic

app = Flask(__name__)
ytmusic = YTMusic()

@app.route('/top100', methods=['GET'])
def get_top100():
    try:
        playlist = ytmusic.get_playlist("PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR")  # Türkiye Top 100 Playlist ID
        tracks = [
            {
                "title": track["title"],
                "artist": track["artists"][0]["name"] if track.get("artists") else "Unknown",
                "album": track["album"]["name"] if track.get("album") else "Unknown",
                "duration": track["duration"],
                "videoId": track["videoId"],
                "url": f"https://music.youtube.com/watch?v={track['videoId']}"
            }
            for track in playlist.get("tracks", [])
        ]
        return jsonify({"playlist": playlist["title"], "tracks": tracks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render’ın verdiği portu al, yoksa 10000 kullan
    app.run(host='0.0.0.0', port=port)
