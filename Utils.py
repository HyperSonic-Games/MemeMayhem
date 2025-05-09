import ctypes
import tkinter as tk
from tkinter import messagebox, simpledialog
import platform
import os
import sys
import shutil

import Config

# Constant: DEV_MODE
# Flag indicating whether the program is running in development mode.
# Affects logging and error handling behavior.
Config.DEV_MODE


# Group: Logging Functions
# Functions to log debug, warning, and error messages conditionally based on DEV_MODE.


# Function: debug_log
# Logs a debug message if DEV_MODE is enabled.
#
# Parameters:
#     tag - A short label identifying the source.
#     message - The message to display.
def debug_log(tag, message):
    if Config.DEV_MODE:
        print(f"[DEBUG/{tag}] {message}")


# Function: warn_log
# Logs a warning message. In dev mode, prints to console; otherwise shows a popup.
#
# Parameters:
#     tag - Source tag.
#     message - Warning text.
def warn_log(tag, message):
    if Config.DEV_MODE:
        print(f"[WARN/{tag}] {message}")
    else:
        pm = PopupManager(no_init_msg=True)
        pm.Warning(tag, message)


# Function: error_log
# Logs an error message. In dev mode, prints to console; otherwise shows a popup.
#
# Parameters:
#     tag - Source tag.
#     message - Error text.
def error_log(tag, message):
    if Config.DEV_MODE:
        print(f"[ERROR/{tag}] {message}")
    else:
        pm = PopupManager(no_init_msg=True)
        pm.Error(tag, message)


# Function: IsDiscordAppInstalled
# Checks if a Discord client is installed on the current system.
#
# Returns:
#     bool - True if found, False otherwise.
#
# Notes:
#     Searches standard install paths for Windows, Linux, and macOS.
def IsDiscordAppInstalled() -> bool:
    if sys.platform.startswith("win"):
        discord_paths = [
            os.path.join(os.getenv("LOCALAPPDATA", ""), "Discord"),
            os.path.join(os.getenv("LOCALAPPDATA", ""), "DiscordCanary"),
            os.path.join(os.getenv("LOCALAPPDATA", ""), "DiscordPTB"),
        ]
        return any(os.path.exists(path) for path in discord_paths)

    elif sys.platform.startswith("linux"):
        return any(os.path.exists(path) for path in [
            "/usr/bin/discord",
            "/snap/bin/discord",
            os.path.expanduser("~/.local/bin/discord"),
        ]) or shutil.which("discord") is not None

    elif sys.platform.startswith("darwin"):
        discord_paths = [
            "/Applications/Discord.app",
            "/Applications/Discord Canary.app",
            "/Applications/Discord PTB.app"
        ]
        return any(os.path.exists(path) for path in discord_paths)

    return False


# Class: PopupManager
# Handles GUI popups for errors, warnings, and messages.
#
# Platform-specific implementation: Uses Windows native message boxes via ctypes,
# and tkinter on other systems.
#
# Constructor Parameters:
#     no_init_msg - If True, disables the initialization debug message.
class PopupManager:
    def __init__(self, no_init_msg=False):
        self.os_name = platform.system()
        if self.os_name != "Windows":
            self.root = tk.Tk()
            self.root.withdraw()
            if not no_init_msg:
                debug_log("PopupManager", f"Initialized on {self.os_name}")

    # Function: _windows_messagebox
    # Internal function to show a native Windows message box.
    #
    # Parameters:
    #     title - Title of the popup.
    #     text - Message body.
    #     icon - One of "info", "warning", or "error".
    def _windows_messagebox(self, title: str, text: str, icon: str) -> None:
        icons = {
            "info": 0x40,     # MB_ICONINFORMATION
            "warning": 0x30,  # MB_ICONWARNING
            "error": 0x10     # MB_ICONERROR
        }
        ctypes.windll.user32.MessageBoxW(0, text, title, icons.get(icon, 0))

    # Function: Warning
    # Displays a warning popup.
    def Warning(self, Title: str, Text: str) -> None:
        if self.os_name == "Windows":
            self._windows_messagebox(Title, Text, "warning")
        else:
            messagebox.showwarning(Title, Text)

    # Function: Info
    # Displays an info popup.
    def Info(self, Title: str, Text: str) -> None:
        if self.os_name == "Windows":
            self._windows_messagebox(Title, Text, "info")
        else:
            messagebox.showinfo(Title, Text)

    # Function: Error
    # Displays an error popup.
    def Error(self, Title: str, Text: str) -> None:
        if self.os_name == "Windows":
            self._windows_messagebox(Title, Text, "error")
        else:
            messagebox.showerror(Title, Text)

    # Function: TextInput
    # Opens a simple text input dialog and returns the user's input.
    #
    # Parameters:
    #     Title - Window title.
    #     Prompt - Prompt text.
    #
    # Returns:
    #     str - The input string or None if canceled.
    def TextInput(self, Title: str, Prompt: str) -> str | None:
        return simpledialog.askstring(Title, Prompt)
