import re

class MapLoader:
    def __init__(self, PathToMapFile: str):
        with open(PathToMapFile, 'r') as f:
            self.MapData = f.read()