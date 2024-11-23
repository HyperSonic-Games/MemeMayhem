import FLEXCOM.FLEXCOM
import socket
import threading

class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"[INFO] Connected to server at {self.host}:{self.port}")

        # Start a thread to listen for server messages
        self.receiving_thread = threading.Thread(target=self.receive_messages)
        self.receiving_thread.start()

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))
        print(f"[SENT] {message}")

    def receive_messages(self):
        while True:
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                if response:
                    print(f"[RECEIVED] {response}")
                else:
                    print("[INFO] Server closed the connection.")
                    break
            except ConnectionResetError:
                print("[ERROR] Connection was closed by the server.")
                break

    def close(self):
        self.client_socket.close()
        print("[INFO] Client connection closed.")

if __name__ == "__main__":
    client = Client()
    while True:
        msg = input("Enter a message to send to the server (or 'quit' to exit): ")
        if msg.lower() == 'quit':
            client.close()
            break
        client.send_message(msg)