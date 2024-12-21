import pygame

from src.core import algorithms
from src.ui.screens.main_menu import MainMenuScreen
from src.core.environment import Environment
from src.core.algorithms import random_walk  # Example import
from src.ui.screens.environment_editor import EnvironmentEditorScreen
from src.ui.screens.algorithm_selection import AlgorithmSelectionScreen
from src.ui.screens.sensor_import import SensorImportScreen

class MAPApp:
    def __init__(self):
        pygame.init()
        self.algorithm_selection_screen = AlgorithmSelectionScreen()
        self.environment_editor_screen = EnvironmentEditorScreen()
        self.sensor_import_screen = SensorImportScreen()
        self.imported_sensor_module = None  # To store the imported sensor module

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Motion Analysis Platform")
        self.clock = pygame.time.Clock()
        self.current_screen = "main_menu"
        self.environment = Environment(50, 40) # Example environment

        # Button hover states for the main menu
        self.algorithm_button_hovered = False
        self.environment_button_hovered = False
        self.sensor_button_hovered = False

        # Initialize button rects here
        button_width = 250
        button_height = 50
        button_spacing = 20
        start_y = 200

        self.environment_button_rect = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            start_y,
            button_width,
            button_height,
        )

        self.algorithm_button_rect = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width,
            button_height,
        )

        self.sensor_button_rect = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            start_y + 2 * (button_height + button_spacing),
            button_width,
            button_height,
        )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def handle_input(self, event):
        if self.current_screen == "main_menu":
            MainMenuScreen.handle_input(self, event)
        elif self.current_screen == "environment_editor":
            EnvironmentEditorScreen.handle_input(self, event)
        elif self.current_screen == "algorithm_selection":
            AlgorithmSelectionScreen.handle_input(self, event)
        elif self.current_screen == "sensor_import":
            SensorImportScreen.handle_input(self, event)

    def update(self):
        if self.current_screen == "main_menu":
            MainMenuScreen.update(self)
        elif self.current_screen == "environment_editor":
            EnvironmentEditorScreen.update(self)
        elif self.current_screen == "algorithm_selection":
            AlgorithmSelectionScreen.update(self)
        elif self.current_screen == "sensor_import":
            SensorImportScreen.update(self)

    def draw(self):
        if self.current_screen == "main_menu":
            MainMenuScreen.draw(self)
        elif self.current_screen == "environment_editor":
            EnvironmentEditorScreen.draw(self)
        elif self.current_screen == "algorithm_selection":
            AlgorithmSelectionScreen.draw(self)
        elif self.current_screen == "sensor_import":
            SensorImportScreen.draw(self)
        pygame.display.flip()

    def run_selected_algorithm(self):
        if self.algorithm_selection_screen.selected_algorithm_name:
            algorithm_name = self.algorithm_selection_screen.selected_algorithm_name
            # Find the selected algorithm class
            selected_algorithm_class = getattr(algorithms, algorithm_name)
            planner = selected_algorithm_class()
            path = planner.plan(self.environment)
            if path:
                print("Path found:", path)
                # You would likely switch to a new screen to display the results
            else:
                print("No path found.")

if __name__ == "__main__":
    app = MAPApp()
    app.run()