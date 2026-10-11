
import socket

HOST = "127.0.0.1"
PORT = 8081

sent = 100
received = 0
lost = 0

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    client.settimeout(1)

    for i in range(1, sent + 1):
        message = f"Packet #{i}"
        client.sendto(message.encode("utf-8"), (HOST, PORT))

        try:
            data, addr = client.recvfrom(4096)
            received += 1
            print(f"{message} -> {data.decode('utf-8')}")
        except socket.timeout:
            lost += 1
            print(f"{message} -> TIMEOUT (lost)")

print("\n--- UDP Test Results ---")
print(f"Sent: {sent}")
print(f"Received: {received}")
print(f"Lost: {lost}")
print(f"Packet Loss: {lost / sent * 100:.1f}%")
