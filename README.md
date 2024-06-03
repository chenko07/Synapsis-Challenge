# Synapsis-Challenge

1. Desain Database  (Done) 
Database menggunakan SQLite3 pada python sehingga tidak perlu menggunakan database eksternal. Database.py harus dijalankan terlebih dahulu untuk menjalankan programnya.
Database yang dibuat dengan generate ID = menggunakan kombinasi {TAHUN MASUK} + Divisi Mapping + Urutan ID

divisi_mapping = {
        "IT": "02",
        "Pekerja Konstruksi": "04",
        "Mandor": "03",
        "HR": "01",
        "Environment": "05",
        "Visitor": "07",
        "Intern": "06"
    }

Penyimpanan gambar yang diambil pada penambahan karyawan disimpan dengan format IMG + {nama} dan presensi disimpan dengan format IMG_{nama}_{waktu_presensi}
Pembuatan Jadwal_Kerja menggunakan generate (belum jadi diterapkan)
Ketika melakukan presensi maka langsung tampil hasil presensi (bisa digunakan oleh admin saja
Delete pada Karyawan mengalami bug, jadi akan reset ke ID 1 jika terdapat data yang dihapus.
Edit tidak mengalami kendala
Presensi mengalami kendala untuk melakukan fetching threshold untuk Face recognition, seharusnya ketika simpan presensi langsung capture dan analisa kemudian baru bisa save, ternyata terjadi crash TRESHOLDING dan menjadikan freeze. 

2. Pengumpulan Dataset (Done)
Pengumpulan dataset menggunakan Teachable Machine untuk mendapatkan framing yang diinginkan sehingga derajat tertentu lebih akurat

3. Face Recognition (Done) 
Menggunakan ResNet-15 dalam melakukan pelatihan model pada 4 kelas
Kendala yang dimiliki adalah integrasi ke Aplikasinya tidak bisa, karena build CMake dan dlib nya bermasalah padahal sudah dicoba menggunakan versi alternate dari anaconda dan sudah menggunakan homebrew untuk ARM based Mac.

4. Fatigue Analysis  (X)
Mengalami kendala berupa dataset yang kurang dipahami antara menggunakan gambar atau hanya prediksi dari jam kerja sehingga database kelelahan kerja belum bisa didapatkan

5. Integrasi Sistem (X)
Kendala Environtment sudah dicoba untuk library face_recognition dan openface, namun masih gagal dalam aktivasi hingga download model h5 nya. 

6. Deployment (X)
Proses environtmenya belum bisa
