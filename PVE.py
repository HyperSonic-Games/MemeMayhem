import pygame
import math
from MAPS import DEV_GRASS_PLAIN, TILE_SIZE, point_tile_collides, TileType

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
zoom = 3.0  # zoom level (tweak to fit)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meme Mayhem - Raycast Shadows Demo")
clock = pygame.time.Clock()

entity = {
    'x': 15 * TILE_SIZE + TILE_SIZE // 2,
    'y': 15 * TILE_SIZE + TILE_SIZE // 2,
    'radius': 14,
    'rotation': 0,
    'speed': 180,
}

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def resolve_collision(entity, tilemap, tile_size):
    px, py = entity['x'], entity['y']
    r = entity['radius']

    left_tile = int((px - r) // tile_size)
    right_tile = int((px + r) // tile_size)
    top_tile = int((py - r) // tile_size)
    bottom_tile = int((py + r) // tile_size)

    for ty in range(top_tile, bottom_tile + 1):
        for tx in range(left_tile, right_tile + 1):
            if 0 <= ty < len(tilemap) and 0 <= tx < len(tilemap[0]):
                if tilemap[ty][tx].collidable:
                    tile_rect = pygame.Rect(tx * tile_size, ty * tile_size, tile_size, tile_size)
                    closest_x = clamp(px, tile_rect.left, tile_rect.right)
                    closest_y = clamp(py, tile_rect.top, tile_rect.bottom)

                    dist_x = px - closest_x
                    dist_y = py - closest_y
                    dist_sq = dist_x * dist_x + dist_y * dist_y

                    if dist_sq < r * r:
                        dist = math.sqrt(dist_sq)
                        if dist == 0:
                            # Push out in arbitrary direction
                            if py > tile_rect.centery:
                                dist_y = 1
                                dist_x = 0
                            else:
                                dist_y = -1
                                dist_x = 0
                            dist = 1
                        push_dist = r - dist
                        nx = dist_x / dist
                        ny = dist_y / dist
                        entity['x'] += nx * push_dist
                        entity['y'] += ny * push_dist

def cast_rays(entity, tilemap, tile_size, num_rays=360, max_dist=600):
    px, py = entity['x'], entity['y']
    points = []

    for i in range(num_rays):
        angle = math.radians(i)
        dx = math.cos(angle)
        dy = math.sin(angle)

        for dist in range(0, max_dist, 4):
            test_x = px + dx * dist
            test_y = py + dy * dist
            if point_tile_collides(tilemap, tile_size, test_x, test_y):
                points.append((test_x, test_y))
                break
        else:
            points.append((px + dx * max_dist, py + dy * max_dist))
    return points

def world_to_screen(wx, wy, cam_x, cam_y):
    sx = (wx - cam_x) * zoom + SCREEN_WIDTH // 2
    sy = (wy - cam_y) * zoom + SCREEN_HEIGHT // 2
    return int(sx), int(sy)

def draw_tilemap(surface, tilemap, tile_size, cam_x, cam_y):
    tiles_x = int(SCREEN_WIDTH / (tile_size * zoom)) + 2
    tiles_y = int(SCREEN_HEIGHT / (tile_size * zoom)) + 2
    start_x = int(cam_x // tile_size) - tiles_x // 2
    start_y = int(cam_y // tile_size) - tiles_y // 2

    for y in range(start_y, start_y + tiles_y):
        for x in range(start_x, start_x + tiles_x):
            if 0 <= y < len(tilemap) and 0 <= x < len(tilemap[0]):
                tile = tilemap[y][x]
                color = (80, 180, 80) if tile.tile_type == TileType.GROUND else (60, 60, 60)
                rect = pygame.Rect(0, 0, tile_size * zoom, tile_size * zoom)
                screen_x, screen_y = world_to_screen(x * tile_size, y * tile_size, cam_x, cam_y)
                rect.topleft = (screen_x, screen_y)
                pygame.draw.rect(surface, color, rect)
                if tile.collidable:
                    pygame.draw.rect(surface, (255, 0, 0), rect, 1)

def draw_player(surface, entity, cam_x, cam_y):
    px, py = world_to_screen(entity['x'], entity['y'], cam_x, cam_y)
    r = int(entity['radius'] * zoom)
    pygame.draw.circle(surface, (0, 255, 0), (px, py), r, 3)

    angle_rad = math.radians(entity['rotation'] - 90)
    tip_x = entity['x'] + math.cos(angle_rad) * (entity['radius'] + 16)
    tip_y = entity['y'] + math.sin(angle_rad) * (entity['radius'] + 16)
    tip_sx, tip_sy = world_to_screen(tip_x, tip_y, cam_x, cam_y)
    pygame.draw.line(surface, (255, 0, 0), (px, py), (tip_sx, tip_sy), 2)
    pygame.draw.circle(surface, (255, 0, 0), (tip_sx, tip_sy), max(3, int(4 * zoom)))

def draw_shadows(surface, entity, tilemap, tile_size, cam_x, cam_y):
    points = cast_rays(entity, tilemap, tile_size)
    screen_points = [world_to_screen(x, y, cam_x, cam_y) for x, y in points]

    shadow_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 200))  # fill whole screen with semi-transparent black
    pygame.draw.polygon(shadow_surface, (0, 0, 0, 0), screen_points)  # cut out light (fully transparent)
    surface.blit(shadow_surface, (0, 0))

def main():
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_rel()

        entity['rotation'] = (entity['rotation'] + mx * 0.3) % 360 # type: ignore

        move_dx = 0
        move_dy = 0
        if keys[pygame.K_w]: move_dy -= 1
        if keys[pygame.K_s]: move_dy += 1
        if keys[pygame.K_a]: move_dx -= 1
        if keys[pygame.K_d]: move_dx += 1

        length = math.hypot(move_dx, move_dy)
        if length > 0:
            move_dx /= length
            move_dy /= length

        entity['x'] += move_dx * entity['speed'] * dt # type: ignore
        entity['y'] += move_dy * entity['speed'] * dt # type: ignore

        resolve_collision(entity, DEV_GRASS_PLAIN, TILE_SIZE)

        cam_x, cam_y = entity['x'], entity['y']

        screen.fill((30, 30, 30))
        draw_tilemap(screen, DEV_GRASS_PLAIN, TILE_SIZE, cam_x, cam_y)
        draw_player(screen, entity, cam_x, cam_y)
        draw_shadows(screen, entity, DEV_GRASS_PLAIN, TILE_SIZE, cam_x, cam_y)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
