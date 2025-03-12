import pygame
import socket

DISCORD_APP_CLIENT_ID = "1349055429304520734"

# DEV MODE
DEV_MODE = True

# Pygame setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Player settings

player_color = (0, 128, 255)
player_x, player_y = 400, 300
player_speed = 5
