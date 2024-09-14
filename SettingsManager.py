import toml
import enum
from Utils import TranslateToPygameKey  # Import the translation function

class SettingsKeyMap(enum.Enum):
    MoveUp = "MoveUp"
    MoveDown = "MoveDown"
    MoveLeft = "MoveLeft"
    MoveRight = "MoveRight"
    FireWeapon = "FireWeapon"
    ReloadWeapon = "ReloadWeapon"

class RenderingOptions(enum.Enum):
    VSync = "VSync"
    Fullscreen = "Fullscreen"

class SettingsManager:
    def __init__(self, settings_file):
        # Load the settings from the TOML file
        with open(settings_file, "r") as f:
            self.Settings = toml.load(f)

    # Method to get control mappings
    def GetControl(self, control_key):
        control_str = self.Settings["CONTROLS"].get(control_key.value)
        return TranslateToPygameKey(control_str)  # Convert to Pygame key

    # Specific method for MoveUp control
    def GetControlMoveUp(self):
        return self.GetControl(SettingsKeyMap.MoveUp)

    # Method to get rendering options (e.g., VSync, Fullscreen)
    def GetRenderingOption(self, option_key):
        return self.Settings["RENDERING"].get(option_key.value)

    # Specific methods for rendering options
    def GetVSync(self):
        return self.GetRenderingOption(RenderingOptions.VSync)

    def GetFullscreen(self):
        return self.GetRenderingOption(RenderingOptions.Fullscreen)