from twisted.internet import reactor, protocol
import toml

ConnectedClientsDataList = []  # Format: [{"ClientID": "", "x": 0, "y": 0, "hp": 100, "Guns": [None], "EquippedGun": None}] 

class GameServerProtocol(protocol.Protocol):
    def connectionMade(self):
        client_address = self.transport.getPeer()
        print(f"[ServerProtocol : ConnectionMade]: Player connected: {client_address.host}:{client_address.port}")

    def dataReceived(self, data):
        client_address = self.transport.getPeer()
        decoded_data = data.decode()
        print(f"[ServerProtocol : DataReceived]: Received data from {client_address.host}:{client_address.port}: {decoded_data}")
        
        try:
            received_state = toml.loads(decoded_data)  # Parse TOML data into Python dict
            client_id = received_state.get("ClientID", None)
            if client_id is None:
                raise ValueError("Received data does not contain ClientID")
            
            # Find the client data in ConnectedClientsDataList and update it
            for client_data in ConnectedClientsDataList:
                if client_data["ClientID"] == client_id:
                    # Update existing client data with received state
                    client_data.update(received_state)
                    print(f"[ServerProtocol : DataReceived]: Updated state for ClientID {client_id}: {client_data}")
                    break
            else:
                # ClientID not found, create a new entry
                new_client_data = {"ClientID": client_id}
                new_client_data.update(received_state)
                ConnectedClientsDataList.append(new_client_data)
                print(f"[ServerProtocol : DataReceived]: Created new state for ClientID {client_id}: {new_client_data}")

        except Exception as e:
            print(f"Error processing received data: {e}")

    def send_state(self, state):
        data = self.dict_to_toml(state)
        self.transport.write(data.encode())

    def dict_to_toml(self, data_dict):
        # Convert Python dictionary to TOML string
        return toml.dumps(data_dict)

class GameServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return GameServerProtocol()

# Start the server
if __name__ == "__main__":
    print("[Main]: Starting server...")
    reactor.listenTCP(31425, GameServerFactory())
    print("[Main]: Server started and listening on port 31425")
    reactor.run()
