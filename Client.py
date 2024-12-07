import pygame
import socket
import pickle

# Pygame setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Player settings
player_size = 50
player_color = (0, 128, 255)
player_x, player_y = 400, 300
player_speed = 5

# Socket setup
host = '127.0.0.1'
port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states for movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Send player position to the server
    player_data = {'x': player_x, 'y': player_y}
    client_socket.send(pickle.dumps(player_data))

    # Receive the game state (positions of all players)
    game_state = client_socket.recv(1024)
    players = pickle.loads(game_state)

    # Draw all players (for this example, we draw all players as rectangles)
    for player_address, player_info in players.items():
        pygame.draw.rect(screen, player_color, (player_info['x'], player_info['y'], player_size, player_size))

    pygame.display.flip()
    clock.tick(30)

# Close the connection when done
client_socket.close()
pygame.quit()