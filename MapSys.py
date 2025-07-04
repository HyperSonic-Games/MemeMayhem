import json
import enum
import pygame
import cbor2
from typing import Union, Optional

"""
Enum: TileType
The type of a tile in the map.
"""
class TileType(enum.Enum):
    GROUND = 0       # Walkable ground
    WALL = 1         # Solid wall
    DAMG = 2         # Damage tile
    SPWN = 3         # Player spawn point
    ENEMY_SPWN = 4   # Enemy spawn point
    HEALTH = 5       # Health pickup


"""
Class: Animation
Represents a tile animation.
"""
class Animation:
    """
    Function: __init__
    Creates a new Animation.

    Parameters:
        frames - A list of frame image names.
        rate - How fast the animation plays (frames per step).
        offset - Start delay for the animation.
        loop - Whether the animation loops.
    """
    def __init__(self, frames: list[str], rate: int, offset: int = 0, loop: bool = True):
        self.frames = frames
        self.rate = rate
        self.offset = offset
        self.loop = loop


"""
Class: Tile
A tile on the map with optional texture, animation, health, and properties.
"""
class Tile:
    """
    Constructor: __init__
    Initializes a tile.

    Parameters:
        type - The tile's type (see <TileType>).
        texture - A pygame Surface representing the texture.
        animation - An optional animation for the tile see <Animation>.
        hp - Optional health for destructible tiles.
        properties - A dictionary of custom properties.
    """
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

    """
    Function: get_type
    Gets the type of this tile.

    Returns:
        A TileType value.
    """
    def get_type(self) -> TileType:
        return self.type

    """
    Function: get_texture
    Gets the tile's texture.

    Returns:
        A pygame.Surface.

    Raises:
        ValueError if the tile has no texture or animation.
    """
    def get_texture(self) -> pygame.surface.Surface:
        if self.texture:
            return self.texture
        elif self.animation:
            return load_texture(self.animation.frames[0])
        else:
            raise ValueError("Tile has no texture or animation")


"""
Function: load_texture
Loads a texture by name. (NOT IMPL YET)

Parameters:
    name - The name of the texture to load.

Returns:
    A pygame.Surface placeholder (pink).
"""
def load_texture(name: str) -> pygame.surface.Surface:
    surface = pygame.Surface((16, 16))
    surface.fill((255, 0, 255))
    return surface


"""
Function: parse_tile
Parses a tile from a dictionary.

Parameters:
    data - A dictionary with tile data.

Returns:
    A Tile object.
"""
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


"""
Function: parse_map
Loads and parses a map file (.mmmap or .mmcmap).

Parameters:
    path - Path to the map file.

Returns:
    A list of Tile objects.

Raises:
    ValueError if file format is unknown or tile count doesn't match width * height.
"""
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
        raise ValueError(f"Expected {width * height} tiles, got {len(tiles_data)}")

    return [parse_tile(t) for t in tiles_data]


"""
Function: compile_map
Converts a .mmmap JSON map file to a .mmcmap CBOR binary.

Parameters:
    json_path - Input .mmmap file.
    cbor_path - Output .mmcmap file path. If None, auto-generates path.

Raises:
    ValueError if input is not a .mmmap file.
"""
def compile_map(json_path: str, cbor_path: Union[str, None] = None):
    if not json_path.endswith(".mmmap"):
        raise ValueError("Input must be a .mmmap file")

    if cbor_path is None:
        cbor_path = json_path.replace(".mmmap", ".mmcmap")

    with open(json_path, "r") as f:
        raw = json.load(f)

    with open(cbor_path, "wb") as f:
        cbor2.dump(raw, f)


"""
Function: get_tile_at
Gets the tile at a given world coordinate.

Parameters:
    player_x - X position in pixels.
    player_y - Y position in pixels.
    tiles - List of Tile objects.
    map_width - Width of the map in tiles.
    tile_width - Width of one tile in pixels.
    tile_height - Height of one tile in pixels.

Returns:
    A Tile object the player is currently on.

Raises:
    IndexError if player is outside the map bounds.
"""
def get_tile_at(player_x: int, player_y: int, tiles: list[Tile], map_width: int,
                tile_width: int = 16, tile_height: int = 16) -> Tile:
    tile_x = player_x // tile_width
    tile_y = player_y // tile_height
    index = tile_y * map_width + tile_x

    if index < 0 or index >= len(tiles):
        raise IndexError("Player is outside the map bounds")

    return tiles[index]


"""
Function: is_colliding
Checks if the player is colliding with a solid tile (e.g., WALL).

Parameters:
    player_x - X position of the player.
    player_y - Y position of the player.
    player_w - Width of the player's bounding box.
    player_h - Height of the player's bounding box.
    tiles - List of Tile objects.
    map_width - Width of the map in tiles.
    tile_size - Size of each square tile in pixels.

Returns:
    True if collision with a solid tile is detected, False otherwise.
"""
def is_colliding(player_x: int, player_y: int, player_w: int, player_h: int,
                 tiles: list[Tile], map_width: int, tile_size: int = 16) -> bool:
    def tile_at(px, py):
        tx = px // tile_size
        ty = py // tile_size
        index = ty * map_width + tx
        if 0 <= index < len(tiles):
            return tiles[index]
        return None  # Out of bounds

    points = [
        (player_x, player_y),
        (player_x + player_w - 1, player_y),
        (player_x, player_y + player_h - 1),
        (player_x + player_w - 1, player_y + player_h - 1),
    ]

    for px, py in points:
        tile = tile_at(px, py)
        if tile and tile.get_type() == TileType.WALL:
            return True

    return False
