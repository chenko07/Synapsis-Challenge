import sqlite3

conn = sqlite3.connect('presensi.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS karyawan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    nik TEXT NOT NULL,
    departemen TEXT NOT NULL,
    foto TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS jadwal_kerja (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    hari TEXT NOT NULL,
    shift TEXT NOT NULL,  -- Tambahkan kolom shift di sini
    jam_masuk TEXT NOT NULL,
    jam_keluar TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS kelelahan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    tanggal TEXT NOT NULL,s
    tingkat_kelelahan TEXT NOT NULL
)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS presensi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        shift TEXT,
        waktu TEXT,
        keterangan TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sequences (
        departemen TEXT PRIMARY KEY,
        sequence INTEGER
    )
''')
conn.commit()
conn.close()
