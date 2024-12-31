import pygame

from src.config import config_instance as CONFIG
from src.ui.assets import Button, ColorPicker


class SettingsScreen:
    def __init__(self):
        self.config = CONFIG
        self.settings_controls = {}
        self.back_button = None
        self.color_picker_buttons = {}

    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for color_picker in app.settings_screen.color_picker_buttons.values():
                color_picker.handle_event(event)
        if app.settings_screen.back_button:
            if event.type == pygame.MOUSEBUTTONDOWN:
                app.settings_screen.back_button.handle_event(event)
        if event.type == pygame.MOUSEWHEEL:
            app.scroll_y -= event.y * 20

    @staticmethod
    def update(app):
        pass

    @staticmethod
    def draw(app):
        # Constants for scrollable area
        content_height = 2000  # Adjust as needed for total settings content height
        scroll_speed = 20  # Pixels to scroll with each event
        app.scroll_y = getattr(app, 'scroll_y', 0)  # Initialize if not already set

        # Clamp the scroll_y to ensure it doesn't go out of bounds
        app.scroll_y = max(0, min(content_height - app.screen_height, app.scroll_y))

        # Create the scrollable content surface
        content_surface = pygame.Surface((app.screen_width, content_height))
        content_surface.fill((240, 240, 240))  # Background color

        # Draw content on the scrollable surface
        font = pygame.font.Font(None, 36)
        title_text = font.render("Settings", True, CONFIG.title_color)
        title_rect = title_text.get_rect(center=(app.screen_width // 2, 50))
        content_surface.blit(title_text, title_rect)

        app.settings_screen.back_button = Button(
            20, 20, 100, 50, "Back",
            action=lambda: setattr(app, "current_screen", "main_menu"),
        )
        app.settings_screen.back_button.draw(content_surface)

        # Draw settings options
        settings_y_start = 100
        settings_spacing = 10
        settings_width = 300
        settings_height = 50

        for i, (setting_name, setting_value) in enumerate(app.settings_screen.config.__dict__.items()):
            if setting_name.startswith("_"):
                continue
            if isinstance(setting_value, tuple) and "color" in setting_name:
                app.settings_screen.color_picker_buttons[setting_name] = ColorPicker(
                    position=(
                        app.screen_width // 2 - settings_width // 2,
                        settings_y_start + i * (settings_height + settings_spacing)
                    ),
                    title=setting_name,
                    initial_color=setting_value,
                    action=lambda name=setting_name: setattr(
                        app.settings_screen.config,
                        name,
                        app.settings_screen.color_picker_buttons[name].selected_color
                    )
                )

        for color_picker in app.settings_screen.color_picker_buttons.values():
            color_picker.draw(content_surface)

        # Draw the visible portion of the content surface onto the main screen
        # app.screen.fill((0, 0, 0))  # Clear screen
        app.screen.blit(content_surface, (0, -app.scroll_y)
                        # ,area=pygame.Rect(0, app.scroll_y, app.screen_width, app.screen_height)
                        )

        # Draw a diagonal red text to say that setting not implemented yet
        font = pygame.font.Font(None, 100)
        text = font.render("Setting not implemented yet", True, (255, 0, 0))
        text = pygame.transform.rotate(text, 45)  # Rotate the text surface by 45 degrees
        text_rect = text.get_rect(center=(app.screen_width // 2, app.screen_height // 2))
        app.screen.blit(text, text_rect)

        pygame.display.flip()
