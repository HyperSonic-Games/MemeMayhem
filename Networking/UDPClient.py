import socket
import time
from enum import Enum
from Serializer import Serializer
import Messages


# Helper function for LERP interpolation
def Lerp(Start, End, T):
    return (Start[0] + T * (End[0] - Start[0]), Start[1] + T * (End[1] - Start[1]))


# Helper function for Dead Reckoning prediction
def DeadReckon(LastPosition, Velocity, TimeDelta):
    NewX = LastPosition[0] + Velocity[0] * TimeDelta
    NewY = LastPosition[1] + Velocity[1] * TimeDelta
    return (NewX, NewY)


class UdpClient:
    def __init__(self, serverAddress: tuple, msgHandler: callable, timeDelta: float = 0.1):
        """
        Initialize the UDP client with the server address, message handler, and other parameters.

        Args:
        - serverAddress (tuple): Address and port of the server.
        - msgHandler (callable): A function to handle incoming server messages.
        - timeDelta (float): Time step (in seconds) between updates.
        """
        self.ServerAddress = serverAddress
        self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
        self.LastPosition = (0, 0)
        self.Velocity = (1, 1)  # Example velocity (dx, dy)
        self.TimeDelta = timeDelta
        self.MsgHandler = msgHandler

    def SendPositionToServer(self, position, velocity):
        """
        Send the current player's position to the server.
        """
        message = {
            'type': Messages.MessageType.DATA_PUSH.name,  # Use enum name for message type
            'position': position,
            'velocity': velocity
        }
        # Serialize and send the message
        packet = Serializer.Serialize(message)
        self.ClientSocket.sendto(packet, self.ServerAddress)

    def ReceiveData(self):
        """
        Receive data from the server and pass it to the message handler.
        """
        data, server = self.ClientSocket.recvfrom(4096)  # Receive server's response
        receivedData = Serializer.Deserialize(data)
        self.MsgHandler(receivedData)  # Pass the received data to the handler function

    def Run(self):
        """
        Run the UDP client. This sends positions to the server and handles responses.
        """
        while True:
            # Step 1: Predict the position of the player (Dead Reckoning)
            predictedPosition = DeadReckon(self.LastPosition, self.Velocity, self.TimeDelta)

            # Step 2: Send current predicted position to the server
            self.SendPositionToServer(predictedPosition, self.Velocity)

            # Step 3: Receive server's position update and handle it with the custom handler
            self.ReceiveData()

            # Step 4: Sleep for the next frame (simulate the game loop)
            time.sleep(self.TimeDelta)