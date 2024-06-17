import pygame
import sys
import subprocess

CREATE_NO_WINDOW = 0x08000000

# Initialize Pygame
pygame.init()

# Set up the display
ScreenWidth = 800
ScreenHeight = 600

pygame.display.set_caption("Meme Mayhem: Main Menu")
try:
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), vsync=1)
    print("Vsync Render Created")
except:
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
    print("Normal Renderer Created")

# Colors
Gray = (50, 50, 50)
White = (255, 255, 255)
NavyBlue = (0, 0, 128)
Red = (255, 0, 0)

# Button properties
ButtonWidth = 200
ButtonHeight = 50
ButtonSpacing = 20

# Define button class
class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text != '':
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

# Create buttons for the settings menu
settings_buttons = [
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2 + 2 * (ButtonHeight + ButtonSpacing), ButtonWidth, ButtonHeight, Red, "Back")
]

def MainMenu():
    pygame.mixer.music.load("Assets/Sound/Meme Mayhem Main Theme.mp3")
    pygame.mixer.music.play(-1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in main_menu_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.text == "Play":
                            pygame.mixer.music.stop()
                            pygame.quit()
                            subprocess.run(["python", "Client.py"], creationflags=CREATE_NO_WINDOW)
                            sys.exit()  # Exit Python
                        
                        elif button.text == "Host":
                            pygame.mixer.music.stop()
                            pygame.quit()
                            subprocess.run(["python", "Server.py"], creationflags=CREATE_NO_WINDOW)
                            sys.exit()  # Exit Python
                        elif button.text == "Settings":
                            subprocess.run(["python", "SettingsManager.py"], creationflags=CREATE_NO_WINDOW)
                        elif button.text == "Credits":
                            # Handle Credits action
                            pass

        # Clear the screen
        Screen.fill(Gray)

        # Draw buttons
        for button in main_menu_buttons:
            button.draw(Screen)

        # Update the display
        pygame.display.flip()


# Call the MainMenu function to run the main menu loop
if __name__ == "__main__":
    MainMenu()
