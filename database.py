import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('manicure.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            service TEXT,
            datetime TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            file_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_booking(user_id, username, service, dt):
    conn = sqlite3.connect('manicure.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (user_id, username, service, datetime, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, service, dt, datetime.now().isoformat()))
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()
    return booking_id

def get_pending_bookings():
    conn = sqlite3.connect('manicure.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE status = 'pending'")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_booking_status(booking_id, status):
    conn = sqlite3.connect('manicure.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
    conn.commit()
    conn.close()

def add_photo(service, file_id):
    conn = sqlite3.connect('manicure.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO photos (service, file_id) VALUES (?, ?)", (service, file_id))
    conn.commit()
    conn.close()

def get_photos(service):
    conn = sqlite3.connect('manicure.db')
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM photos WHERE service = ?", (service,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
