import pygame
import pygame_gui
import toml
import Utils

def RenderSettingsGui():
    ScreenWidth = 800
    ScreenHeight = 600
    pygame.init()
    Screen = pygame.display
    Screen.init()
    Screen.set_caption()
    Screen.set_mode((ScreenWidth, ScreenHeight))
    GuiManager = pygame_gui.UI
