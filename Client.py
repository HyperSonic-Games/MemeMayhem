from twisted.internet import reactor, protocol
import Utils
import pygame

CLIENT_STARTING_INFO = {"ClientID": "", "x": 0, "y": 0, "hp": 100, "Guns": [None], "EquippedGun": None}





class GameClientProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server")
        # sending initial state to the server TODO: Make This Work With Spawning
        self.send_state(CLIENT_STARTING_INFO)

    def dataReceived(self, data):
        print("Received data:", data.decode())
        # Process received data from the server
        pass

    def send_state(self, state):
        data = self.dict_to_bytes(state)
        self.transport.write(data)

    def dict_to_bytes(self, data_dict):
        # Convert Python dictionary to bytes
        data_str = ""
        for key, value in data_dict.items():
            data_str += f"{key}:{value};"
        return data_str.encode()

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
        pass
        



class Game:
    def __init__(self):
        pygame.init()
        self.PygameWindowContext = pygame.display
        pygame.display.toggle_fullscreen()
        



pm = Utils.PopupManager()
pm.TextInput("Enter Your Name", "Name: ")

# Connect to the server
reactor.connectTCP("localhost", 31425, GameClientFactory())
reactor.run()
