import pygame
import sys
import subprocess
import platform
import random
from pypresence import Presence
import Utils
import SettingsManager

DISCORD_APP_CLIENT_ID = "1349055429304520734"

# DEV MODE
DEV_MODE = True

SM = SettingsManager.SettingsManager("SETTINGS.toml")



# Initialize Pygame
pygame.init()


# Initialize Discord RPC
if Utils.IsDiscordAppInstalled() == True:
    RPC = Presence(DISCORD_APP_CLIENT_ID)
    RPC.connect() # Start the handshake loop
    RPC.update(state="Playing Meme Mayhem: \nMain Menu") # Updates our presence

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.display.set_caption("Meme Mayhem - Main Menu")

# Try enabling VSync, fallback if unsupported
try:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
    if DEV_MODE:
        print("[DEBUG] VSync Renderer Created")
except Exception as e:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    if DEV_MODE:
        print(f"[DEBUG] Normal Renderer Created - Error: {e}")

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
    """Load a random splash text from file."""
    try:
        with open("Assets/splash.txt", "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
            return random.choice(lines) if lines else "Welcome!"
    except FileNotFoundError:
        if DEV_MODE:
            print("[DEBUG] Splash text file not found!")
        return "Welcome!"

SPLASH_TEXT = load_splash_text()

# ---- Dynamic Font Scaling ----
def get_scaled_font(size_factor=15):
    """Dynamically scale font size based on screen width."""
    font_size = SCREEN_WIDTH // size_factor
    return pygame.font.Font(None, font_size)

class Button:
    def __init__(self, x, y, width, height, color, text='', action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = get_scaled_font(20)  # Scale button text dynamically
        self.action = action  # Store function reference

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def click(self):
        """Execute the button's assigned action."""
        if self.action:
            self.action()

# ---- Button Actions ----
def play_game():
    """Launch the client."""
    pygame.mixer.music.stop()
    pygame.quit()
    if DEV_MODE:
        print("[DEBUG] Launching Client")
        subprocess.run(["Client"])
    else:
        subprocess.run(["Client"])
    sys.exit()

def host_game():
    """Launch the server."""
    pygame.mixer.music.stop()
    pygame.quit()
    if DEV_MODE:
        print("[DEBUG] Launching Server")
        subprocess.run(["Server"])
    else:
        subprocess.run(["Server"])
    sys.exit()

def show_credits():
    """Show credits (placeholder)."""
    if DEV_MODE:
        print("[DEBUG] Credits button clicked - Feature not implemented yet.")

# ---- Create Buttons ----
MAIN_MENU_BUTTONS = [
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Play", play_game),
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Host", host_game),
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, NAVY_BLUE, "Credits", show_credits)
]

def main_menu():
    """Display the main menu."""
    try:
        pygame.mixer.music.load("Assets/Sound/Prisoner.mp3")
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except pygame.error as e:
        if DEV_MODE:
            print(f"[DEBUG] Failed to load music: {e}")

    splash_font = get_scaled_font(21)  # Splash text should be larger

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in MAIN_MENU_BUTTONS:
                    if button.rect.collidepoint(event.pos):
                        button.click()  # Execute associated function

        # Render UI
        SCREEN.fill(GRAY)

        # Draw splash text at the top center
        splash_surface = splash_font.render(SPLASH_TEXT, True, WHITE)
        splash_rect = splash_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10))
        SCREEN.blit(splash_surface, splash_rect)

        # Draw buttons
        for button in MAIN_MENU_BUTTONS:
            button.draw(SCREEN)

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
