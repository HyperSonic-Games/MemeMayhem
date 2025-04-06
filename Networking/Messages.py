from enum import Enum

class MessageType(Enum):
    # Connection-related messages
    CONN_ACK = 0       # Acknowledgment of a connection request
    CONN_REQ = 1       # Connection request from client
    
    # Authentication messages
    AUTH_REQ = 2       # Authentication request (e.g., login)
    AUTH_SUCCESS = 3   # Authentication successful
    AUTH_FAIL = 4      # Authentication failed

    # General data exchange
    DATA_REQ = 5       # Request for data from the server
    DATA_RESP = 6      # Response containing requested data
    DATA_PUSH = 7      # Server pushes data to the client

    # Error handling
    ERROR = 8          # General error message

    # Heartbeat and keep-alive
    PING = 9           # Client sends heartbeat
    PONG = 10          # Server responds to heartbeat
    
    # Disconnection
    DISCONNECT = 11    # Request to terminate connection
    DISCONNECT_ACK = 12 # Acknowledgment of disconnection

# HEADERS

# Player actions
CLIENT_POS_UPDATE = "CLIENT_POS_UPDATE"     # Player position update
PLAYER_SHOOT = "PLAYER_SHOOT"               # Player fired a weapon
PLAYER_HIT = "PLAYER_HIT"                   # Player hit another player
PLAYER_DEATH = "PLAYER_DEATH"               # Player died
PLAYER_RESPAWN = "PLAYER_RESPAWN"           # Player respawned
PLAYER_INTERACT = "PLAYER_INTERACT"         # Player interacted with an object
PLAYER_SCORE_UPDATE = "PLAYER_SCORE_UPDATE" # Player score update

# Chat & Messaging
CHAT_MESSAGE = "CHAT_MESSAGE"               # Player sends a chat message
PRIVATE_MESSAGE = "PRIVATE_MESSAGE"         # Private message between players
SYSTEM_MESSAGE = "SYSTEM_MESSAGE"           # Server/system-wide message

# Game events
ROUND_START = "ROUND_START"                 # Start of a game round
ROUND_END = "ROUND_END"                     # End of a game round
PLAYER_KILL = "PLAYER_KILL"                 # A player got a kill
OBJECTIVE_COMPLETED = "OBJECTIVE_COMPLETED" # Player/team completed an objective

# Server control
ADMIN_BAN = "ADMIN_BAN"                     # Admin bans a player
ADMIN_KICK = "ADMIN_KICK"                   # Admin kicks a player
SERVER_KICK = "SERVER_KICK"                 # Server auto-kicks a player
SERVER_SHUTDOWN = "SERVER_SHUTDOWN"         # Server is shutting down

# Miscellaneous
HEARTBEAT_PROTOCOL = "HEARTBEAT_PROTOCOL"   # Heartbeat check
LATENCY_CHECK = "LATENCY_CHECK"             # Ping-pong latency check
DEBUG_INFO = "DEBUG_INFO"                   # Debugging information

