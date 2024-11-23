import FLEXCOM.FLEXCOM
import socket
import threading

class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[INFO] Server started at {self.host}:{self.port}")

    def handle_client(self, client_socket, address):
        print(f"[INFO] Connection from {address} has been established.")
        client_socket.send("Welcome to the server!".encode('utf-8'))

        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if msg:
                    print(f"[RECEIVED] {msg} from {address}")
                    response = f"Server received: {msg}"
                    client_socket.send(response.encode('utf-8'))
                    print(f"[SENT] Response to {address}")
                else:
                    print(f"[INFO] Connection with {address} has been closed.")
                    break
            except ConnectionResetError:
                print(f"[ERROR] Connection with {address} was closed unexpectedly.")
                break

        client_socket.close()

    def run(self):
        print("[INFO] Server is running and waiting for connections...")
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"[INFO] Accepted connection from {address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()

if __name__ == "__main__":
    server = Server()
    server.run()