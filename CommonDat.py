import enum
import pygame
import MapSys


"""
about: Common data structures
"""

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
    
    def move(self, dx, dy, tiles, map_width, tile_size):
        new_x = self.x + dx
        new_y = self.y + dy
        
        if not MapSys.is_colliding(new_x, new_y, 16, 16, tiles, map_width, tile_size):
            self.x = new_x
            self.y = new_y

    def draw(self, surface, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        surface.blit(self.texture, (draw_x, draw_y))

