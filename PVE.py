import pygame
import sys
import Utils
from pypresence import Presence
import Config
import CommonDat

DISCORD_APP_CLIENT_ID = "1349055429304520734"
TILE_SIZE = 16
MAP_WIDTH = 320
MAP_HEIGHT = 180
VIRTUAL_WIDTH = MAP_WIDTH * TILE_SIZE  # 5120
VIRTUAL_HEIGHT = MAP_HEIGHT * TILE_SIZE  # 2880

pm = Utils.PopupManager()

# Initialize Pygame
pygame.init()
Utils.debug_log("PYGAME_INIT", "Pygame initialized")

# Initialize Discord RPC
if Utils.IsDiscordAppInstalled():
    try:
        RPC = Presence(DISCORD_APP_CLIENT_ID)
        RPC.connect()
        RPC.update(state="Playing Meme Mayhem: \nPVE")
        Utils.debug_log("DISCORD", "Discord RPC Connected and Presence Set")
    except Exception as e:
        Utils.error_log("DISCORD", f"Failed to initialize Discord RPC: {e}")

# Get screen info
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set fullscreen and window title
pygame.display.set_caption(
    "Meme Mayhem (DEV_MODE) - PVE" if Config.DEV_MODE else "Meme Mayhem - PVE"
)

# Try enabling VSync, fallback if unsupported
try:
    SCREEN = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, vsync=1)
    Utils.debug_log("PYGAME_RENDERER", "VSync Fullscreen Renderer Created")
except Exception as e:
    SCREEN = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    Utils.error_log("PYGAME_RENDERER", f"VSync failed, fallback to fullscreen: {e}")

# Create a virtual rendering surface
virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
clock = pygame.time.Clock()

# Integer scale factor and centering
scale_x = screen_width // VIRTUAL_WIDTH
scale_y = screen_height // VIRTUAL_HEIGHT
scale = max(1, min(scale_x, scale_y))
x_offset = (screen_width - VIRTUAL_WIDTH * scale) // 2
y_offset = (screen_height - VIRTUAL_HEIGHT * scale) // 2

def screen_to_virtual(mouse_x, mouse_y):
    """Convert real mouse coords to virtual resolution coords."""
    virtual_x = (mouse_x - x_offset) // scale
    virtual_y = (mouse_y - y_offset) // scale
    return int(virtual_x), int(virtual_y)



# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = screen_to_virtual(*event.pos)

    # Clear virtual surface
    virtual_surface.fill((0, 0, 0))

    # Draw grid
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(virtual_surface, (40, 40, 40), rect, 1)


    # Scale and blit to screen
    scaled_surface = pygame.transform.scale(
        virtual_surface, (VIRTUAL_WIDTH * scale, VIRTUAL_HEIGHT * scale)
    )
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(scaled_surface, (x_offset, y_offset))
    pygame.display.flip()
    clock.tick(60)
