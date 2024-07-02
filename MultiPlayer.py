import socket
import threading

# Class to represent a message with prefix, message name, IP, and data
class Message:
    def __init__(self, prefix, message_name, ip, data):
        self.prefix = prefix
        self.message_name = message_name
        self.ip = ip
        self.data = data
    
    def __repr__(self):
        return [self.prefix, self.message_name, self.ip, self.data]

# Server class to handle connections and communication with clients
class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        # Create a socket for the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the host and port
        self.server_socket.bind((self.host, self.port))
        # Start listening for incoming connections
        self.server_socket.listen(5)
        print(f"[INFO] Server started at {self.host}:{self.port}")

    # Method to handle communication with a connected client
    def handle_client(self, client_socket, address):
        print(f"[INFO] Connection from {address} has been established.")
        # Send a welcome message to the client
        welcome_message = Message("SVR", "Welcome", self.host, "Welcome to the server!")
        client_socket.send(welcome_message.encode().encode('utf-8'))
        print(f"[SENT] {welcome_message} to {address}")

        while True:
            try:
                # Receive a message from the client
                msg = client_socket.recv(1024).decode('utf-8')
                if msg:
                    message = Message.decode(msg)
                    print(f"[RECEIVED] {message} from {address}")
                    # Send a response message to the client
                    response = Message("SVR", "Response", self.host, "Hello, client!")
                    client_socket.send(response.encode().encode('utf-8'))
                    print(f"[SENT] {response} to {address}")
                else:
                    # Handle the case when the client disconnects
                    print(f"[INFO] Connection from {address} has been closed.")
                    break
            except ConnectionResetError:
                # Handle unexpected disconnection from the client
                print(f"[ERROR] Connection from {address} has been closed unexpectedly.")
                break
        # Close the client socket
        client_socket.close()
        print(f"[INFO] Connection with {address} closed.")

    # Method to start the server and accept connections
    def run(self):
        print(f"[INFO] Server is running and waiting for connections...")
        while True:
            # Accept a new client connection
            client_socket, address = self.server_socket.accept()
            print(f"[INFO] Accepted connection from {address}")
            # Create a new thread to handle the client
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()

# Client class to connect to the server and communicate
class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        # Create a socket for the client
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

        # Start a thread to receive messages from the server
        self.receiving_thread = threading.Thread(target=self.receive_messages)
        self.receiving_thread.start()

    # Method to send a message to the server
    def send_message(self, message_name, data):
        message = Message("CLNT", message_name, self.host, data)
        self.client_socket.send(message.encode().encode('utf-8'))

    # Method to receive messages from the server
    def receive_messages(self):
        while True:
            try:
                # Receive a message from the server
                response = self.client_socket.recv(1024).decode('utf-8')
                if response:
                    message = Message.decode(response)
                    print(f"Received: {message}")
                    # Optionally, process the received message here
                else:
                    # Handle the case when the server closes the connection
                    print("Connection closed by the server.")
                    break
            except ConnectionResetError:
                # Handle unexpected disconnection from the server
                print("Connection closed unexpectedly by the server.")
                break

    # Method to close the client connection
    def close(self):
        self.client_socket.close()
        print("Client connection closed.")
