import threading
from twisted.internet import reactor, protocol
import pygame
import Utils
import sys
import toml

ServerData = []

CLIENT_STARTING_INFO = {"ClientID": "", "x": 0, "y": 0, "hp": 100, "Guns": [None], "EquippedGun": None}

class GameClientProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server")
        # sending initial state to the server
        self.send_state(CLIENT_STARTING_INFO)

    def dataReceived(self, data):
        global ServerData
        decoded_data = data.decode()
        try:
            # Parse TOML data received from the server
            ServerData = toml.loads(decoded_data)
            print(f"Received data from server: {ServerData}")
        except Exception as e:
            print(f"Error decoding server data: {e}")

    def send_state(self, state):
        data = self.dict_to_toml(state)
        self.transport.write(data.encode())

    def dict_to_toml(self, data_dict):
        # Convert Python dictionary to TOML string
        return toml.dumps(data_dict)

class GameClientFactory(protocol.ClientFactory):
    protocol = GameClientProtocol

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

class Player:
    def __init__(self, ImagePath):
        self.Guns = []
        self.EquippedGun = ""
        self.PlayerSprite = pygame.image.load(ImagePath)
        self.rect = self.PlayerSprite.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def render(self, screen):
        screen.blit(self.PlayerSprite, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Your Game Title")

        self.screen_width = 800
        self.screen_height = 600
        self.PygameWindowContext = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Load player and initialize its position
        self.player = Player("Assets/Images/Player/Blue.png")
        self.player.update(self.screen_width // 2, self.screen_height // 2)  # Center player initially

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # Clear the screen
            self.PygameWindowContext.fill((0, 0, 0))

            # Render the player
            self.player.render(self.PygameWindowContext)

            # Render other clients
            for client_data in ServerData:
                if client_data["ClientID"] != CLIENT_STARTING_INFO["ClientID"]:  # Exclude own client
                    x = client_data.get("x", 0)
                    y = client_data.get("y", 0)
                    # Render other clients assuming they have a sprite or representation
                    pygame.draw.circle(self.PygameWindowContext, (255, 0, 0), (x, y), 20)

            pygame.display.flip()
            clock.tick(60)  # Limit frame rate to 60 FPS

    def start_networking(self):
        reactor.connectTCP("localhost", 31425, GameClientFactory())
        reactor.run(installSignalHandlers=0)

def run_game_and_networking():
    game = Game()
    networking_thread = threading.Thread(target=game.start_networking)
    networking_thread.start()
    game.run()

if __name__ == "__main__":
    pm = Utils.PopupManager()
    name = pm.TextInput("Enter Your Name", "Name: ")
    CLIENT_STARTING_INFO["ClientID"] = name

    run_game_and_networking()
