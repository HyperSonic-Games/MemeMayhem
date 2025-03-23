import socket
import threading
from Networking import UDPServer  # Assuming the UDPServer class is in the Networking module
from Networking import Messages
import Utils
from pypresence import Presence
from typing import Any
from enum import Enum

DISCORD_APP_CLIENT_ID = "1349055429304520734"

# Message template
"""
message = {
    'TYPE':  # Use enum name for message type
    'HEADER': "",  # Any data for the server/client to have subtypes of packets
    '*':  # Anything else for the packet's data
}
"""

# DEV MODE
DEV_MODE = True

# Initialize Discord RPC
if Utils.IsDiscordAppInstalled():
    RPC = Presence(DISCORD_APP_CLIENT_ID)
    RPC.connect()  # Start the handshake loop
    RPC.update(state="Running a Meme Mayhem Server")  # Updates our presence


"""
Welcome to the
How The Actual F*** Does This Work Part™

Basically, each message handler parses the header and calls out to other functions,
which then do most of the work.

"""

Players = [] # format {name: "", pox_x: 0, pos_y: 0, hp: 100, wep: 0}

# Message Handlers
def HANDLE_CONN_ACK(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    print(f"Connection Acknowledged from {clientAddress}")
    # You can send a response back to the client
    response = {
        'TYPE': 'CONN_ACK',
        'HEADER': "ACK_RECEIVED"
    }
    server.SendToClient(clientAddress, response)

def HANDLE_CONN_REQ(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    print(f"Connection Request from {clientAddress}")
    # Process the connection request and send a response
    response = {
        'TYPE': 'CONN_ACK',
        'HEADER': "CONN_ESTABLISHED"
    }
    server.SendToClient(clientAddress, response)

# Other Handlers (you can implement them similarly)
def HANDLE_AUTH_REQ(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass

def HANDLE_AUTH_SUCCESS(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass

def HANDLE_AUTH_FAIL(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass

def HANDLE_DATA_REQ(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass

def HANDLE_DATA_PUSH(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass


def HANDLE_ERROR(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass

def HANDLE_PING(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass

def HANDLE_PONG(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass


def HANDLE_DISCONNECT(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass

def HANDLE_DISCONNECT_ACK(receivedData: Any, clientAddress: tuple, server: UDPServer.UdpServer):
    pass


# The Server Class
class Server:
    def __init__(self, server_address: tuple):
        self.server_address = server_address
        self.udp_server = UDPServer.UdpServer(server_address, self.message_handler)

    def message_handler(self, message: Any, clientAddress: tuple, server: UDPServer.UdpServer):
        """
        Custom message handler to route messages to the correct handler based on message type.
        """
        message_type = message.get('TYPE', None)

        if message_type == 'CONN_ACK':
            HANDLE_CONN_ACK(message, clientAddress, server)
        elif message_type == 'CONN_REQ':
            HANDLE_CONN_REQ(message, clientAddress, server)
        elif message_type == 'AUTH_REQ':
            HANDLE_AUTH_REQ(message, clientAddress, server)
        elif message_type == 'AUTH_SUCCESS':
            HANDLE_AUTH_SUCCESS(message, clientAddress, server)
        elif message_type == 'AUTH_FAIL':
            HANDLE_AUTH_FAIL(message, clientAddress, server)
        # Add other handlers for additional message types

    def run(self):
        """
        Run the server. This method starts the UDP server and handles incoming client messages.
        """
        self.udp_server.Run()

# Main Loop to Start the Server
def mainloop():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    server_address =(ip_address, 666)
    server = Server(server_address)

    # Run the server
    server.run()

if __name__ == "__main__":
    mainloop()
