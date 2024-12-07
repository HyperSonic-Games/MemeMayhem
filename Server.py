import socket
import threading
import pickle

# List to store player data
players = {}

# Function to handle communication with each client
def handle_client(client_socket, client_address):
    global players

    print(f"New connection from {client_address}")
    client_socket.send("Connected to server.".encode())

    player_data = {
        'x': 400,
        'y': 300,
        'health': 100
    }

    # Add the player to the game world
    players[client_address] = player_data

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)

            if not data:
                break

            # Unpickle the data (client sends positions or actions)
            player_input = pickle.loads(data)
            player_data['x'] = player_input.get('x', player_data['x'])
            player_data['y'] = player_input.get('y', player_data['y'])

            # Broadcast the updated game state to all clients
            game_state = pickle.dumps(players)
            for client in players:
                if client != client_address:
                    try:
                        client_socket.send(game_state)
                    except:
                        continue

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        del players[client_address]
        client_socket.close()

# Function to start the server
def start_server():
    host = '127.0.0.1'
    port = 12345

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    start_server()