import pygame
from src.core import algorithms  # Import the algorithms module
import inspect

class AlgorithmSelectionScreen:
    BUTTON_COLOR = (0, 128, 255)
    BUTTON_HOVER_COLOR = (0, 150, 255)
    TEXT_COLOR = (255, 255, 255)

    def __init__(self):
        self.algorithm_buttons = []
        self.selected_algorithm_name = None

    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.current_screen = "main_menu"
            elif event.key == pygame.K_RETURN and app.algorithm_selection_screen.selected_algorithm_name:
                # Run the selected algorithm (implementation needed in MAPApp)
                app.run_selected_algorithm()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for name, rect in app.algorithm_selection_screen.algorithm_buttons:
                if rect.collidepoint(mouse_pos):
                    app.algorithm_selection_screen.selected_algorithm_name = name

    @staticmethod
    def update(app):
        mouse_pos = pygame.mouse.get_pos()
        for name, rect in app.algorithm_selection_screen.algorithm_buttons:
            if rect.collidepoint(mouse_pos):
                app.algorithm_selection_screen.hovered_button = name
                break
            else:
                app.algorithm_selection_screen.hovered_button = None

    @staticmethod
    def draw(app):
        app.screen.fill((230, 230, 230))  # Light gray background
        font = pygame.font.Font(None, 36)
        button_y_start = 100
        button_height = 40
        button_spacing = 10
        button_width = 200

        # Get list of available algorithms dynamically
        available_algorithms = AlgorithmSelectionScreen.get_available_algorithms()
        app.algorithm_selection_screen.algorithm_buttons = []

        # Title
        title_text = font.render("Select Motion Planning Algorithm", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(app.screen_width // 2, 50))
        app.screen.blit(title_text, title_rect)

        # Algorithm Buttons
        for i, algo_name in enumerate(available_algorithms):
            button_rect = pygame.Rect(
                app.screen_width // 2 - button_width // 2,
                button_y_start + i * (button_height + button_spacing),
                button_width,
                button_height,
            )
            app.algorithm_selection_screen.algorithm_buttons.append((algo_name, button_rect))

            is_hovered = app.algorithm_selection_screen.hovered_button == algo_name
            button_color = AlgorithmSelectionScreen.BUTTON_HOVER_COLOR if is_hovered else AlgorithmSelectionScreen.BUTTON_COLOR
            pygame.draw.rect(app.screen, button_color, button_rect)

            text_color = AlgorithmSelectionScreen.TEXT_COLOR
            if app.algorithm_selection_screen.selected_algorithm_name == algo_name:
                text_color = (255, 255, 0)  # Highlight selected algorithm

            text = font.render(algo_name.replace("_", " ").title(), True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            app.screen.blit(text, text_rect)

        # Instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Press ESC to go back to Main Menu",
            "Click to select an algorithm",
            "Press ENTER to run the selected algorithm"
        ]
        y_offset = app.screen_height - 3 * 20 - 10
        for line in instructions:
            text = instruction_font.render(line, True, (0, 0, 0))
            app.screen.blit(text, (10, y_offset))
            y_offset += 20

    @staticmethod
    def get_available_algorithms():
        # Dynamically get available algorithms from the src.core.algorithms module
        algorithms_list = []
        for name, obj in inspect.getmembers(algorithms):
            if inspect.isclass(obj) and hasattr(obj, 'plan'):  # Check if it's a class with a 'plan' method
                algorithms_list.append(name)
        return algorithms_list