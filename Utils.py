import pyautogui

class PopupManager:

    def Warning(self, Title, Text):
        # Show a warning message box
        pyautogui.alert(text=Text, title=Title, button='OK')

    def Info(self, Title, Text):
        # Show an info message box
        pyautogui.alert(text=Text, title=Title, button='OK')
    
    def Error(self, Title, Text):
        # Show an error message box
        pyautogui.alert(text=Text, title=Title, button='OK')
    
    def TextInput(self, Title, Prompt):
        # Prompt the user for text input
        return pyautogui.prompt(text=Prompt, title=Title, default='')

