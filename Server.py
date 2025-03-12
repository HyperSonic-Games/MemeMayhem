import socket
import threading
from Networking import UDPServer
from Networking import Messages
import Utils
from pypresence import Presence
from typing import Any

DISCORD_APP_CLIENT_ID = "1349055429304520734"

# message template
"""
message = {
    'TYPE'  # Use enum name for message type
    'HEADER': "", # any data for the server/client to have subtypes of packets
    '*': # anything else for the packet's data
}
"""

# DEV MODE
DEV_MODE = True

# Initialize Discord RPC
if Utils.IsDiscordAppInstalled() == True:
    RPC = Presence(DISCORD_APP_CLIENT_ID)
    RPC.connect() # Start the handshake loop
    RPC.update(state="In Main Menu") # Updates our presence

def HANDLE_CONN_ACK(receivedData: Any):
    pass

def HANDLE_CONN_REQ(receivedData: Any):
    pass

def HANDLE_AUTH_REQ(receivedData: Any):
    pass

def HANDLE_AUTH_SUCCESS(receivedData: Any):
    pass

def HANDLE_AUTH_FAIL(receivedData: Any):
    pass

def HANDLE_DATA_REQ(receivedData: Any):
    pass

def HANDLE_DATA_RESP(receivedData: Any):
    pass

def HANDLE_DATA_PUSH(receivedData: Any):
    pass
    
def HANDLE_ERROR(receivedData: Any):
    pass

def HANDLE_PING(receivedData: Any):
    pass

def HANDLE_PONG(receivedData: Any):
    pass

def HANDLE_DISCONNECT(receivedData: Any):
    pass

def HANDLE_DISCONNECT_ACK(receivedData: Any):
    pass