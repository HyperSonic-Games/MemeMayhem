import enum
import pygame



"""
about: Common data structures
"""

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
Class: Tile
Stores all of the data required to query and render a tile on the map
"""
class Tile:

    def __init__(self, type: TileType, texture: pygame.surface.Surface):
        self.type = type
        self.texture = texture
    
    """
    Method: get_type
    Used to query the tile about what type it is
    """
    def get_type(self) -> TileType:
        return self.type
    
    """
    Method: get_type
    Used to query the tile about what type it is
    Returns:
        texture - a pygame surface used to draw the tile
    """
    def get_texture(self):
        return self.texture
    
"""
Class: Entity
The Base class for <Player> and <Enemy>
provides things like location and hp
"""
class Entity:
    def __init__(self, startX, startY, startAngle, startHp, texture: pygame.surface.Surface):
        self.x = startX
        self.y = startY
        self.angle = startAngle
        self.hp = startHp
        self.texture = texture
    
    def get_x(self):
        return self.x
    
    def set_x(self, x):
        self.x = x
    
    def get_y(self):
        return self.y
    
    def set_y(self, y):
        self.y = y
    
    def get_angle(self):
        return self.angle
    
    def set_angle(self, angle):
        self.angle = angle
    
    def get_hp(self):
        return self.hp
    
    def set_hp(self, hp):
        self.hp = hp

    def get_texture(self):
        return self.texture
    
    def set_texture(self, texture: pygame.surface.Surface):
        self.texture = texture

class Player(Entity):
    def __init__(self, startX, startY, startAngle, startHp, texture: pygame.surface.Surface):
        super().__init__(startX, startY, startAngle, startHp, texture)
