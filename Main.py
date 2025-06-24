import pygame
import sys
import subprocess
import platform
import random
from pypresence import Presence
import Utils
import SettingsManager
import os

import Config


# The Client ID used for Discord RPC (Rich Presence) integration.
DISCORD_APP_CLIENT_ID = "1349055429304520734"


# Initializes the settings manager for loading the game's settings from a TOML file.
SM = SettingsManager.SettingsManager("SETTINGS.toml") # type: ignore

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
    "Meme Mayhem (DEV_MODE) - Main Menu" if Config.DEV_MODE else "Meme Mayhem - Main Menu"
)

# Try enabling VSync, fallback if unsupported
# Attempts to enable VSync for smoother rendering, with a fallback if VSync is unsupported.
try:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
    Utils.debug_log("PYGAME_RENDERER", "VSync Renderer Created")
except Exception as e:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Utils.error_log("PYGAME_RENDERER", f"VSync failed, fallback to normal: {e}")

#Constants: Colors
# Defines commonly used colors in RGB format for UI elements.
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
NAVY_BLUE = (0, 0, 128)
RED = (255, 0, 0)

# Constants: Button settings
# Configures the size and spacing for the buttons in the main menu.
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

# Function: load_splash_text
# Loads a random splash text from a text file located in the "Assets" directory.
#
# Parameters:
#     None
#
# Returns:
#     string - A randomly selected line from the splash text file, or a default message if the file cannot be loaded.
#
# Notes:
#     If the splash text file is not found or there is an error reading it, a fallback message will be used.
def load_splash_text():
    path = os.path.join("Assets", "splash.txt")
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
            Utils.debug_log("FILE_LOADER", f"Loaded splash text file: {os.path.abspath(path)}")
            return random.choice(lines) if lines else "Welcome!"
    except FileNotFoundError:
        Utils.warn_log("FILE_LOADER", f"Splash text file not found at: {os.path.abspath(path)}")
        return "Welcome To Meme Mayhem!"
    except Exception as e:
        Utils.error_log("FILE_LOADER", f"Unexpected error reading splash text: {e}")
        return "Welcome!"

# Loads the splash text to be displayed at the top of the main menu.
SPLASH_TEXT = load_splash_text()

# Function: load_logo
# Loads the logo image from the "Assets" directory.
#
# Parameters:
#     None
#
# Returns:
#     pygame.Surface - The loaded logo image, or a fallback surface if the logo cannot be loaded.
#
# Notes:
#     If the logo file is not found or there is an error loading it, a red fallback surface will be used.
def load_logo():
    path = os.path.join("Assets", "Images", "IconsAndLogos", "MemeMayhemLogo.png")
    try:
        logo = pygame.image.load(path)
        Utils.debug_log("FILE_LOADER", f"Loaded logo image from: {os.path.abspath(path)}")
        return logo
    except FileNotFoundError:
        Utils.warn_log("FILE_LOADER", f"Logo image not found at: {os.path.abspath(path)}")
    except pygame.error as e:
        Utils.error_log("FILE_LOADER", f"Pygame image load failed: {e}")
    except Exception as e:
        Utils.error_log("FILE_LOADER", f"Unknown error loading logo: {e}")

    # fallback logo
    fallback = pygame.Surface((100, 100))
    fallback.fill(RED)
    return fallback

# Loads the Meme Mayhem logo image for display in the main menu.
MM_Logo = load_logo()

# Function: get_scaled_font
# Dynamically scales the font size based on the screen width to maintain UI consistency.
#
# Parameters:
#     size_factor - Factor for determining the font size (default is 15).
#
# Returns:
#     pygame.font.Font - A Pygame font object with the calculated font size.
def get_scaled_font(size_factor=15):
    font_size = SCREEN_WIDTH // size_factor
    return pygame.font.Font(None, font_size)

# Button class: Defines the structure and behavior of a UI button in the main menu.
class Button:
    def __init__(self, x, y, width, height, color, text='', action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = get_scaled_font(20)
        self.action = action

    def draw(self, surface):
        # Draws the button on the given surface.
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def click(self):
        # Executes the action associated with the button when clicked.
        if self.action:
            Utils.debug_log("UI_BUTTON_CLICK", f"Executing action for: {self.text}")
            self.action()

# ---- Button Actions ----
# Actions executed when buttons in the main menu are clicked.

def play_PVE():
    # Stops music, quits Pygame, and launches the PVE engine.
    pygame.mixer.music.stop()
    pygame.quit()
    Utils.debug_log("LAUNCHER", "Launching Client(PVE)")
    subprocess.run(["PVE"])
    sys.exit()

def play_game():
    # Stops music, quits Pygame, and launches the game client for PVE mode.
    pygame.mixer.music.stop()
    pygame.quit()
    Utils.debug_log("LAUNCHER", "Launching Client")
    subprocess.run(["Client"])
    sys.exit()

def host_game():
    # Stops music, quits Pygame, and launches the game server.
    pygame.mixer.music.stop()
    pygame.quit()
    Utils.debug_log("LAUNCHER", "Launching Server")
    subprocess.run(["Server"])
    sys.exit()

def show_credits():
    # Placeholder function for displaying credits; not implemented yet.
    Utils.debug_log("UI_CALLBACK", "Credits button clicked - Feature not implemented yet.")

# ---- Create Buttons ----
# Creates buttons for "Play", "Host", and "Credits" in the main menu.
MAIN_MENU_BUTTONS = [
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "PVE", play_PVE),
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Play", play_game),
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Host", host_game),
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Credits", show_credits)
]

# Function: main_menu
# The main menu of the game, responsible for rendering the UI and handling button clicks.
#
# Parameters:
#     None
#
# Returns:
#     None
def main_menu():
    # Load and play background music
    music_path = os.path.join("Assets", "Sound", "Prisoner.mp3")
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        Utils.debug_log("FILE_LOADER", f"Loaded and playing music from: {os.path.abspath(music_path)}")
    except FileNotFoundError:
        Utils.warn_log("FILE_LOADER", f"Music file not found at: {os.path.abspath(music_path)}")
    except pygame.error as e:
        Utils.error_log("FILE_LOADER", f"Failed to load music: {e}")
    except Exception as e:
        Utils.error_log("FILE_LOADER", f"Unknown error loading music: {e}")

    splash_font = get_scaled_font(21)

    while True:
        for event in pygame.event.get():
            # Only log non-mouse movement events
            if event.type not in [pygame.MOUSEMOTION]:  # Exclude mouse movement
                Utils.debug_log("PYGAME_EVENTS", event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in MAIN_MENU_BUTTONS:
                    if button.rect.collidepoint(event.pos):
                        button.click()

        # Render UI
        SCREEN.fill(GRAY)

        # Splash text
        splash_surface = splash_font.render(SPLASH_TEXT, True, WHITE)
        splash_rect = splash_surface
