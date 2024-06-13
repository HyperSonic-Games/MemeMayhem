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

# Example usage:
if __name__ == "__main__":
    pm = PopupManager()
    pm.Warning("Warning Title", "This is a warning message.")
    pm.Info("Info Title", "This is an info message.")
    pm.Error("Error Title", "This is an error message.")
    user_input = pm.TextInput("Input Needed", "Please enter some text:")
    if user_input is not None:
        print("User input:", user_input)
    else:
        print("No input provided.")
