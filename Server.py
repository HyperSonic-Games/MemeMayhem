from twisted.internet import reactor, protocol

ConectedClientsDataList = [] # FORMAT: [{"ClientID": "", "x": 0, "y": 0, "hp": 100, "Guns": [None], "EquippedGun": None}] 

class GameServerProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Player connected")

    def dataReceived(self, data):
        print("Received data:", data.decode())
        # Process received data from the client
        self.send_state({"x": 200, "y": 250, "hp": 80})  # Example: sending updated state

    def send_state(self, state):
        data = self.dict_to_bytes(state)
        self.transport.write(data)

    def dict_to_bytes(self, data_dict):
        # Convert Python dictionary to bytes
        data_str = ""
        for key, value in data_dict.items():
            data_str += f"{key}:{value};"
        return data_str.encode()

class GameServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return GameServerProtocol()

# Start the server
reactor.listenTCP(31425, GameServerFactory())
print("Server started")
reactor.run()
