import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def tampilkan_data_karyawan():
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM karyawan ORDER BY id")
    data = cursor.fetchall()
    
    conn.close()
    
    return data

def urutkan_id():
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM karyawan ORDER BY id")
    data = cursor.fetchall()
    
    for i, row in enumerate(data):
        new_id = i + 1
        cursor.execute("UPDATE karyawan SET id = ? WHERE id = ?", (new_id, row[0]))
    
    conn.commit()
    conn.close()

def hapus_karyawan(id_karyawan):
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM karyawan WHERE id = ?", (id_karyawan,))
    conn.commit()
    
    urutkan_id()  # Memanggil fungsi untuk mengurutkan ID kembali
    conn.close()
    
    messagebox.showinfo("Sukses", "Data karyawan berhasil dihapus dan ID diperbarui")
    perbarui_tampilan()

def edit_karyawan(id_karyawan, nama, nik, departemen, foto):
    def simpan_perubahan():
        nama_baru = entry_nama.get()
        nik_baru = entry_nik.get()
        departemen_baru = entry_departemen.get()
        foto_baru = entry_foto.get()

        conn = sqlite3.connect('presensi.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE karyawan
            SET nama = ?, nik = ?, departemen = ?, foto = ?
            WHERE id = ?
        ''', (nama_baru, nik_baru, departemen_baru, foto_baru, id_karyawan))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sukses", "Data karyawan berhasil diperbarui")
        edit_window.destroy()
        perbarui_tampilan()
    
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Karyawan")
    
    tk.Label(edit_window, text="Nama:").pack()
    entry_nama = tk.Entry(edit_window)
    entry_nama.pack()
    entry_nama.insert(0, nama)
    
    tk.Label(edit_window, text="NIK:").pack()
    entry_nik = tk.Entry(edit_window)
    entry_nik.pack()
    entry_nik.insert(0, nik)
    
    tk.Label(edit_window, text="Departemen:").pack()
    entry_departemen = tk.Entry(edit_window)
    entry_departemen.pack()
    entry_departemen.insert(0, departemen)
    
    tk.Label(edit_window, text="Foto:").pack()
    entry_foto = tk.Entry(edit_window)
    entry_foto.pack()
    entry_foto.insert(0, foto)
    
    tk.Button(edit_window, text="Simpan Perubahan", command=simpan_perubahan).pack()

def perbarui_tampilan():
    for item in tree.get_children():
        tree.delete(item)
    
    data_karyawan = tampilkan_data_karyawan()
    for item in data_karyawan:
        tree.insert("", "end", values=item + ("Edit", "Delete"))

def on_tree_click(event):
    region = tree.identify_region(event.x, event.y)
    if region == "cell":
        column = tree.identify_column(event.x)
        item = tree.identify_row(event.y)
        
        if column == "#6":  # Edit column
            selected_item = tree.item(item)['values']
            id_karyawan = selected_item[0]
            nama = selected_item[1]
            nik = selected_item[2]
            departemen = selected_item[3]
            foto = selected_item[4]
            edit_karyawan(id_karyawan, nama, nik, departemen, foto)
        elif column == "#7":  # Delete column
            id_karyawan = tree.item(item)['values'][0]
            hapus_karyawan(id_karyawan)

root = tk.Tk()
root.title("Data Karyawan")

columns = ("id", "nama", "nik", "departemen", "foto", "edit", "delete")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, stretch=tk.YES, anchor="center")

data_karyawan = tampilkan_data_karyawan()
for item in data_karyawan:
    tree.insert("", "end", values=item + ("Edit", "Delete"))

tree.bind("<ButtonRelease-1>", on_tree_click)
tree.pack(expand=True, fill='both')

perbarui_tampilan()
root.mainloop()