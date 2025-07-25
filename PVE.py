import pygame
import sys
import Utils
from pypresence import Presence
import Config
import CommonDat
import MapSys

DISCORD_APP_CLIENT_ID = "1349055429304520734"
TILE_SIZE = 16
MAP_WIDTH = 0
MAP_HEIGHT = 0
VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 240

pm = Utils.PopupManager()

pygame.init()
Utils.debug_log("PYGAME_INIT", "Pygame initialized")

if Utils.IsDiscordAppInstalled():
    try:
        RPC = Presence(DISCORD_APP_CLIENT_ID)
        RPC.connect()
        RPC.update(state="Playing Meme Mayhem: \nPVE")
        Utils.debug_log("DISCORD", "Discord RPC Connected and Presence Set")
    except Exception as e:
        Utils.error_log("DISCORD", f"Failed to initialize Discord RPC: {e}")

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

pygame.display.set_caption(
    "Meme Mayhem (DEV_MODE) - PVE" if Config.DEV_MODE else "Meme Mayhem - PVE"
)

try:
    SCREEN = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, vsync=1)
    Utils.debug_log("PYGAME_RENDERER", "VSync Fullscreen Renderer Created")
except Exception as e:
    SCREEN = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    Utils.error_log("PYGAME_RENDERER", f"VSync failed, fallback to fullscreen: {e}")

virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
clock = pygame.time.Clock()

scale_x = screen_width // VIRTUAL_WIDTH
scale_y = screen_height // VIRTUAL_HEIGHT
scale = max(1, min(scale_x, scale_y))
x_offset = (screen_width - VIRTUAL_WIDTH * scale) // 2
y_offset = (screen_height - VIRTUAL_HEIGHT * scale) // 2

def screen_to_virtual(mouse_x, mouse_y):
    virtual_x = (mouse_x - x_offset) // scale
    virtual_y = (mouse_y - y_offset) // scale
    return int(virtual_x), int(virtual_y)

# Load map
try:
    tiles = MapSys.parse_map("Assets/Maps/test.mmmap")
    Utils.debug_log("MAP_LOAD", f"Loaded {len(tiles)} tiles")
    MAP_WIDTH, MAP_HEIGHT = MapSys.get_map_size("Assets/Maps/test.mmmap")

    # Find player spawn point
    for i, tile in enumerate(tiles):
        if tile.get_type() == MapSys.TileType.SPWN:
            spawn_x = (i % MAP_WIDTH) * TILE_SIZE
            spawn_y = (i // MAP_WIDTH) * TILE_SIZE
            break
    else:
        spawn_x = spawn_y = 0  # fallback

    player_texture = pygame.Surface((16, 16), pygame.SRCALPHA)
    player_texture.fill((255, 255, 0))  # Yellow box
    player = CommonDat.Player(spawn_x, spawn_y, 0, 100, player_texture)

except Exception as e:
    Utils.error_log("MAP_LOAD", f"Failed to load map: {e}")
    tiles = []
    player_texture = pygame.Surface((16, 16))
    player_texture.fill((255, 0, 255))
    player = CommonDat.Player(0, 0, 0, 100, player_texture)

frame_count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            try:
                RPC.clear() # pyright: ignore[reportPossiblyUnboundVariable]
                RPC.close() # pyright: ignore[reportPossiblyUnboundVariable]
            except:
                pass
            pygame.quit()
            sys.exit()

    # Player movement input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.move(0, -2, tiles, MAP_WIDTH, TILE_SIZE)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.move(0, 2, tiles, MAP_WIDTH, TILE_SIZE)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move(-2, 0, tiles, MAP_WIDTH, TILE_SIZE)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move(2, 0, tiles, MAP_WIDTH, TILE_SIZE)

    # Camera follow player like most top-down games
    map_pixel_width = MAP_WIDTH * TILE_SIZE
    map_pixel_height = MAP_HEIGHT * TILE_SIZE

    if map_pixel_width <= VIRTUAL_WIDTH:
        camera_x = -(VIRTUAL_WIDTH - map_pixel_width) // 2
    else:
        target_x = int(player.get_x() + player_texture.get_width() // 2 - VIRTUAL_WIDTH // 2)
        camera_x = max(0, min(target_x, map_pixel_width - VIRTUAL_WIDTH))

    if map_pixel_height <= VIRTUAL_HEIGHT:
        camera_y = -(VIRTUAL_HEIGHT - map_pixel_height) // 2
    else:
        target_y = int(player.get_y() + player_texture.get_height() // 2 - VIRTUAL_HEIGHT // 2)
        camera_y = max(0, min(target_y, map_pixel_height - VIRTUAL_HEIGHT))

    # Draw map
    virtual_surface.fill((0, 0, 0))
    MapSys.render_map(
        screen=virtual_surface,
        tiles=tiles,
        map_width=MAP_WIDTH,
        map_height=MAP_HEIGHT,
        camera_x=camera_x,
        camera_y=camera_y,
        tile_size=TILE_SIZE,
        frame_count=frame_count
    )

    # Draw player
    player.draw(virtual_surface, camera_x, camera_y)

    # Optional: FPS counter
    if Config.DEV_MODE:
        fps = clock.get_fps()
        font = pygame.font.SysFont(None, 20)
        fps_text = font.render(f"{fps:.1f} FPS", False, (0, 255, 0))
        virtual_surface.blit(fps_text, (2, 2))

    # Scale & blit to screen
    scaled_surface = pygame.transform.scale(
        virtual_surface, (VIRTUAL_WIDTH * scale, VIRTUAL_HEIGHT * scale)
    )
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(scaled_surface, (x_offset, y_offset))
    pygame.display.flip()
    clock.tick(60)
    frame_count += 1
