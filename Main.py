import pygame
import sys
import subprocess

# Constant to suppress the console window when launching subprocesses
CREATE_NO_WINDOW = 0x08000000

# Initialize Pygame
pygame.init()

# Set up the display dimensions
ScreenWidth = 800
ScreenHeight = 600

# Set the window title
pygame.display.set_caption("Meme Mayhem: Main Menu")

# Try to create a display surface with vsync enabled
try:
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), vsync=1)
    print("Vsync Render Created")
except:
    # Fall back to creating a normal display surface if vsync is not supported
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
    print("Normal Renderer Created")

# Define color constants
Gray = (50, 50, 50)
White = (255, 255, 255)
NavyBlue = (0, 0, 128)
Red = (255, 0, 0)

# Define button dimensions and spacing
ButtonWidth = 200
ButtonHeight = 50
ButtonSpacing = 20

# Define a Button class for creating clickable buttons
class Button:
    def __init__(self, x, y, width, height, color, text=''):
        # Initialize button properties
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        # Draw the button on the given surface
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text != '':
            # Render and draw the button text
            text_surface = self.font.render(self.text, True, White)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

# Create buttons for the main menu
main_menu_buttons = [
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2 - ButtonHeight - ButtonSpacing, ButtonWidth, ButtonHeight, NavyBlue, "Play"),
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2, ButtonWidth, ButtonHeight, NavyBlue, "Host"),
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2 + ButtonHeight + ButtonSpacing, ButtonWidth, ButtonHeight, NavyBlue, "Settings"),
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2 + 2 * (ButtonHeight + ButtonSpacing), ButtonWidth, ButtonHeight, NavyBlue, "Credits")
]

# Create a button for the settings menu
settings_buttons = [
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2 + 2 * (ButtonHeight + ButtonSpacing), ButtonWidth, ButtonHeight, Red, "Back")
]

# Function to display the main menu
def MainMenu():
    # Load and play the main theme music
    pygame.mixer.music.load("Assets/Sound/Meme Mayhem Main Theme.mp3")
    pygame.mixer.music.play(-1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle quit event
                pygame.quit()
                sys.exit()

            # Check for mouse button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in main_menu_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.text == "Play":
                            # Stop music, quit Pygame, and run Client.py
                            pygame.mixer.music.stop()
                            pygame.quit()
                            subprocess.run(["python", "Client.py"], creationflags=CREATE_NO_WINDOW)
                            sys.exit()  # Exit Python
                        
                        elif button.text == "Host":
                            # Stop music, quit Pygame, and run Server.py
                            pygame.mixer.music.stop()
                            pygame.quit()
                            subprocess.run(["python", "Server.py"], creationflags=CREATE_NO_WINDOW)
                            sys.exit()  # Exit Python
                        elif button.text == "Settings":
                            # Quit Pygame and run SettingsManager.py
                            pygame.quit()
                            subprocess.run(["python", "SettingsManager.py"], creationflags=CREATE_NO_WINDOW)
                            sys.exit()  # Exit Python
                        elif button.text == "Credits":
                            # Handle Credits action (not implemented)
                            pass

        # Clear the screen with the gray color
        Screen.fill(Gray)

        # Draw all main menu buttons
        for button in main_menu_buttons:
            button.draw(Screen)

        # Update the display with the new frame
        pygame.display.flip()

# Run the main menu if this script is executed directly
if __name__ == "__main__":
    MainMenu()
