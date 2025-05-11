import pygame
import Config
from Utils import PopupManager
from NetCode.Networking import UDPClient

from typing import Optional, TypedDict

# Constant: DISCORD_APP_CLIENT_ID
# The Client ID used for Discord RPC (Rich Presence) integration.
DISCORD_APP_CLIENT_ID = "13409554293425408734"

pm = PopupManager()

Client = UDPClient.UDPClient(pm.TextInput("Server IP", "Enter the IP of the server you would like to contect to"), 54777)


class ClientData(TypedDict):
    USERNAME: str
    POS_X: Optional[int]
    POS_Y: Optional[int]
    HP: int
    AMMO: int
    WEAPON: str
    STAT_KILLS: int
    STAT_DEATHS: int
    
