from flask import Flask, jsonify
import yt_dlp

app = Flask(__name__)

# Önceden belirlenmiş linkler (senin verdiğin sahte linkler)
custom_links = {
    "Şarkı 1": "https://rr2---sn-u0g3uxax3-xncz.googlevideo.com/videoplayback?expire=1742137974&ei=FpbWZ6DXKNj-xN8PiKPw2A8&itag=251",
    "Şarkı 2": "https://rr2---sn-u0g3uxax3-xncz.googlevideo.com/videoplayback?expire=1742137979&ei=G5bWZ9aRCa3yi9oP8Le1-QE&itag=251"
}

def get_top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'sleep_interval': 5,
        'max_sleep_interval': 20
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    tracks = []
    if 'entries' in info:
        for entry in info['entries']:
            title = entry.get('title', 'Bilinmeyen Şarkı')
            artist = entry.get('uploader', 'Bilinmeyen Sanatçı')

            # Eğer özel URL varsa, onu kullan; yoksa YouTube Music linkini ekle
            if title in custom_links:
                audio_url = custom_links[title]
            else:
                audio_url = f"https://music.youtube.com/watch?v={entry.get('id', '')}"

            tracks.append({
                'title': title,
                'artist': artist,
                'audioUrl': audio_url
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
