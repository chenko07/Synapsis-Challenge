import tkinter as tk
from tkinter import ttk
import sqlite3

def tampilkan_data_kelelahan():
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM kelelahan")
    data = cursor.fetchall()
    
    conn.close()
    
    return data

root = tk.Tk()
root.title("Data Kelelahan")

columns = ("id", "nama", "tanggal", "tingkat_kelelahan")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

data_kelelahan = tampilkan_data_kelelahan()
for item in data_kelelahan:
    tree.insert("", "end", values=item)

tree.pack(expand=True, fill='both')
root.mainloop()
