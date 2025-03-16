from flask import Flask, jsonify
import yt_dlp

app = Flask(__name__)

def get_top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'cookies': 'C:/Users/gulec/Desktop/ytmusic-flask-api/cookies.txt'  
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
    
    tracks = []
    if 'entries' in info:
        for entry in info['entries']:
            video_url = f"https://music.youtube.com/watch?v={entry.get('id', '')}"
            
            # Doğrudan oynatılabilir URL'yi çekme
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'cookies': 'path/to/your/cookies.txt'}) as ydl:
                    direct_info = ydl.extract_info(video_url, download=False)
                    stream_url = direct_info.get('url', '')
            except Exception:
                stream_url = "Hata: URL alınamadı"
            
            tracks.append({
                'title': entry.get('title', 'Bilinmeyen Şarkı'),
                'artist': entry.get('uploader', 'Bilinmeyen Sanatçı'),
                'streamUrl': stream_url  # Güncellenmiş doğrudan oynatma URL'si
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
    app.run(debug=True)
