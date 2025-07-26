from enum import Enum

class TileType(Enum):
    GROUND = 0
    WALL = 1
    SPWN = 2
    ENEMY_SPWN = 3
    HEAL = 4
    DMG = 5

class Tile:
    def __init__(self, texture: str, tile_type: TileType):
        self.texture = texture
        self.tile_type = tile_type
        self.collidable = tile_type == TileType.WALL

TILE_SIZE = 32

def point_tile_collides(tilemap, tile_size, px, py):
    tx = int(px // tile_size)
    ty = int(py // tile_size)
    if 0 <= ty < len(tilemap) and 0 <= tx < len(tilemap[0]):
        return tilemap[ty][tx].collidable
    return False

# Build 100x100 map filled with ground
DEV_GRASS_PLAIN = [[Tile("grass", TileType.GROUND) for _ in range(100)] for _ in range(100)]

def add_building(x, y, w, h, door_positions=None):
    """
    door_positions: list of (ix, iy) tile coords relative to building top-left, where doors should be placed.
    """
    if door_positions is None:
        door_positions = []

    for iy in range(y, y + h):
        for ix in range(x, x + w):
            # walls on edges only (building border)
            if ix == x or ix == x + w - 1 or iy == y or iy == y + h - 1:
                rel_x = ix - x
                rel_y = iy - y
                if (rel_x, rel_y) in door_positions:
                    DEV_GRASS_PLAIN[iy][ix] = Tile("door", TileType.GROUND)
                else:
                    DEV_GRASS_PLAIN[iy][ix] = Tile("wall", TileType.WALL)
            else:
                DEV_GRASS_PLAIN[iy][ix] = Tile("grass", TileType.GROUND)

# Add building 1 at (10,10) 20x15 tiles with door at bottom center (relative tile (10,14))
add_building(10, 10, 20, 15, door_positions=[(10, 14)])

# Add building 2 at (50,50) 30x25 tiles with two doors (left edge center and right edge center)
add_building(50, 50, 30, 25, door_positions=[(0, 12), (29, 12)])
