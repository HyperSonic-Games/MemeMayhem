import socket
import time
from enum import Enum
from Serializer import Serializer
import Messages


class UdpServer:
    def __init__(self, serverAddress: tuple, messageHandler, timeDelta: float = 0.1):
        """
        Initialize the UDP server with the server address and a custom message handler.

        Args:
        - serverAddress (tuple): Address and port of the server.
        - messageHandler (function): A custom handler function to process incoming messages.
        - timeDelta (float): Time step (in seconds) for sending updates.
        """
        self.ServerAddress = serverAddress
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
        self.ServerSocket.bind(self.ServerAddress)  # Bind server to address
        self.TimeDelta = timeDelta
        self.Players = {}
        self.MessageHandler = messageHandler  # Store the message handler

    def SendToClient(self, clientAddress, message):
        """
        Send a message to a specific client.

        Args:
        - clientAddress (tuple): Address and port of the client.
        - message (dict): Message to send to the client.
        """
        packet = Serializer.Serialize(message)
        self.ServerSocket.sendto(packet, clientAddress)

    def HandleClientMessage(self, data, clientAddress):
        """
        Handle incoming data from a client, call the custom message handler.

        Args:
        - data (bytes): Data received from the client.
        - clientAddress (tuple): Address of the client that sent the data.
        """
        # Deserialize the data
        try:
            message = Serializer.Deserialize(data)
        except ValueError:
            print(f"Failed to deserialize message from {clientAddress}")
            return

        # Call the custom message handler with the message and client address
        self.MessageHandler(message, clientAddress, self)

    def Run(self):
        """
        Run the UDP server. This continuously listens for incoming messages and processes them.
        """
        while True:
            # Listen for messages from clients
            data, clientAddress = self.ServerSocket.recvfrom(4096)  # Buffer size
            self.HandleClientMessage(data, clientAddress)

            # Sleep for the next frame (simulate the game loop)
            time.sleep(self.TimeDelta)