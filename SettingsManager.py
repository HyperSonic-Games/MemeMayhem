import pygame
import pygame_gui
import toml

class SettingsManager:
    def __init__(self, filename):
        # Load settings from the TOML file
        with open(filename, 'r') as f:
            self.settings = toml.load(f)
        
    def GetSetting(self, section, setting_name):
        # Retrieve a specific setting from a given section
        section_data = self.settings.get(section)
        if section_data:
            return section_data.get(setting_name)
        return None


class SettingsManagerUi:
    def __init__(self, filename):
        self.filename = filename
        self.settings = self.load_settings()  # Load settings when initializing

    def load_settings(self):
        # Load settings from the TOML file
        try:
            with open(self.filename, 'r') as f:
                settings = toml.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            settings = {}
        return settings

    def save_settings(self):
        # Save current settings to the TOML file
        try:
            with open(self.filename, 'w') as f:
                toml.dump(self.settings, f)
            print("Settings saved successfully.")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get_settings(self):
        # Return the current settings
        return self.settings


if __name__ == "__main__":
    # Initialize pygame
    pygame.init()

    # Define colors for the dark theme
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (200, 200, 200)
    BUTTON_COLOR = (50, 50, 50)
    BUTTON_TEXT_COLOR = (200, 200, 200)

    # Load settings and calculate the window height based on the number of settings sections and elements
    settings_manager = SettingsManagerUi('SETTINGS.toml')
    num_sections = len(settings_manager.get_settings())
    num_elements = sum(len(values) for values in settings_manager.get_settings().values())
    window_height = 50 + num_sections * 40 + num_elements * 40 + 150  # Calculate total height

    # Set up display with calculated dimensions, limiting height to 600 if needed
    screen = pygame.display.set_mode((400, min(window_height, 600)), pygame.SCALED)
    pygame.display.set_caption('Settings Editor')

    # Initialize pygame GUI manager
    manager = pygame_gui.UIManager(screen.get_size())

    # Create a scroll view container to hold all settings elements
    scroll_view = pygame_gui.elements.UIScrollingContainer(
        relative_rect=pygame.Rect(0, 0, 400, min(window_height, 600)),
        manager=manager
    )

    # Initialize y position for placing elements in the GUI
    y_pos = 50
    elements = []  # List to store all created elements

    # Loop through each section and its values in the settings
    for section, values in settings_manager.get_settings().items():
        # Create a label for the section
        label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, y_pos), (200, 30)),
            text=f"[{section}]",
            manager=manager,
            container=scroll_view,
            object_id='#section_label',
        )
        y_pos += 40  # Update y position for the next element
        # Loop through each key-value pair in the section
        for key, value in values.items():
            if key.startswith('_'):  # Skip internal config parser items
                continue
            # Create a label for the key
            label_key = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((50, y_pos), (150, 30)),
                text=f"{key}:",
                manager=manager,
                container=scroll_view,
                object_id='#key_label',
            )
            elements.append(label_key)  # Add label to elements list
            # Create an input field for the value
            input_field = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((200, y_pos), (150, 30)),
                manager=manager,
                container=scroll_view,
                object_id='#input_field',
            )
            input_field.set_text(str(value))  # Set the input field's text to the current value
            elements.append(input_field)  # Add input field to elements list
            elements.append((section, key, input_field))  # Store references for saving later
            y_pos += 40  # Update y position for the next element

    # Add a button to save the settings
    save_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, y_pos), (100, 40)),
        text='Save',
        manager=manager,
        container=scroll_view,
        object_id='#save_button',
    )
    elements.append(save_button)  # Add save button to elements list

    # Main loop to handle events and update the GUI
    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0  # Time delta in seconds

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the main loop
            elif event.type == pygame.USEREVENT:
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == save_button:
                        print("Save button pressed.")
                        # Update settings from input fields
                        try:
                            for element in elements:
                                if isinstance(element, tuple):  # Only process input field tuples
                                    section, key, input_field = element
                                    settings_manager.get_settings()[section][key] = input_field.get_text()
                            # Save updated settings to the TOML file
                            settings_manager.save_settings()
                        except Exception as e:
                            print(f"Error updating or saving settings: {e}")

            manager.process_events(event)  # Process the event with the GUI manager

        manager.update(time_delta)  # Update the GUI manager

        screen.fill(BACKGROUND_COLOR)  # Fill the screen with the background color
        scroll_view.set_position((0, 0))  # Reset scroll position
        scroll_view.update(time_delta)  # Update the scroll view
        manager.draw_ui(screen)  # Draw the GUI elements

        pygame.display.flip()  # Update the display

    pygame.quit()  # Quit pygame