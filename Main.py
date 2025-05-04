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



DISCORD_APP_CLIENT_ID = "1349055429304520734"

# DEV MODE

SM = SettingsManager.SettingsManager("SETTINGS.toml")



# Initialize Pygame
pygame.init()
Utils.debug_log("PYGAME_INIT", "Pygame initialized")

# Initialize Discord RPC
if Utils.IsDiscordAppInstalled():
    try:
        RPC = Presence(DISCORD_APP_CLIENT_ID)
        RPC.connect()
        RPC.update(state="Playing Meme Mayhem: \nMain Menu")
        Utils.debug_log("DISCORD", "Discord RPC Connected and Presence Set")
    except Exception as e:
        Utils.error_log("DISCORD", f"Failed to initialize Discord RPC: {e}")

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Window title
pygame.display.set_caption(
    "Meme Mayhem (DEV_MODE) - Main Menu" if Config.DEV_MODE else "Meme Mayhem - Main Menu"
)

# Try enabling VSync, fallback if unsupported
try:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
    Utils.debug_log("PYGAME_RENDERER", "VSync Renderer Created")
except Exception as e:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Utils.error_log("PYGAME_RENDERER", f"VSync failed, fallback to normal: {e}")

# Colors
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
NAVY_BLUE = (0, 0, 128)
RED = (255, 0, 0)

# Button settings
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

# ---- Load Splash Text from File ----
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

SPLASH_TEXT = load_splash_text()

# ---- Load Logo Image ----
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

MM_Logo = load_logo()

# ---- Dynamic Font Scaling ----
def get_scaled_font(size_factor=15):
    font_size = SCREEN_WIDTH // size_factor
    return pygame.font.Font(None, font_size)

class Button:
    def __init__(self, x, y, width, height, color, text='', action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = get_scaled_font(20)
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def click(self):
        if self.action:
            Utils.debug_log("UI_BUTTON_CLICK", f"Executing action for: {self.text}")
            self.action()

# ---- Button Actions ----
def play_game():
    pygame.mixer.music.stop()
    pygame.quit()
    Utils.debug_log("LAUNCHER", "Launching Client")
    subprocess.run(["Client"])
    sys.exit()

def host_game():
    pygame.mixer.music.stop()
    pygame.quit()
    Utils.debug_log("LAUNCHER", "Launching Server")
    subprocess.run(["Server"])
    sys.exit()

def show_credits():
    Utils.debug_log("UI_CALLBACK", "Credits button clicked - Feature not implemented yet.")

# ---- Create Buttons ----
MAIN_MENU_BUTTONS = [
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Play", play_game),
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Host", host_game),
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Credits", show_credits)
]

def main_menu():
    # Load music
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
        splash_rect = splash_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10))
        SCREEN.blit(splash_surface, splash_rect)

        # Buttons
        for button in MAIN_MENU_BUTTONS:
            button.draw(SCREEN)

        # Logo
        SCREEN.blit(MM_Logo, (100, 100))

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
