
import socket
import threading
from datetime import datetime
from collections import Counter

HOST = "127.0.0.1"
PORT = 8080


def analyze_text(text):
    words = text.lower().split()
    word_count = len(words)
    char_count = len(text)
    common_words = Counter(words).most_common(3)

    return (
        f"Words: {word_count}\n"
        f"Characters: {char_count}\n"
        f"Most common: {common_words}"
    )


def handle_client(conn, addr):
    print(f"Client connected: {addr[0]}:{addr[1]}")
    print(f"Time: {datetime.now()}")

    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            text = data.decode("utf-8").strip()

            if text.upper() == "EXIT":
                break

            result = analyze_text(text)
            conn.sendall(result.encode("utf-8"))

    print(f"Client disconnected: {addr}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        print(f"TCP server started on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            )
            thread.start()

def start_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.bind((HOST, 8081))
        print("UDP server started on 127.0.0.1:8081")

        packet_count = 0

        while True:
            data, addr = udp.recvfrom(4096)
            text = data.decode("utf-8")

            if text.startswith("Packet #"):
                packet_count += 1

                # Відкидаємо кожен 10-й тестовий пакет
                if packet_count % 10 == 0:
                    print(f"Dropped: {text}")
                    continue

            response = f"Length: {len(text)}"
            udp.sendto(response.encode("utf-8"), addr)

if __name__ == "__main__":
    threading.Thread(target=start_udp_server, daemon=True).start()
    start_server()
