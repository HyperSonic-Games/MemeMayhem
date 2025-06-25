import enum


"""
about: Common data structures
"""

"""
Class: TileType


"""
class TileType(enum.Enum):
    GROUND = 0
    WALL = 1
    DAMG = 2
    SPWN = 3
    ENEMY_SPWN = 4
    HEALTH = 5

class Tile:
    def __init__(self,):
        pass