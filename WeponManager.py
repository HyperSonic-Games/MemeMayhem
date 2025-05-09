import os
import enum
import toml
import Utils
import Config

# Class: WeponType
# Represents the category/type of a weapon.
#
# Enum Values:
#     AUTOMATIC - Weapon that fires continuously while held.
#     ONE_USE   - Weapon that is used once, like grenades.
#     MELEE     - Close-range physical weapons like bats or knives.
class WeponType(enum.Enum):
    AUTOMATIC = 0
    ONE_USE = 1
    MELEE = 2


# Class: Wepon
# Represents a game weapon, loaded from asset files or defined in code.
#
# This class is used to configure weapons with properties like damage, type,
# headshot ability, and more. It can be extended or manipulated by modders.
#
# Usage:
#     Create a new weapon instance, set its properties, or load them from a .toml file.
#
# Example:
#     weapon = Wepon()
#     weapon.set_name("MooseysAntlers")
#     weapon.set_type(WeponType.MELEE)
#
# Attributes:
#     name - Display name of the weapon (e.g., "Автомат Калашникова").
#     reload_time - Time to reload in seconds.
#     mag_size - Number of bullets in each magazine.
#     base_shot_damage - Damage dealt on body shot.
#     can_headshot - Whether headshots apply extra damage.
#     head_shot_damage - Damage dealt on headshot.
#     range - Effective range in pixels.
#     type - Type of weapon from WeponType enum.
class Wepon:
    def __init__(self):
        self._name: str = ""
        self._reload_time: int = 0
        self._mag_size: int = 0
        self._base_shot_damage: int = 0
        self._can_headshot: bool = True
        self._head_shot_damage: int = 0
        self._range: int = 0
        self._type: WeponType = WeponType.AUTOMATIC

    # Function: get_name
    # Returns the weapon's display name.
    def get_name(self):
        return self._name

    # Function: set_name
    # Sets the weapon's display name.
    def set_name(self, value: str):
        self._name = value

    # Function: get_reload_time
    # Returns the weapon's reload time in seconds.
    def get_reload_time(self):
        return self._reload_time

    # Function: set_reload_time
    # Sets the reload time in seconds.
    def set_reload_time(self, value: int):
        self._reload_time = value

    # Function: get_mag_size
    # Returns the number of bullets per magazine.
    def get_mag_size(self):
        return self._mag_size

    # Function: set_mag_size
    # Sets the number of bullets per magazine.
    def set_mag_size(self, value: int):
        self._mag_size = value

    # Function: get_base_shot_damage
    # Returns the base body shot damage.
    def get_base_shot_damage(self):
        return self._base_shot_damage

    # Function: set_base_shot_damage
    # Sets the base body shot damage.
    def set_base_shot_damage(self, value: int):
        self._base_shot_damage = value

    # Function: get_can_headshot
    # Returns whether headshots are enabled for this weapon.
    def get_can_headshot(self):
        return self._can_headshot

    # Function: set_can_headshot
    # Enables or disables headshot capability.
    def set_can_headshot(self, value: bool):
        self._can_headshot = value

    # Function: get_head_shot_damage
    # Returns the headshot damage.
    def get_head_shot_damage(self):
        return self._head_shot_damage

    # Function: set_head_shot_damage
    # Sets the damage dealt on headshots.
    def set_head_shot_damage(self, value: int):
        self._head_shot_damage = value

    # Function: get_range
    # Returns the effective range of the weapon in pixels.
    def get_range(self):
        return self._range

    # Function: set_range
    # Sets the effective range in pixels.
    def set_range(self, value: int):
        self._range = value

    # Function: get_type
    # Returns the weapon type as a WeponType enum.
    def get_type(self):
        return self._type

    # Function: set_type
    # Sets the weapon type.
    def set_type(self, value: WeponType):
        self._type = value

    # Function: get_image_path
    # Returns the image file path for the weapon icon.
    #
    # Parameters:
    #     base_dir - Path to the image directory. Defaults to "Assets/Images/Weapons".
    #
    # Returns:
    #     str - Full path to the image if found, otherwise None.
    #
    # Notes:
    #     The image file is matched by name, replacing spaces with underscores,
    #     and searched for in common formats like .png and .jpg.
    def get_image_path(self, base_dir: str = "Assets/Images/Weapons") -> str | None:
        supported_exts = [".png", ".jpg", ".jpeg", ".bmp"]
        base_name = self._name.lower().replace(" ", "_")

        for ext in supported_exts:
            file_path = os.path.join(base_dir, base_name + ext)
            if os.path.isfile(file_path):
                return file_path

        return None
