import tkinter as tk
from tkinter import ttk
import sqlite3

def tampilkan_hasil_presensi():
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM presensi")
    data = cursor.fetchall()
    
    conn.close()
    
    return data

def perbarui_tampilan():
    for item in tree.get_children():
        tree.delete(item)
    
    data_presensi = tampilkan_hasil_presensi()
    for item in data_presensi:
        tree.insert("", "end", values=item)

root = tk.Tk()
root.title("Data Presensi")
root.configure(bg="white")

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="white",
                foreground="black",
                fieldbackground="white")

style.map("Treeview", 
          background=[('selected', 'lightgrey')],
          foreground=[('selected', 'black')])

columns = ("ID", "Nama", "Shift", "Waktu", "Keterangan")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, stretch=tk.YES, anchor="center")

style.configure("Treeview.Heading", font=("Arial", 12))

perbarui_tampilan()
tree.pack(expand=True, fill='both')

root.mainloop()