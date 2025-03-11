import ctypes
import tkinter as tk
from tkinter import messagebox, simpledialog
import platform

# DEV MODE
DEV_MODE = True

class PopupManager:
    def __init__(self):
        self.os_name = platform.system()
        if self.os_name != "Windows":
            self.root = tk.Tk()
            self.root.withdraw()  # Hide the root window

        if DEV_MODE:
            print(f"[DEBUG] PopupManager initialized on {self.os_name}")

    def _windows_messagebox(self, title: str, text: str, icon: str) -> None:
        """Show a Windows native message box using ctypes."""
        icons = {
            "info": 0x40,     # MB_ICONINFORMATION
            "warning": 0x30,  # MB_ICONWARNING
            "error": 0x10     # MB_ICONERROR
        }
        result = ctypes.windll.user32.MessageBoxW(0, text, title, icons.get(icon, 0))
        
        if DEV_MODE:
            print(f"[DEBUG] Windows MessageBox ({icon}) -> Title: '{title}', Text: '{text}', Result: {result}")

    def Warning(self, Title: str, Text: str) -> None:
        """Show a warning message box."""
        if DEV_MODE:
            print(f"[DEBUG] Warning: {Title} - {Text}")

        if self.os_name == "Windows":
            self._windows_messagebox(Title, Text, "warning")
        else:
            messagebox.showwarning(Title, Text)

    def Info(self, Title: str, Text: str) -> None:
        """Show an info message box."""
        if DEV_MODE:
            print(f"[DEBUG] Info: {Title} - {Text}")

        if self.os_name == "Windows":
            self._windows_messagebox(Title, Text, "info")
        else:
            messagebox.showinfo(Title, Text)

    def Error(self, Title: str, Text: str) -> None:
        """Show an error message box."""
        if DEV_MODE:
            print(f"[DEBUG] Error: {Title} - {Text}")

        if self.os_name == "Windows":
            self._windows_messagebox(Title, Text, "error")
        else:
            messagebox.showerror(Title, Text)

    def TextInput(self, Title: str, Prompt: str) -> str | None:
        """Prompt the user for text input."""
        if DEV_MODE:
            print(f"[DEBUG] TextInput Prompt: {Title} - {Prompt}")

        return simpledialog.askstring(Title, Prompt)
