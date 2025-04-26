import ctypes
import tkinter as tk
from tkinter import messagebox, simpledialog
import platform
import os
import sys
import shutil

import Config

# DEV MODE
DEV_MODE = Config.DEV_MODE


# Check if discord is installed
def IsDiscordAppInstalled() -> bool:
    """Check if the Discord application is installed based on the OS."""
    if sys.platform.startswith("win"):
        # Windows: Check the LocalAppData directory for Discord
        discord_paths = [
            os.path.join(os.getenv("LOCALAPPDATA", ""), "Discord"),
            os.path.join(os.getenv("LOCALAPPDATA", ""), "DiscordCanary"),
            os.path.join(os.getenv("LOCALAPPDATA", ""), "DiscordPTB"),
        ]
        return any(os.path.exists(path) for path in discord_paths)

    elif sys.platform.startswith("linux"):
        # Linux: Check common locations or use `shutil.which`
        return any(os.path.exists(path) for path in [
            "/usr/bin/discord",
            "/snap/bin/discord",
            os.path.expanduser("~/.local/bin/discord"),
        ]) or shutil.which("discord") is not None

    elif sys.platform.startswith("darwin"):
        # macOS: Check the Applications folder
        discord_paths = [
            "/Applications/Discord.app",
            "/Applications/Discord Canary.app",
            "/Applications/Discord PTB.app"
        ]
        return any(os.path.exists(path) for path in discord_paths)

    return False  # Unknown platform


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
