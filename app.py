from flask import Flask, jsonify, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)
UPLOAD_FOLDER = "downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def download_mp3(video_url):
    """YouTube Music videosunu MP3 olarak indirir."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{UPLOAD_FOLDER}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_name = f"{info['title']}.mp3"
        return file_name

@app.route('/download', methods=['POST'])
def download():
    """Belirtilen şarkıyı indirir ve URL döndürür."""
    data = request.json
    if not data or "url" not in data:
        return jsonify({"error": "Lütfen geçerli bir URL sağlayın."}), 400
    
    try:
        file_name = download_mp3(data["url"])
        file_url = f"https://your-render-app.onrender.com/files/{file_name}"
        return jsonify({"message": "İndirme tamamlandı!", "file_url": file_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/<filename>', methods=['GET'])
def serve_file(filename):
    """İndirilen MP3 dosyalarını sunar."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == '__main__':
    app.run(debug=True)
