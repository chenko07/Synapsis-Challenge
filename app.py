import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import sqlite3
import subprocess
import os
import datetime

camera = None

def presensi(panel):
    global camera
    camera = cv2.VideoCapture(0)
    
    def pembaruan():
        ret, frame = camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            panel.configure(image=img)
            panel.image = img
            panel.after(10, pembaruan)
    
    pembaruan()

def tangkap_gambar(nama):
    if camera:
        ret, frame = camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            folder_path = 'aset'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            nama_file = os.path.join(folder_path, f"IMG_{nama}.jpg")
            img.save(nama_file)
            return nama_file
        else:
            messagebox.showerror("Error", "Gagal mengambil gambar.")
            return None

def buka_presensi():
    subprocess.Popen(['python', 'presensi.py'])
    
def buka_file_tampilan_data_karyawan():
    subprocess.Popen(['python', 'tampilan_database.py'])

def buka_file_tampilan_data_jadwal_kerja():
    subprocess.Popen(['python', 'tampilan_database_jadwal_kerja.py'])

def buka_file_tampilan_data_kelelahan():
    subprocess.Popen(['python', 'tampilan_database_kelelahan.py'])
    
def tampilkan_hasil_presensi():
    subprocess.Popen(['python', 'hasil_presensi.py']) 

conn = sqlite3.connect('presensi.db')
cursor = conn.cursor()

def generate_id(departemen):
    def get_latest_sequence(departemen):
        cursor.execute("SELECT sequence FROM sequences WHERE departemen = ?", (departemen,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0 
    def update_sequence(departemen, sequence):
        cursor.execute("REPLACE INTO sequences (departemen, sequence) VALUES (?, ?)", (departemen, sequence))
        conn.commit()

    divisi_mapping = {
        "IT": "02",
        "Pekerja Konstruksi": "04",
        "Mandor": "03",
        "HR": "01",
        "Environment": "05",
        "Visitor": "07",
        "Intern": "06"
    }

    nomor_divisi = divisi_mapping.get(departemen, "")
    tahun_masuk = datetime.datetime.now().year
    nomor_urutan = get_latest_sequence(departemen) + 1
    new_id = f"{tahun_masuk}{nomor_divisi}{nomor_urutan:02}"
    update_sequence(departemen, nomor_urutan)
    return new_id
    
def tambah_karyawan():
    def simpan_ke_database():
        nama = entry_nama.get()
        nik = entry_nik.get()
        departemen = combo_departemen.get()
        foto = tangkap_gambar(nama)
        
        if not foto:
            return

        new_id = generate_id(departemen)
        conn = sqlite3.connect('presensi.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO karyawan (id, nama, nik, departemen, foto)
            VALUES (?, ?, ?, ?, ?)
        ''', (new_id, nama, nik, departemen, foto))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sukses", "Data karyawan berhasil disimpan")
        tambah_karyawan_window.destroy()
    
    tambah_karyawan_window = tk.Toplevel(root)
    tambah_karyawan_window.title("Tambah Karyawan")
    
    tk.Label(tambah_karyawan_window, text="Nama:").pack()
    entry_nama = tk.Entry(tambah_karyawan_window)
    entry_nama.pack()
    
    tk.Label(tambah_karyawan_window, text="NIK:").pack()
    entry_nik = tk.Entry(tambah_karyawan_window)
    entry_nik.pack()
    
    tk.Label(tambah_karyawan_window, text="Departemen:").pack()

    departemen_options = ["IT", "Pekerja Konstruksi", "Mandor", "HR", "Environment", "Visitor", "Intern"]
    combo_departemen = ttk.Combobox(tambah_karyawan_window, values=departemen_options)
    combo_departemen.pack()
    
    panel = tk.Label(tambah_karyawan_window)
    panel.pack()
    
    tk.Button(tambah_karyawan_window, text="Simpan", command=simpan_ke_database).pack()
    
    presensi(panel) 


#ROOT USER INTERFACE
root = tk.Tk()
root.title("Aplikasi Presensi")
root.geometry("640x480")  
root.configure(bg="white")

# Membuat frame untuk tata letak yang lebih rapi
frame = tk.Frame(root, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Membuat tombol-tombol dengan gaya tata letak situs web
tombol_presensi = tk.Button(frame, 
                            text="Presensi", 
                            command=buka_presensi, 
                            bg="lightgrey", 
                            fg="black", 
                            font=("Arial", 12), 
                            width=20)
tombol_presensi.grid(row=0, 
                     column=0, 
                     pady=5)

tombol_tambah_karyawan = tk.Button(frame, 
                                   text="Tambah Karyawan", 
                                   command=tambah_karyawan, 
                                   bg="lightgrey", 
                                   fg="black", 
                                   font=("Arial", 12), 
                                   width=20)
tombol_tambah_karyawan.grid(row=1, 
                            column=0, 
                            pady=5)

tombol_tampilkan_data = tk.Button(frame, 
                                  text="Tampilkan Data Karyawan", 
                                  command=buka_file_tampilan_data_karyawan, 
                                  bg="lightgrey", fg="black", 
                                  font=("Arial", 12), 
                                  width=20)
tombol_tampilkan_data.grid(row=2, 
                           column=0, 
                           pady=5)

tombol_tampilkan_data_jadwal = tk.Button(frame, 
                                         text="Tampilkan Data Jadwal Kerja", 
                                         command=buka_file_tampilan_data_jadwal_kerja, 
                                         bg="lightgrey", 
                                         fg="black", 
                                         font=("Arial", 12), 
                                         width=20)
tombol_tampilkan_data_jadwal.grid(row=3, 
                                  column=0, 
                                  pady=5)

tombol_tampilkan_data_kelelahan = tk.Button(frame, 
                                            text="Tampilkan Data Kelelahan", 
                                            command=buka_file_tampilan_data_kelelahan, 
                                            bg="lightgrey", 
                                            fg="black", 
                                            font=("Arial", 12), 
                                            width=20)
tombol_tampilkan_data_kelelahan.grid(row=4, 
                                     column=0, 
                                     pady=5)

tombol_tampilkan_hasil_presensi = tk.Button(frame, 
                                            text="Tampilkan Hasil Presensi", 
                                            command=tampilkan_hasil_presensi, 
                                            bg="lightgrey", 
                                            fg="black", 
                                            font=("Arial", 12), 
                                            width=20)
tombol_tampilkan_hasil_presensi.grid(row=5, 
                                     column=0, 
                                     pady=5)

root.mainloop()