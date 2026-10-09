# Belajar Socket & Web Server dari Nol

Repo ini catatan praktek saya belajar fundamental jaringan komputer pakai Python. Di sini saya nyoba bikin web server sendiri langsung pakai modul bawaan `socket`, tanpa pakai framework seperti Flask, FastAPI, atau Express.

Tujuannya murni buat paham apa yang sebenarnya terjadi di balik layar ketika browser ngirim request dan server ngembaliin data.

## Apa yang Dipelajari di Sini?

1. **TCP Socket Dasar**: Cara kerja `socket()`, `bind()`, `listen()`, `accept()`, `recv()`, dan `sendall()`.
2. **Parsing HTTP Manual**: Membaca string mentah dari browser, memisahkan method (`GET`) dan path (`/`, `/halo`).
3. **Merakit HTTP Response**: Menyusun header (`HTTP/1.1 200 OK`, `Content-Length`, `Content-Type`) dan menggabungkannya dengan body secara manual sebelum di-encode ke bytes.
4. **Multithreading Sederhana**: Pakai `threading.Thread` supaya server bisa nerima koneksi client berikutnya tanpa nunggu proses client sebelumnya selesai.

## File di Repo

- `socket_programmer.py`: Script utama web server soket TCP.
- `index.html`: Eksperimen simulasi animasi sederhana pakai HTML Canvas.

## Cara Menjalankan

1. Jalankan server:
   ```bash
   python3 socket_programmer.py
   ```
2. Buka browser atau terminal lain:
   - `http://127.0.0.1:50007/` -> halaman utama
   - `http://127.0.0.1:50007/halo` -> endpoint sapaan
   - Atau pakai curl:
     ```bash
     curl -i http://127.0.0.1:50007/
     ```

## Catatan & Next Step

Masih banyak keterbatasan (belum handle error parsing kompleks, belum support keep-alive, dan masih thread-per-connection biasa). 

Langkah berikutnya: belajar narik data langsung dari database lokal (PostgreSQL via socket / `psycopg2`) lalu ngerakit hasilnya jadi response HTTP langsung lewat soket ini.
