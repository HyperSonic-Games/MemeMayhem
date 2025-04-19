import socket
import threading
from Networking import UDPServer  # Assuming the UDPServer class is in the Networking module
from Networking import Messages
from Networking import Serializer
import Utils
from pypresence import Presence
from typing import Any
from enum import Enum

DISCORD_APP_CLIENT_ID = "1349055429304520734"

pm = Utils.PopupManager()

serial = Serializer.Serializer()

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

def msg_handler(message: bytes, clientAddress: tuple, server_class: UDPServer.UdpServer):
    try:
        data = serial.deserialize(message)
    except ValueError as e:
        pm.Error("PACKET_DESERIALIZE_ERROR", "Error: " + str(e))
        
        if DEV_MODE:
            print("[DEBUG] Skipping packet due to deserialization error:")
            print(e)
            print("\n")
        
        return  # Skip the packet
    
    if data["TYPE"] == Messages.MessageType.PING:
        header = data["HEADER"]
        
