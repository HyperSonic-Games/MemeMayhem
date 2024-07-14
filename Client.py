import pygame
import pygame_gui
import threading
import FLEXCOM  
import Utils
import sys

# Base Game class
class Game:
    UserName = None  # Class-level attribute to store the username

    def __init__(self):
        # Get the user's name using a popup input only once
        if Game.UserName is None:
            Game.UserName = Utils.PopupManager().TextInput("Enter Your User Name", "User Name: ")

        # Set window properties
        self.WindowWidth = 800
        self.WindowHeight = 600
        self.WindowTitle = "Meme Mayhem"

        if len(sys.argv) > 1:
            print(sys.argv[1])

        # Initialize pygame and setup the display
        pygame.init()
        self.screen = pygame.display.set_mode((self.WindowWidth, self.WindowHeight))
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
        self.screen.fill((0, 0, 0))  # Example: clear screen with black


# Gui class inheriting from Game
class Gui(Game):
    def __init__(self):
        super().__init__()
        # Initialize pygame_gui elements

    def Render(self):
        self.RenderContext = super().GetRenderContext()
        # Implement additional GUI rendering logic specific to Gui class
        # Example: render some text
        font = pygame.font.Font(None, 36)
        text = font.render('GUI Rendering', True, (255, 255, 255))
        self.RenderContext.blit(text, (10, 10))


# Player class inheriting from Game
class Player(Game):
    def __init__(self):
        super().__init__()
        # Initialize player-specific attributes and logic

    def Render(self):
        self.RenderContext = super().GetRenderContext()
        # Example: render a player rectangle
        pygame.draw.rect(self.RenderContext, (0, 128, 255), pygame.Rect(50, 50, 60, 60))


# Main entry point
if __name__ == "__main__":
    

    # Initialize the core game, GUI, and player
    game = Game()
    gui = Gui()
    player = Player()
    
    # Start The FLEXCOM Classes And Check For Conection
    if len(sys.argv) > 1:
        host = sys.argv[1]
    FLEXCOM_Client = FLEXCOM.Client(host=host, )

    running = True  # Main loop control variable
    clock = pygame.time.Clock()  # Clock object to control frame rate

    while running:
        TimeDelta = clock.tick() / 1000  # Time since the last tick in milliseconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Exit the loop if the Escape key is pressed

        # Render core game elements, GUI elements, and player elements
        game.Render()
        player.Render()
        gui.Render()


        pygame.display.flip()  # Update the display with the rendered frame
        clock.tick(60)  # Limit frame rate to 60 FPS

    pygame.quit()  # Quit pygame when the loop ends