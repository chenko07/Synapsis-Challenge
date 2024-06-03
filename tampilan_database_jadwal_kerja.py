import tkinter as tk
from tkinter import ttk
import sqlite3

def tampilkan_data_jadwal_kerja():
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM jadwal_kerja")
    data = cursor.fetchall()
    
    conn.close()
    
    return data

root = tk.Tk()
root.title("Data Jadwal Kerja")

columns = ("id", "nama", "hari", "shift", "jam_masuk", "jam_keluar")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

data_jadwal = tampilkan_data_jadwal_kerja()
for item in data_jadwal:
    tree.insert("", "end", values=item)

tree.pack(expand=True, fill='both')
root.mainloop()
