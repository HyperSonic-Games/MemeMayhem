import pygame, math
from MAPS import TILE_SIZE, point_tile_collides

RAY_COUNT = 360
ANGLES = [math.radians(a) for a in range(RAY_COUNT)]
MAX_LIGHT_DIST = 400
STEP = 1

def cast_light_polygon(entity, tilemap):
    px, py = entity['x'], entity['y']
    points = []
    for ang in ANGLES:
        dx, dy = math.cos(ang), math.sin(ang)
        hit_x, hit_y = px + dx * MAX_LIGHT_DIST, py + dy * MAX_LIGHT_DIST
        for dist in range(0, MAX_LIGHT_DIST, STEP):
            tx, ty = px + dx * dist, py + dy * dist
            if point_tile_collides(tilemap, TILE_SIZE, tx, ty):
                hit_x, hit_y = tx, ty
                break
        points.append((hit_x, hit_y))
    return points

def draw_light_and_shadows(screen, entity, tilemap, cam_x, cam_y, zoom):
    poly = cast_light_polygon(entity, tilemap)
    screen_poly = [((x - cam_x) * zoom + screen.get_width()//2,
                    (y - cam_y) * zoom + screen.get_height()//2) for x, y in poly]

    shadow_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    shadow_surf.fill((0,0,0,200))  # fill whole screen with shadow (semi-transparent black)
    pygame.draw.polygon(shadow_surf, (0,0,0,0), screen_poly)  # cut out light area (fully transparent)

    glow_rad = int(entity['radius'] * zoom * 3)
    glow = pygame.Surface((glow_rad*2, glow_rad*2), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255,255,180,80), (glow_rad, glow_rad), glow_rad)
    gx = int((entity['x'] - cam_x) * zoom + screen.get_width()//2 - glow_rad)
    gy = int((entity['y'] - cam_y) * zoom + screen.get_height()//2 - glow_rad)
    shadow_surf.blit(glow, (gx, gy), special_flags=pygame.BLEND_ADD)

    screen.blit(shadow_surf, (0,0))
