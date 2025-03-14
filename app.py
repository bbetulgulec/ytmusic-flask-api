from flask import Flask, jsonify
from ytmusicapi import YTMusic

app = Flask(__name__)
ytmusic = YTMusic()

@app.route('/top100', methods=['GET'])
def get_top100():
    try:
        playlist = ytmusic.get_playlist("PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR")
        tracks = []

        for track in playlist["tracks"]:
            track_info = {
                "title": track["title"],
                "artist": track["artists"][0]["name"] if track["artists"] else "Unknown",
                "videoId": track["videoId"],
                "streamUrl": f"https://music.youtube.com/watch?v={track['videoId']}"  # Şarkı linki
            }
            tracks.append(track_info)

        return jsonify({"tracks": tracks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
