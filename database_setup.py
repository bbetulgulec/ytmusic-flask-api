import sqlite3

def create_database():
    conn = sqlite3.connect("top100.db")  # Veritabanını oluştur veya bağlan
    cursor = conn.cursor()

    # tracks tablosunu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT NOT NULL,
        audio_url TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Veritabanı oluşturuldu ve 'tracks' tablosu hazır!")

# Çalıştır
create_database()
