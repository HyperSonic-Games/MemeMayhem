import os
import enum
import toml
import Utils
import Config


class WeponType(enum.Enum):
    AUTOMATIC = 0
    ONE_USE = 1
    MELEE = 2


class Wepon:
    """
    Represents a weapon with properties used in gameplay mechanics.

    Attributes:
        name (str): Display name of the weapon (e.g., "Автомат Калашникова").
        reload_time (int): Time to reload in seconds.
        mag_size (int): Number of bullets per magazine.
        base_shot_damage (int): Damage dealt to body.
        can_headshot (bool): True if headshot damage is enabled.
        head_shot_damage (int): Damage dealt to head.
        range (int): Effective range in pixels before damage falloff starts.
        type (WeponType): Weapon type (Automatic, One-use, Melee).
    """
    def __init__(self):
        self._name: str = ""
        self._reload_time: int = 0
        self._mag_size: int = 0
        self._base_shot_damage: int = 0
        self._can_headshot: bool = True
        self._head_shot_damage: int = 0
        self._range: int = 0
        self._type: WeponType = WeponType.AUTOMATIC

    def get_name(self):
        return self._name

    def set_name(self, value: str):
        self._name = value

    def get_reload_time(self):
        return self._reload_time

    def set_reload_time(self, value: int):
        self._reload_time = value

    def get_mag_size(self):
        return self._mag_size

    def set_mag_size(self, value: int):
        self._mag_size = value

    def get_base_shot_damage(self):
        return self._base_shot_damage

    def set_base_shot_damage(self, value: int):
        self._base_shot_damage = value

    def get_can_headshot(self):
        return self._can_headshot

    def set_can_headshot(self, value: bool):
        self._can_headshot = value

    def get_head_shot_damage(self):
        return self._head_shot_damage

    def set_head_shot_damage(self, value: int):
        self._head_shot_damage = value

    def get_range(self):
        return self._range

    def set_range(self, value: int):
        self._range = value

    def get_type(self):
        return self._type

    def set_type(self, value: WeponType):
        self._type = value
    
    def get_image_path(self, base_dir: str = "Assets/Images/Weapons") -> str | None:
        """
        Returns the image path for the weapon based on its name.
        Supports Pygame-compatible formats. Returns None if no match is found.
        """
        supported_exts = [".png", ".jpg", ".jpeg", ".bmp"]
        base_name = self._name.lower().replace(" ", "_")

        for ext in supported_exts:
            file_path = os.path.join(base_dir, base_name + ext)
            if os.path.isfile(file_path):
                return file_path

        return None

