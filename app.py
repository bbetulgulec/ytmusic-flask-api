import yt_dlp
from flask import Flask, jsonify

app = Flask(__name__)

def get_top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"

    ydl_opts = {
        'quiet': False,
        'format': 'bestaudio/best',  # En iyi ses formatını seç
        'extract_flat': False,  # Doğrudan ses URL’sini almak için
        'noplaylist': False,  # Tüm playlist'i çekmek için
        'force_generic_extractor': False,  # YouTube Music'e özel extractor'ı kullansın
        'sleep_interval': 3,  # YouTube tarafından engellenmemek için bekleme süresi
        'max_sleep_interval': 7,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)

        tracks = []
        if 'entries' in playlist_info:
            for entry in playlist_info['entries']:
                if entry is None:
                    continue

                title = entry.get('title', 'Bilinmeyen Şarkı')
                artist = entry.get('uploader', 'Bilinmeyen Sanatçı')

                # Ses dosyasının direkt URL'sini al
                ydl_opts_audio = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
                    audio_info = ydl_audio.extract_info(entry['url'], download=False)
                
                audio_url = audio_info.get('url', '')

                tracks.append({
                    'title': title,
                    'artist': artist,
                    'audioUrl': audio_url
                })

        return {'tracks': tracks}

    except yt_dlp.utils.DownloadError as e:
        return {'error': 'YouTube engelledi mi?', 'details': str(e)}
    
    except Exception as e:
        return {'error': 'Bilinmeyen hata!', 'details': str(e)}

@app.route('/top100', methods=['GET'])
def top100():
    response = get_top100()
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
