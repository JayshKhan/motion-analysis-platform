import inspect

import pygame

from src.config import config_instance as CONFIG
from src.core import algorithms
from src.ui.assets import Button


class AlgorithmSelectionScreen:

    def __init__(self):
        self.algorithm_buttons = []
        self.hovered_button = None

    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.current_screen = "main_menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for name, button in app.algorithm_selection_screen.algorithm_buttons:
                if button.rect.collidepoint(mouse_pos):
                    app.load_algorithm(name)  # Load the selected algorithm in MAPApp
                    app.run_selected_algorithm()  # Transition to execution screen

    @staticmethod
    def update(app):
        mouse_pos = pygame.mouse.get_pos()
        for button in app.algorithm_selection_screen.algorithm_buttons:
            name, button = button
            if button.rect.collidepoint(mouse_pos):
                app.algorithm_selection_screen.hovered_button = name
                button.update(mouse_pos)
                break
            else:
                app.algorithm_selection_screen.hovered_button = None

    @staticmethod
    def draw(app):
        app.screen.fill((230, 230, 230))  # Light gray background
        font = pygame.font.Font(None, 36)
        button_y_start = 100
        button_height = 50
        button_spacing = 10
        button_width = 300

        # Title
        title_text = font.render("Select Motion Planning Algorithm", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(app.screen_width // 2, 50))
        app.screen.blit(title_text, title_rect)

        # Algorithm Buttons
        available_algorithms = AlgorithmSelectionScreen.get_available_algorithms()
        app.algorithm_selection_screen.algorithm_buttons = []
        for i, algo_name in enumerate(available_algorithms):
            button_rect = Button(
                app.screen_width // 2 - button_width // 2,
                button_y_start + i * (button_height + button_spacing),
                button_width,
                button_height,
                algo_name.replace("_", " ").title(),
                action=lambda: app.load_algorithm(algo_name)
            )

            app.algorithm_selection_screen.algorithm_buttons.append((algo_name, button_rect))
            button_rect.draw(app.screen)

            text_color = CONFIG.text_color
            text = font.render(algo_name.replace("_", " ").title(), True, text_color)
            text_rect = text.get_rect(center=button_rect.rect.center)
            app.screen.blit(text, text_rect)

        # Instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Press ESC to go back to Main Menu",
            "Click on an algorithm to select and proceed",
        ]
        y_offset = app.screen_height - 2 * 20 - 10
        for line in instructions:
            text = instruction_font.render(line, True, (0, 0, 0))
            app.screen.blit(text, (10, y_offset))
            y_offset += 20

    @staticmethod
    def get_available_algorithms():
        algorithms_list = []
        for name, obj in inspect.getmembers(algorithms):
            if inspect.isclass(obj) and hasattr(obj, 'plan'):
                algorithms_list.append(name)
        return algorithms_list
