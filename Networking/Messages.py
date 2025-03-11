from enum import Enum

class MessageType(Enum):
    # Connection-related messages
    CONN_ACK = 0      # Acknowledgment of a connection request
    CONN_REQ = 1      # Connection request from client
    
    # Authentication messages
    AUTH_REQ = 2      # Authentication request (e.g., login)
    AUTH_SUCCESS = 3  # Authentication successful
    AUTH_FAIL = 4     # Authentication failed

    # General data exchange
    DATA_REQ = 5      # Request for data from the server
    DATA_RESP = 6     # Response containing requested data
    DATA_PUSH = 7     # Server pushes data to the client

    # Error handling
    ERROR = 8         # General error message

    # Heartbeat and keep-alive
    PING = 9          # Client sends heartbeat
    PONG = 10         # Server responds to heartbeat
    
    # Disconnection
    DISCONNECT = 11   # Request to terminate connection
    DISCONNECT_ACK = 12 # Acknowledgment of disconnection


