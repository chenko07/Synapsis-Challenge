import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import os
import sqlite3
import numpy as np
from datetime import datetime
import threading
import subprocess

camera = None

def presensi(panel, combo_nama, combo_shift):
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

def simpan_foto(nama, combo_shift, presensi_karyawan_window):
    if camera:
        ret, frame = camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            folder_path = 'aset'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            waktu_presensi = datetime.now().strftime('%Y%m%d%H%M%S')
            nama_file = os.path.join(folder_path, f"IMG_{nama}_{waktu_presensi}.jpg")
            img.save(nama_file)
            update_presensi_database(nama, combo_shift.get())
            presensi_karyawan_window.destroy()
            messagebox.showinfo("Sukses", f"Presensi {nama} berhasil disimpan")
            tampilkan_hasil_presensi()
        else:
            messagebox.showerror("Error", "Gagal mengambil gambar.")

def load_known_faces():
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nama, foto FROM karyawan")
    data = cursor.fetchall()
    conn.close()
    known_faces = {}
    for nama, foto_path in data:
        known_faces[nama] = cv2.imread(foto_path, cv2.IMREAD_GRAYSCALE)
    return known_faces

def recognize_faces(frame, known_faces):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        face_region = gray_frame[y:y+h, x:x+w]
        recognized_name = "Unknown"
        
        lbp_face = cv2.LBPHFaceRecognizer_create()
        lbp_face.train(list(known_faces.values()), np.array([i for i in range(len(known_faces))]))
        label, confidence = lbp_face.predict(face_region)
        if confidence < 50:  # Sesuaikan threshold kecocokan
            recognized_name = list(known_faces.keys())[label]
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, recognized_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    return frame

def update_presensi_database(name, shift):
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    waktu_presensi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO presensi (nama, shift, waktu, keterangan)
        VALUES (?, ?, ?, ?)
    ''', (name, shift, waktu_presensi, 'HADIR'))
    conn.commit()
    conn.close()

def tampilkan_hasil_presensi():
    subprocess.Popen(['python', 'hasil_presensi.py'])

def presensi_karyawan():
    presensi_karyawan_window = tk.Toplevel(root)
    presensi_karyawan_window.title("Presensi Karyawan")
    
    tk.Label(presensi_karyawan_window, text="Nama:").pack()
    nama_karyawan_options = tampilkan_nama_karyawan()
    combo_nama = ttk.Combobox(presensi_karyawan_window, values=nama_karyawan_options)
    combo_nama.pack()
    
    tk.Label(presensi_karyawan_window, text="Shift:").pack()
    combo_shift = ttk.Combobox(presensi_karyawan_window, values=["pagi", "siang", "malam"])
    combo_shift.pack()
    
    panel = tk.Label(presensi_karyawan_window)
    panel.pack()
    
    tk.Button(presensi_karyawan_window, text="Presensi", command=lambda: simpan_foto(combo_nama.get(), combo_shift, presensi_karyawan_window)).pack()
    
    presensi(panel, combo_nama, combo_shift)

def tampilkan_nama_karyawan():
    conn = sqlite3.connect('presensi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nama FROM karyawan ORDER BY id")
    data = cursor.fetchall()
    conn.close()
    return [row[0] for row in data
]

def presensi_karyawan():
    def simpan_presensi_ke_database():
        nama = combo_nama.get()
        simpan_foto(nama, combo_shift, presensi_karyawan_window) 
    
    def start_presensi():
        presensi_thread = threading.Thread(target=simpan_presensi_ke_database)
        presensi_thread.start()
    
    presensi_karyawan_window = tk.Toplevel(root)
    presensi_karyawan_window.title("Presensi Karyawan")
    
    tk.Label(presensi_karyawan_window, text="Nama:").pack()
    nama_karyawan_options = tampilkan_nama_karyawan()
    combo_nama = ttk.Combobox(presensi_karyawan_window, values=nama_karyawan_options)
    combo_nama.pack()
    
    tk.Label(presensi_karyawan_window, text="Shift:").pack()
    combo_shift = ttk.Combobox(presensi_karyawan_window, values=["pagi", "siang", "malam"])
    combo_shift.pack()
    
    panel = tk.Label(presensi_karyawan_window)
    panel.pack()
    
    tk.Button(presensi_karyawan_window, text="Presensi", command=start_presensi).pack()
    
    presensi(panel, combo_nama, combo_shift)  # Menambahkan combo_shift

root = tk.Tk()
root.title("Aplikasi Presensi")
root.geometry("640x480")  

tombol_presensi = tk.Button(root, text="Presensi Karyawan", command=presensi_karyawan)
tombol_presensi.pack()

root.mainloop()