import os
from flask import Flask, jsonify, request
from ytmusicapi import YTMusic

app = Flask(__name__)
ytmusic = YTMusic()

@app.route('/top100', methods=['GET'])
def get_top100():
    try:
        playlist = ytmusic.get_playlist("PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR")  # Buraya YouTube Music Top 100 ID'sini koy
        return jsonify(playlist)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/artist/<artist_name>', methods=['GET'])
def get_artist_songs(artist_name):
    try:
        search_results = ytmusic.search(artist_name, filter="songs")
        return jsonify(search_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/album/<album_id>', methods=['GET'])
def get_album(album_id):
    try:
        album_info = ytmusic.get_album(album_id)
        return jsonify(album_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render’ın verdiği portu al, yoksa 10000 kullan
    app.run(host='0.0.0.0', port=port)
