import socket
import time
from enum import Enum
from . import Serializer
from . import Messages


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
        self.TimeDelta = timeDelta
        self.MsgHandler = msgHandler
        self.serializer = Serializer.Serializer()

    def ReceiveData(self):
        """
        Receive data from the server and pass it to the message handler.
        """
        data, server = self.ClientSocket.recvfrom(4096)  # Receive server's response
        receivedData = self.serializer.deserialize(data)
        self.MsgHandler(receivedData)  # Pass the received data to the handler function

    def SendData(self, data):
        """
        Send data to the server.

        Args:
        - data: Data to send (can be any object that can be serialized).
        """
        serializedData = self.serializer.serialize(data)  # Serialize the data
        self.ClientSocket.sendto(serializedData, self.ServerAddress)  # Send data to the server

    def Run(self):
        """
        Run the UDP client. This listens for incoming server messages and handles them.
        """
        while True:
            self.ReceiveData()  # Receive any incoming data from the server
            time.sleep(self.TimeDelta)  # Wait for the next cycle