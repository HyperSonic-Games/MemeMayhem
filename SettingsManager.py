import pygame
import sys

class InputUtils:
    @staticmethod
    def handle_events(input_manager):
        """Handle all events and pass them to the input manager."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_manager.quit_game()
            elif event.type == pygame.KEYDOWN:
                input_manager.key_down(event.key)
            elif event.type == pygame.KEYUP:
                input_manager.key_up(event.key)

class InputManager:
    def __init__(self):
        self.actions = {
            pygame.K_w: self.move_forward,
            pygame.K_s: self.move_backward,
            pygame.K_a: self.move_left,
            pygame.K_d: self.move_right,
            pygame.K_SPACE: self.shoot,
            pygame.K_e: self.interact,
            pygame.K_q: self.quit_game
        }
        self.pressed_keys = set()

    def key_down(self, key):
        """Handle key press events."""
        if key in self.actions:
            self.actions[key]()
        self.pressed_keys.add(key)

    def key_up(self, key):
        """Handle key release events."""
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def move_forward(self):
        print("Moving forward")

    def move_backward(self):
        print("Moving backward")

    def move_left(self):
        print("Moving left")

    def move_right(self):
        print("Moving right")

    def shoot(self):
        print("Shooting")

    def interact(self):
        print("Interacting")

    def quit_game(self):
        print("Quitting game")
        pygame.quit()
        sys.exit()

# Example usage
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("3rd Person Shooter Input Manager")

    input_manager = InputManager()

    while True:
        InputUtils.handle_events(input_manager)
        screen.fill((0, 0, 0))  # Clear the screen with black

        # Here you would update game logic and render game objects

        pygame.display.flip()  # Update the full display Surface to the screen

if __name__ == "__main__":
    main()