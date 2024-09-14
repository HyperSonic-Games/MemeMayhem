import pygame
import sys
import threading
import socket

# Set up the server
class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        # Create a socket for the client
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.server_socket.connect((self.host, self.port))
        #Bind the socket to the host and port
        self.server_socket.bind((self.host, self.port)) 
        #Start listening for incoming connections
        self.server_socket.listen(5)
        print(f"Connected to server at {self.host}:{self.port}")


        # Method to handle comuniaction with the clients
        def handle_client(self, client_socket, address)
            print(f"Connection from {address}has be established")
            
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

    #Method to start the server an comunicate 
    def run(self):
        print("Accepted connection from Client")
        while True
            #Accept new client connection
            client_socket, address = self.server_socket.accept()
            print(f"Accepted connection from {address}")
            # Create a new thread to handle client 
            client_handler = threading.Thread(target=self.server_socket.accept)
            client_handler.start()
            