
import socket

HOST = "127.0.0.1"
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print("Connected to server!")
    print("Enter text or EXIT to quit.")

    while True:
        text = input("\nEnter text: ")
        client.sendall(text.encode("utf-8"))

        if text.upper() == "EXIT":
            break

        response = client.recv(4096).decode("utf-8")
        print(response)

print("Disconnected.")
