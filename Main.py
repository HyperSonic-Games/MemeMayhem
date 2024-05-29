import pygame
import sys
import subprocess
import runpy

# Initialize Pygame
pygame.init()

# Set up the display
ScreenWidth = 800
ScreenHeight = 600
Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Meme Mayhem: Main Menu")

# Colors
Gray = (50, 50, 50)
White = (255, 255, 255)
NavyBlue = (0, 0, 128)

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

# Create buttons
buttons = [
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2 - ButtonHeight - ButtonSpacing, ButtonWidth, ButtonHeight, NavyBlue, "Play"),
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2, ButtonWidth, ButtonHeight, NavyBlue, "Host"),
    Button(ScreenWidth // 2 - ButtonWidth // 2, ScreenHeight // 2 + ButtonHeight + ButtonSpacing, ButtonWidth, ButtonHeight, NavyBlue, "Credits")
]

def MainMenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.text == "Play":
                            subprocess.run(["python", "Client.py"])  # Run the GameJoin.py file
                            pygame.quit()  # Exit Pygame
                            sys.exit()  # Exit Python
                        elif button.text == "Host":
                            subprocess.Popen("python Server.py")
                            exit(0)

        # Clear the screen
        Screen.fill(Gray)

        # Draw buttons
        for button in buttons:
            button.draw(Screen)

        # Update the display
        pygame.display.flip()

# Call the MainMenu function to run the main menu loop
if __name__ == "__main__":
    MainMenu()
