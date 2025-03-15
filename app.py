from flask import Flask, jsonify
import yt_dlp

app = Flask(__name__)

def get_top100():
    # YouTube Music Top 100 URL (örnek olarak popüler bir liste alınabilir)
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Sadece bağlantıları almak için
        'force_generic_extractor': True  # Ayrıntılı bilgi çekmek için
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
    
    tracks = []
    if 'entries' in info:
        for entry in info['entries']:
            tracks.append({
                'title': entry.get('title', 'Bilinmeyen Şarkı'),
                'artist': entry.get('uploader', 'Bilinmeyen Sanatçı'),
                'streamUrl': f"https://music.youtube.com/watch?v={entry.get('id', '')}"
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
