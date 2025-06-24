import pygame
import sys
import Utils
from pypresence import Presence
import Config


DISCORD_APP_CLIENT_ID = "1349055429304520734"

pm = Utils.PopupManager()


# Initialize Pygame
# Initializes Pygame and logs the successful initialization.
pygame.init()
Utils.debug_log("PYGAME_INIT", "Pygame initialized")


# Initialize Discord RPC
# Sets up the Discord Rich Presence integration to show the game's status on Discord.
if Utils.IsDiscordAppInstalled():
    try:
        RPC = Presence(DISCORD_APP_CLIENT_ID)
        RPC.connect()
        RPC.update(state="Playing Meme Mayhem: \nMain Menu")
        Utils.debug_log("DISCORD", "Discord RPC Connected and Presence Set")
    except Exception as e:
        Utils.error_log("DISCORD", f"Failed to initialize Discord RPC: {e}")


# Screen settings
# Sets up the screen width and height for the main menu window.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Window title
# Sets the window title based on whether DEV_MODE is enabled in the config.
pygame.display.set_caption(
    "Meme Mayhem (DEV_MODE) - PVE" if Config.DEV_MODE else "Meme Mayhem - PVE"
)

# Try enabling VSync, fallback if unsupported
# Attempts to enable VSync for smoother rendering, with a fallback if VSync is unsupported.
try:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
    Utils.debug_log("PYGAME_RENDERER", "VSync Renderer Created")
except Exception as e:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Utils.error_log("PYGAME_RENDERER", f"VSync failed, fallback to normal: {e}")



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

