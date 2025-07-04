import json
import enum
import pygame
import cbor2
from typing import Union, Optional

"""
Class: TileType
The Type of tile on the map
"""
class TileType(enum.Enum):
    GROUND = 0
    WALL = 1
    DAMG = 2
    SPWN = 3
    ENEMY_SPWN = 4
    HEALTH = 5


"""
Class: Animation
Stores all of the data needed for animated tiles
"""
class Animation:
    def __init__(self, frames: list[str], rate: int, offset: int = 0, loop: bool = True):
        self.frames = frames
        self.rate = rate
        self.offset = offset
        self.loop = loop


"""
Class: Tile
Stores all of the data required to query and render a tile on the map
"""
class Tile:
    def __init__(self,
                 type: TileType,
                 texture: Optional[pygame.surface.Surface] = None,
                 animation: Optional[Animation] = None,
                 hp: Optional[int] = None,
                 properties: Optional[dict] = None):
        self.type = type
        self.texture = texture
        self.animation = animation
        self.hp = hp
        self.properties = properties or {}

    def get_type(self) -> TileType:
        return self.type

    def get_texture(self) -> pygame.surface.Surface:
        if self.texture:
            return self.texture
        elif self.animation:
            return load_texture(self.animation.frames[0])  # Default preview frame
        else:
            raise ValueError("Tile has no texture or animation")


def load_texture(name: str) -> pygame.surface.Surface:
    # Replace with actual image loading logic
    surface = pygame.Surface((16, 16))
    surface.fill((255, 0, 255))  # Pink placeholder
    return surface


def parse_tile(data: dict) -> Tile:
    t = TileType(data["t"])

    tex = None
    anim = None

    if "tex" in data:
        tex = load_texture(data["tex"])
    elif "anim" in data:
        a = data["anim"]
        anim = Animation(
            frames=a["frames"],
            rate=a["rate"],
            offset=a.get("offset", 0),
            loop=a.get("loop", True)
        )
    else:
        raise ValueError("Tile must have either 'tex' or 'anim'")

    hp = data.get("hp")
    props = data.get("p", {})

    return Tile(t, tex, anim, hp, props)


def parse_map(path: str) -> list[Tile]:
    if path.endswith(".mmmap"):
        with open(path, "r") as f:
            raw = json.load(f)
    elif path.endswith(".mmcmap"):
        with open(path, "rb") as f:
            raw = cbor2.load(f)
    else:
        raise ValueError("Unsupported file extension")

    width = raw["width"]
    height = raw["height"]
    tiles_data = raw["tiles"]

    if len(tiles_data) != width * height:
        raise ValueError(f"Expected {width*height} tiles, got {len(tiles_data)}")

    return [parse_tile(t) for t in tiles_data]


def compile_map(json_path: str, cbor_path: Union[str, None] = None):
    if not json_path.endswith(".mmmap"):
        raise ValueError("Input must be a .mmmap file")

    if cbor_path is None:
        cbor_path = json_path.replace(".mmmap", ".mmcmap")

    with open(json_path, "r") as f:
        raw = json.load(f)

    with open(cbor_path, "wb") as f:
        cbor2.dump(raw, f)

# anoying math to get the tile we are on
def get_tile_at(player_x: int, player_y: int, tiles: list[Tile], map_width: int, tile_width: int = 16, tile_height: int = 16) -> Tile:
    tile_x = player_x // tile_width
    tile_y = player_y // tile_height
    index = tile_y * map_width + tile_x

    if index < 0 or index >= len(tiles):
        raise IndexError("Player is outside the map bounds")

    return tiles[index]