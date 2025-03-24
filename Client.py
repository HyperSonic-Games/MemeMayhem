import pygame
import socket
from Networking import Serializer
from Networking import UDPClient
import Utils
from typing import Any
from enum import Enum

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
player_name = Utils.PopupManager().TextInput("Username", "Enter Username:")





hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Message template
"""
message = {
    'TYPE':  # Use enum name for message type
    'HEADER': "",  # Any data for the server/client to have subtypes of packets
    '*':  # Anything else for the packet's data
}
"""

def msg_handler(receivedData):
    pass


udp_client = UDPClient.UdpClient((ip_address, 6969))



# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed


    # Draw the player
    pygame.draw.rect(screen, player_color, (player_x, player_y, 50, 50))

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Clean up
pygame.quit()