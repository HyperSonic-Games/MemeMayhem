import toml
import pygame
import os
import Config
import sys

# Import PopupManager for error messages
import Utils



# Initialize PopupManager
popup = Utils.PopupManager()



class SettingsManager:
    MOUSE_MAPPING = {
        "LMB": pygame.BUTTON_LEFT,
        "RMB": pygame.BUTTON_RIGHT,
        "MMB": pygame.BUTTON_MIDDLE
    }

    def __init__(self, PathToTomlConfigFile: os.PathLike):
        self.TomlPath: os.PathLike = PathToTomlConfigFile
        self.config = self._LoadConfig()

   
    def _LoadConfig(self):
        """
        INTERNAL FUNCTION DO NOT USE
        """
        if not os.path.exists(self.TomlPath):
            self._handle_error("Config file not found", f"Could not locate: {self.TomlPath}")
            return {}

        return toml.load(self.TomlPath) # type: ignore

    def _handle_error(self, title: str, message: str):
        """
        INERNAL DO NOT USE
        Handles errors based on DEV_MODE setting.
        """
        Utils.error_log(title, message)
        sys.exit(-1)

    def _get_player_settings(self, key_name: str, default: str):
        """-
        INERNAL DO NOT USE
        Fetch a key from the config and convert it to a pygame key constant or mouse button.
        Logs errors if an invalid key is used and falls back to default.
        """
        key_str = self.config.get("PLAYER", {}).get(key_name, default)

    def _get_key_code(self, key_name: str, default: str) -> int:
        """-
        INERNAL DO NOT USE
        Fetch a key from the config and convert it to a pygame key constant or mouse button.
        Logs errors if an invalid key is used and falls back to default.
        """
        key_str = self.config.get("CONTROLS", {}).get(key_name, default)

        # Check if it's a mouse button
        if key_str in self.MOUSE_MAPPING:
            return self.MOUSE_MAPPING[key_str]

        # Otherwise, assume it's a keyboard key
        try:
            return pygame.key.key_code(key_str)
        except ValueError:
            self._handle_error("Invalid Key Binding", f"'{key_str}' is not a valid key for '{key_name}'. Using default '{default}' instead.")
            return pygame.key.key_code(default)

    def GetControls_MoveUp(self) -> int:
        return self._get_key_code("MoveUp", "w")

    def GetControls_MoveDown(self) -> int:
        return self._get_key_code("MoveDown", "s")

    def GetControls_MoveLeft(self) -> int:
        return self._get_key_code("MoveLeft", "a")

    def GetControls_MoveRight(self) -> int:
        return self._get_key_code("MoveRight", "d")

    def GetControls_FireWeapon(self) -> int:
        return self._get_key_code("FireWeapon", "LMB")

    def GetControls_ReloadWeapon(self) -> int:
        return self._get_key_code("ReloadWeapon", "r")

    def GetRendering_VSync(self) -> bool:
        return self.config.get("RENDERING", {}).get("VSync", False)

    def GetRendering_Fullscreen(self) -> bool:
        return self.config.get("RENDERING", {}).get("Fullscreen", False)
