from flask import Flask, jsonify
import yt_dlp

app = Flask(__name__)

def get_top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,  # Tam veri çekmek için
        'format': 'bestaudio/best',
        'noplaylist': False,  # Oynatma listesini işle
        'force_generic_extractor': False,
        'cookiefile': 'cookies.txt',  # Çerezleri kullan (Render'da bu olmayabilir)
        'extractor-args': 'youtube:player_client=web',
        'sleep_interval': 5,
        'max_sleep_interval': 10
    }

    tracks = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

        if 'entries' in info:
            for entry in info['entries']:
                video_url = f"https://music.youtube.com/watch?v={entry.get('id', '')}"

                # Ses linkini al
                try:
                    with yt_dlp.YoutubeDL({'quiet': True, 'format': 'bestaudio'}) as audio_ydl:
                        audio_info = audio_ydl.extract_info(video_url, download=False)
                        audio_url = audio_info.get('url', 'Ses dosyası alınamadı')
                except Exception:
                    audio_url = "Ses dosyası alınamadı"

                tracks.append({
                    'title': entry.get('title', 'Bilinmeyen Şarkı'),
                    'artist': entry.get('uploader', 'Bilinmeyen Sanatçı'),
                    'audioUrl': audio_url  # Burada artık direkt stream URL var
                })

    return tracks

@app.route('/top100', methods=['GET'])
def top100():
    try:
        tracks = get_top100()
        return jsonify({'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
