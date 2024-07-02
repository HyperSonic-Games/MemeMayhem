import pyautogui

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
    
    def TextInput(self, Title, Prompt):
        # Prompt the user for text input
        # Arguments:
        #   Title (str): The title of the text input prompt.
        #   Prompt (str): The text prompt asking for user input.
        # Returns:
        #   str: The user's input as a string.
        return pyautogui.prompt(text=Prompt, title=Title, default='')
