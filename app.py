import yt_dlp
import json
import time

def get_top100():
    playlist_url = "https://music.youtube.com/playlist?list=PL4fGSI1pDJn5tdVDtIAZArERm_vv4uFCR"

    ydl_opts = {
        'quiet': False,
        'format': 'bestaudio/best',
        'extract_flat': False,
        'noplaylist': False,
        'force_generic_extractor': False,
        'sleep_interval': 3,
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

        # JSON olarak kaydet
        with open("top100.json", "w", encoding="utf-8") as json_file:
            json.dump({'tracks': tracks}, json_file, indent=4, ensure_ascii=False)

        print("Top 100 JSON dosyası güncellendi.")

    except yt_dlp.utils.DownloadError as e:
        print(f"Download Error: {e}")

    except Exception as e:
        print(f"Bilinmeyen Hata: {e}")

if __name__ == "__main__":
    get_top100()
