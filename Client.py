import pygame
import socket
import os

from Networking import Serializer
from Networking import UDPClient
from Utils import PopupManager

from typing import Any
from enum import Enum

DISCORD_APP_CLIENT_ID = "13409554293425408734"

# DEV MODE
DEV_MODE = True

# Pygame setup
pygame.init()

# Window setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pm = PopupManager()

# Player settings
player_color = (0, 128, 255)
player_x, player_y = 100, 100
player_speed = 5
player_name = pm.TextInput("Username", "Enter Username:")


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
if DEV_MODE:
    print(f"[DEBUG] IP: {ip_address}")

def msg_handler(receivedData: Any):
    pass  # Handle incoming messages here

# Game loop placeholder
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, player_color, (player_x, player_y), 20)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()