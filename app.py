from flask import Flask, jsonify
from ytmusicapi import YTMusic

app = Flask(__name__)
ytmusic = YTMusic()

@app.route('/top100', methods=['GET'])
def get_top100():
    playlist = ytmusic.get_playlist("PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR")  # Buraya YouTube Music Top 100 playlist ID'sini koy
    return jsonify(playlist)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
