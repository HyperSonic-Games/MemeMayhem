import Utils
import Config
import pypresence
from NetCode.Networking import UDPServer

# Constant: VERSION
# The current version of the Meme Mayhem server.
VERSION = "0.0.1-alpha"

# Constant: DISCORD_APP_CLIENT_ID
# The Client ID used for Discord RPC (Rich Presence) integration.
DISCORD_APP_CLIENT_ID = "1349055429304520734"

# Initialize PopupManager
pm = Utils.PopupManager()

# Initialize Discord RPC if Discord is installed
if Utils.IsDiscordAppInstalled():
    try:
        RPC = pypresence.Presence(DISCORD_APP_CLIENT_ID)
        RPC.connect()
        RPC.update(state="Running a Meme Mayhem Server")
        Utils.debug_log("DISCORD", "Discord RPC Connected and Presence Set")
    except Exception as e:
        Utils.error_log("DISCORD", f"Failed to initialize Discord RPC: {e}")

# Constant: DEV_MODE
# Flag indicating whether the server is in development mode.
DEV_MODE = Config.DEV_MODE

# Function: server_msg_parser
# Parses incoming server messages from clients.
#
# Parameters:
#     data - Raw data (bytes) from the client.
#
# Returns:
#     dict or None - A dictionary with parsed message content or None if parsing failed.
#
# Notes:
#     This is a placeholder function; it can be replaced with actual message parsing logic.
def server_msg_parser(data: bytes) -> dict | None:
    try:
        # Simple placeholder logic: decode bytes as UTF-8 and return as message dictionary
        return {'message': data.decode('utf-8')}
    except Exception as e:
        print(f"[MEME_MAYHEM/SERVER]: <SERVER_PARSER_FUNC_ERR> Parse error: {e}")
        return None

# Constant: SERVER_HEADER
# ASCII art logo for the Meme Mayhem server, displayed on server startup.
SERVER_HEADER: str = """
███████████████             █████████████          ██████████████             ███████████████       
███▓▓▓▓▓▓▓▓▓█████           ██▓▓▓▓▓▓▓▓▓█████       ██▓▓▓▓▓▓▓▓▓██████          ███▓▓▓▓▓▓▓▓██████     
███▓▓▓▓▓▓▓▓▓███████    ▓▓▓▓▓██▓▓▓▓▓▓▓▓▓███████     ██▓▓▓▓▓▓▓▓▓████████   ▓▓▓▓▓███▓▓▓▓▓▓▓▓████████   
███▓▓▓▓▓▓▓▓▓██████████████████▓▓▓▓▓▓▓▓▓█████████   ██▓▓▓▓▓▓▓▓▓█████████  ████████▓▓▓▓▓▓▓▓██████████ 
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓███████▓▓▓▓███████▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓████████▓▓▓████████▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓███████▓▓▓▓███████▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓████████▓▓▓████████▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓███████▓▓▓▓███████▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓████████▓▓▓████████▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓██████████████████▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓███████████████████▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓██████████████████▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓███████████████████▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓██████████████████▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓███████████████████▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓██████████████████▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓███████████████████▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓███████████ ██████▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓███████████  ██████▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓███████████     ██▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓███████████     ███▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓███████████     ██▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓███████████     ███▓▓▓▓▓▓▓▓███████████
███▓▓▓▓▓▓▓▓▓▓▓▓███████████     ██▓▓▓▓▓▓▓▓▓██████████  ██▓▓▓▓▓▓▓▓▓███████████     ███▓▓▓▓▓▓▓▓███████████
███████████████████████     █████████████████████  ██████████████████████     ██████████████████████
 ██████████████████████     █████████████████████  ██████████████████████      █████████████████████
   ████████████████████      ████████████████████    ████████████████████        ███████████████████
    ███████████████████        ██████████████████      ██████████████████         ██████████████████
      █████████████████          ████████████████        ████████████████           ████████████████
         █████████████             ██████████████          █████████████              ██████████████
"""

# Color formatting for terminal output
RED = "\033[91m"
RESET = "\033[0m"

# Display the server header logo
print(f"{RED}{SERVER_HEADER}{RESET}")

# Constant: SERVER_MAX_PLAYERS
# The maximum number of players allowed on the server at a time.
# Changing this value could impact server stability.
SERVER_MAX_PLAYERS = 15
