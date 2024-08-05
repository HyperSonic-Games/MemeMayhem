import pygame 
import pygame_gui
import threading

import Utils
import sys
from SettingsManager import SettingsManager

# Base Game class
class Game:
    UserName = None  # Class-level attribute to store the username
    ServerAddress: str = None  # Class-level attribute to store the server address

    def __init__(self):
        # Get the user's name using a popup input only once
        if Game.UserName is None:
            Game.UserName = Utils.PopupManager().TextInput("Enter Your User Name", "User Name: ")

        # Get the server address using a popup input only once if not provided via command line
        if Game.ServerAddress is None:
            Game.ServerAddress = Utils.PopupManager().TextInput("Enter Server Address", "Server Address: ")

        # Set window properties
        self.WindowWidth = 800
        self.WindowHeight = 600
        self.WindowTitle = "Meme Mayhem"

        # Initialize pygame and setup the display
        pygame.init()
        vsync_setting = SettingsManager("SETTINGS.toml").GetSetting("RENDERING", "VSync")
        if vsync_setting in [True, "True"]:
            self.screen = pygame.display.set_mode((self.WindowWidth, self.WindowHeight), pygame.SCALED, vsync=1)
        else:
            self.screen = pygame.display.set_mode((self.WindowWidth, self.WindowHeight), pygame.SCALED)
        pygame.display.set_caption(self.WindowTitle)

        # Toggle fullscreen mode if possible
        try:
            pygame.display.toggle_fullscreen()
        except pygame.error:
            # If initialization fails, show an error popup and exit
            Utils.PopupManager.Error("Error: Client", "Pygame Display Surface Failed To Initialize")
            pygame.quit()
            exit(1)

    def GetRenderContext(self):
        return self.screen
    
    # Renders The Map And The Rest Of The Clients
    def Render(self):
        pass

# Base class for all GUI components
class GuiComponent:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def Render(self, surface):
        """Draw the component on the given surface."""
        raise NotImplementedError("Render method must be overridden in derived classes.")
    
    def Update(self, time_delta):
        """Update the component's state."""
        raise NotImplementedError("Update method must be overridden in derived classes.")

# Hp Bar Gui Component inheriting from GuiComponent
class HpBar(GuiComponent):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.health = 100

    def SetHealthBarHealthValue(self, health: int):
        self.health = health

    def Render(self, surface):
        # Render the health bar (placeholder rectangle here)
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 100, 20))
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.health, 20))

    def Update(self, time_delta):
        # Placeholder for potential health bar updates
        pass

# Gui class managing GuiComponents, inheriting from Game
class Gui(Game):
    def __init__(self):
        super().__init__()
        self.components = []  # List to store GUI components
    
    def AddComponent(self, component: GuiComponent):
        """Add a GuiComponent to the GUI."""
        self.components.append(component)

    def Render(self):
        """Render all components."""
        for component in self.components:
            component.Render(self.GetRenderContext())

    def Update(self, time_delta):
        """Update all components."""
        for component in self.components:
            component.Update(time_delta)


# Player class inheriting from Game
class Player(Game):
    def __init__(self):
        super().__init__()
    
    def GetHealth(self) -> int:
        # Grab Hp Data From The Server
        pass
    
    
    def Render(self):
        render_context = super().GetRenderContext()

# Main entry point
if __name__ == "__main__":
    game = Game()
    gui = Gui()
    player = Player()

   
    
   
    running = True  # Main loop control variable
    clock = pygame.time.Clock()  # Clock object to control frame rate

    while running:
        time_delta = clock.tick(60) / 1000  # Convert to seconds
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Exit the loop if the Escape key is pressed

        # Render core game elements, player elements, and GUI elements
        game.Render()
        player.Render()
        gui.Update(time_delta)  # Update all GUI components
        gui.Render()  # Render all GUI components

        pygame.display.flip()  # Update the display with the rendered frame
    
    pygame.quit()  # Quit pygame when the loop ends
