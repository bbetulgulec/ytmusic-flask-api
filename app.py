import os

# Ortam değişkeninden cookies bilgisini al
COOKIES = os.getenv("COOKIES")

ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'force_generic_extractor': True,
    'sleep_interval': 5,
    'max_sleep_interval': 20,
    'proxy': PROXY_URL,
    'cookiefile': '-'  # Standart cookies dosyası yerine stdin kullan
}

def get_top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"
    
    # Eğer cookies ortam değişkeni varsa, bunu kullanarak yt-dlp'ye ver
    if COOKIES:
        ydl_opts['cookiesfromstring'] = COOKIES

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    tracks = []
    if 'entries' in info:
        for entry in info['entries']:
            title = entry.get('title', 'Bilinmeyen Şarkı')
            artist = entry.get('uploader', 'Bilinmeyen Sanatçı')
            audio_url = f"https://music.youtube.com/watch?v={entry.get('id', '')}"

            tracks.append({
                'title': title,
                'artist': artist,
                'audioUrl': audio_url
            })

    return tracks
