import pyautogui
import pygame

# Class to manage popup messages using pyautogui
class PopupManager:

    def Warning(self, Title, Text):
        # Show a warning message box
        # Arguments:
        #   Title (str): The title of the warning message box.
        #   Text (str): The text content of the warning message.
        pyautogui.alert(text=Text, title=Title, button='OK')

    def Info(self, Title, Text):
        # Show an info message box
        # Arguments:
        #   Title (str): The title of the info message box.
        #   Text (str): The text content of the info message.
        pyautogui.alert(text=Text, title=Title, button='OK')
    
    def Error(self, Title, Text):
        # Show an error message box
        # Arguments:
        #   Title (str): The title of the error message box.
        #   Text (str): The text content of the error message.
        pyautogui.alert(text=Text, title=Title, button='OK',)
    
    def TextInput(self, Title, Prompt) -> str:
        # Prompt the user for text input
        # Arguments:
        #   Title (str): The title of the text input prompt.
        #   Prompt (str): The text prompt asking for user input.
        # Returns:
        #   str: The user's input as a string.
        return pyautogui.prompt(text=Prompt, title=Title, default='')





# A dictionary mapping string key values to pygame key constants
KEY_MAP = {
    # Letters
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z,

    # Numbers
    "0": pygame.K_0,
    "1": pygame.K_1,
    "2": pygame.K_2,
    "3": pygame.K_3,
    "4": pygame.K_4,
    "5": pygame.K_5,
    "6": pygame.K_6,
    "7": pygame.K_7,
    "8": pygame.K_8,
    "9": pygame.K_9,

    # Function Keys
    "F1": pygame.K_F1,
    "F2": pygame.K_F2,
    "F3": pygame.K_F3,
    "F4": pygame.K_F4,
    "F5": pygame.K_F5,
    "F6": pygame.K_F6,
    "F7": pygame.K_F7,
    "F8": pygame.K_F8,
    "F9": pygame.K_F9,
    "F10": pygame.K_F10,
    "F11": pygame.K_F11,
    "F12": pygame.K_F12,

    # Arrow Keys
    "Up": pygame.K_UP,
    "Down": pygame.K_DOWN,
    "Left": pygame.K_LEFT,
    "Right": pygame.K_RIGHT,

    # Special Keys
    "Space": pygame.K_SPACE,
    "Enter": pygame.K_RETURN,
    "Shift": pygame.K_LSHIFT,
    "Ctrl": pygame.K_LCTRL,
    "Alt": pygame.K_LALT,
    "Tab": pygame.K_TAB,
    "Backspace": pygame.K_BACKSPACE,
    "Esc": pygame.K_ESCAPE,

    # Mouse Buttons
    "LMB": pygame.BUTTON_LEFT,    # Left Mouse Button
    "RMB": pygame.BUTTON_RIGHT,   # Right Mouse Button
    "MMB": pygame.BUTTON_MIDDLE,  # Middle Mouse Button
}

def TranslateToPygameKey(key_str):
    """
    Translate a key string from settings into the corresponding Pygame key constant.
    
    Args:
        key_str (str): The key as a string from the settings (e.g., "w", "a", "LMB").
    
    Returns:
        int: The corresponding Pygame key constant (e.g., pygame.K_w), or None if not found.
    """
    return KEY_MAP.get(key_str, None)  # Return None if the key is not found
