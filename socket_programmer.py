import socket
import threading

import psycopg2

HOST = "127.0.0.1"
PORT = 50007
BACKLOG = 5


# query
def getProducts():
    body = "Daftar Produk Toko:\n"

    try:
        with (
            psycopg2.connect(dbname="devtective", user="devtective") as conn,
            conn.cursor() as cur,
        ):
            cur.execute("SELECT id, nama_produk, harga FROM produk;")
            for _, nama, harga in cur.fetchall():
                body += f"- {nama}: Rp. {harga}\n"

    except Exception as e:
        print(f"[!] gagal mengambil data dari db: {e}")
        body = "Maaf, db sedang gangguan!"

    return body


def handle_client(client_socket, client_address):

    try:
        data = client_socket.recv(1040)

        if data:
            # decode jadi byte
            decode_data = data.decode("utf-8")
            request_lines = decode_data.splitlines()

            if request_lines:
                request_line = request_lines[0].strip()
                parts = request_line.split()

                if len(parts) >= 2:
                    method = parts[0]
                    path = parts[1]

                    status_code = ""
                    body = ""
                    products = getProducts()

                    if path == "/":
                        status_code = "200 OK"
                        body = "selamat datang dihome"
                    elif path == "/halo":
                        status_code = "200 OK"
                        body = products
                    else:
                        status_code = "404 Not Found"
                        body = "404 halaman tidak ditemukan"

                    response_body_bytes = body.encode("utf-8")
                    content_length = len(response_body_bytes)

                    response_headers = (
                        f"HTTP/1.1 {status_code}\r\n"
                        "Content-Type: text/plain; charset=utf-8\r\n"
                        f"Content-Length: {content_length}\r\n"
                        "\r\n"
                    )

                    http_response_bytes = (
                        response_headers.encode("utf-8") + response_body_bytes
                    )
                    client_socket.sendall(http_response_bytes)
        else:
            print(f"client {client_address} tanpa mengirim data.")

    except Exception as e:
        print(f"[!] Terjadi kesalahan saat memproses client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[-] koneksi dengan {client_address} ditutup")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(BACKLOG)

print(f"Socket berhasil di-bind ke {HOST}:{PORT}")

try:
    while True:
        # istilah -> unpacking value / tuple unpacking , s.accept -> nge return -> tuple berisi 2 item
        client_socket, client_address = s.accept()
        # nerima data dari client

        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address)
        )
        client_thread.start()
except KeyboardInterrupt:
    print("\n Menutup server secara aman")

# finally -> memastikan s.close() dijalankan, tidak peduli apakah program keluar karena nekan ctrl + c, atau karena error mendadak.
# memastikan port 50007 langsung dibebaskan kembali oleh sistem operasi tanpa hambatan.
finally:
    s.close()
    print("Socket server berhasil ditutup, see you!")
