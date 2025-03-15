from flask import Flask, jsonify
from ytmusicapi import YTMusic
import yt_dlp

app = Flask(__name__)
ytmusic = YTMusic()

def get_audio_url(video_id):
    """YouTube Music'ten video ID'sine göre MP3 URL'si alır."""
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'extract_flat': False,
        'cookies': 'cookies.txt'  # Çerezleri ekle
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://music.youtube.com/watch?v={video_id}", download=False)
        for fmt in info['formats']:
            if 'audio' in fmt['format'] and fmt.get('url'):
                return fmt['url']
    return None


@app.route('/top100', methods=['GET'])
def get_top100():
    try:
        playlist = ytmusic.get_playlist("PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR")  # Çalma listesi ID
        tracks = []

        for track in playlist["tracks"]:
            video_id = track.get("videoId")
            audio_url = get_audio_url(video_id) if video_id else None

            track_info = {
                "title": track["title"],
                "artist": track["artists"][0]["name"] if track["artists"] else "Unknown",
                "videoId": video_id,
                "streamUrl": audio_url if audio_url else f"https://music.youtube.com/watch?v={video_id}"
            }
            tracks.append(track_info)

        return jsonify({"tracks": tracks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
