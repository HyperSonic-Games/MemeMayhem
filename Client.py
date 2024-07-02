import pygame
import pygame_gui
import threading
import MultiPlayer  
import Utils

# Base Game class
class Game:
    def __init__(self):
        # Get the user's name using a popup input
        self.UserName = Utils.PopupManager().TextInput("Enter Your User Name", "User Name: ")
        # Set window properties
        self.WindowWidth = 800
        self.WindowHeight = 600
        self.WindowTitle = "Meme Mayhem"

        # Initialize pygame and setup the display
        pygame.init()
        self.screen = pygame.display.set_mode((self.WindowWidth, self.WindowHeight))
        pygame.display.set_caption(self.WindowTitle)

        # Toggle fullscreen mode if possible
        if pygame.display.get_init():
            pygame.display.toggle_fullscreen()
        else:
            # If initialization fails, show an error popup and exit
            Utils.PopupManager.Error("Error", "Pygame Display Surface Failed To Initialize")
            pygame.quit()
            exit(1)

    def render(self):
        # Implement rendering logic common to all game elements
        pass

# Gui class inheriting from Game
class Gui(Game):
    def __init__(self):
        super().__init__()
        # Initialize pygame_gui or other GUI-related elements

    def render(self):
        super().render()
        # Implement additional GUI rendering logic specific to Gui class

# Player class inheriting from Game
class Player(Game):
    def __init__(self):
        super().__init__()
        # Initialize player-specific attributes and logic

    def render(self):
        super().render()
        # Implement additional rendering logic specific to Player class


# Main entry point
if __name__ == "__main__":
    # Initialize the core game, GUI, and player
    game = Game()
    gui = Gui()
    player = Player()

    running = True  # Main loop control variable
    clock = pygame.time.Clock()  # Clock object to control frame rate

    while running:
        TimeDelta = clock.tick() / 1000  # Time since the last tick in milliseconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed

        # Render core game elements, GUI elements, and player elements
        game.render()
        gui.render()
        player.render()

        pygame.display.flip()  # Update the display with the rendered frame
        clock.tick(60)  # Limit frame rate to 60 FPS

    pygame.quit()  # Quit pygame when the loop ends
