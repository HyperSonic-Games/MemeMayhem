import pygame
import sys
import Config
import Utils
from NetCode.Networking import UDPClient

from typing import Optional, TypedDict

# DISCORD_APP_CLIENT_ID
# The Client ID used for Discord RPC (Rich Presence) integration.
DISCORD_APP_CLIENT_ID = "13409554293425408734"

pm = Utils.PopupManager()

Client = UDPClient.UDPClient(pm.TextInput("Server IP", "Enter the IP of the server you would like to contect to"), 54777) # type: ignore


# Class: ClientData
# This is the type definiton for player data
class ClientData(TypedDict):
    USERNAME: str
    POS_X: Optional[int]
    POS_Y: Optional[int]
    HP: int
    AMMO: int
    WEAPON: str
    STAT_KILLS: int
    STAT_DEATHS: int
    

PlayerData: ClientData = {"USERNAME": pm.TextInput("UserName", "Enter your username"), "POS_X": None, "POS_Y": None, "HP": 100} # type: ignore

# Try enabling VSync, fallback if unsupported
# Attempts to enable VSync for smoother rendering, with a fallback if VSync is unsupported.
try:
    SCREEN = pygame.display.set_mode(flags=pygame.FULLSCREEN, vsync=1)
    Utils.debug_log("PYGAME_RENDERER", "VSync Renderer Created")
except Exception as e:
    SCREEN = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    Utils.error_log("PYGAME_RENDERER", f"VSync failed, fallback to normal: {e}")



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
