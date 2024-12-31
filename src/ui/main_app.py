import inspect

import pygame

from src.config import config_instance as CONFIG
from src.core import sensors
from src.core.environment import Environment
from src.ui.assets import Button
from src.ui.screens.algorithm_selection import AlgorithmSelectionScreen
from src.ui.screens.environment_editor import EnvironmentEditorScreen
from src.ui.screens.execution_screen import ExecutionScreen  # Import the new screen
from src.ui.screens.main_menu import MainMenuScreen
from src.ui.screens.sensor_import import SensorImportScreen


class MAPApp:
    def __init__(self):
        pygame.init()
        self.screen_width = CONFIG.screen_width
        self.screen_height = CONFIG.screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(CONFIG.title_text)
        self.clock = pygame.time.Clock()
        self.current_screen = "main_menu"
        self.environment = Environment(int(CONFIG.screen_width / int(CONFIG.grid_resolution)),
                                       int(CONFIG.screen_height / int(CONFIG.grid_resolution)))  # Adjusted grid size
        self.selected_algorithm_name = None
        self.imported_sensor_module = None
        self.selected_sensor = None

        # Button hover states and rects for the main menu
        self.algorithm_button_hovered = False
        self.environment_button_hovered = False
        self.sensor_button_hovered = False
        button_width = 250
        button_height = 50
        button_spacing = 20
        start_y = 200

        self.sensor_button_rect = Button(
            self.screen_width // 2 - button_width // 2,
            start_y + 2 * (button_height + button_spacing),
            button_width,
            button_height,
            "Sensor Model",
            action=lambda: setattr(self, "current_screen", "sensor_import"),
        )
        self.environment_button_rect = Button(
            self.screen_width // 2 - button_width // 2,
            start_y,
            button_width,
            button_height,
            "Edit Environment",
            action=lambda: setattr(self, "current_screen", "environment_editor"),
        )
        self.algorithm_button_rect = Button(
            self.screen_width // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width,
            button_height,
            "Run Algorithm",
            action=lambda: setattr(self, "current_screen", "algorithm_selection"),
        )

        # Initialize screens

        self.environment_editor_screen = EnvironmentEditorScreen()
        self.sensor_import_screen = SensorImportScreen()
        self.algorithm_selection_screen = AlgorithmSelectionScreen()
        self.execution_screen = ExecutionScreen()  # Initialize the execution screen

    def run(self):
        running = True
        while running:
            # Background

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
        elif self.current_screen == "execution":
            ExecutionScreen.handle_input(self, event)

    def update(self):
        if self.current_screen == "main_menu":
            MainMenuScreen.update(self)
        elif self.current_screen == "environment_editor":
            EnvironmentEditorScreen.update(self)
        elif self.current_screen == "algorithm_selection":
            AlgorithmSelectionScreen.update(self)
        elif self.current_screen == "sensor_import":
            SensorImportScreen.update(self)
        elif self.current_screen == "execution":
            ExecutionScreen.update(self)

    def draw(self):
        if self.current_screen == "main_menu":
            MainMenuScreen.draw(self)
        elif self.current_screen == "environment_editor":
            EnvironmentEditorScreen.draw(self)
        elif self.current_screen == "algorithm_selection":
            AlgorithmSelectionScreen.draw(self)
        elif self.current_screen == "sensor_import":
            SensorImportScreen.draw(self)
        elif self.current_screen == "execution":
            ExecutionScreen.draw(self)
        pygame.display.flip()

    def load_algorithm(self, algorithm_name):
        self.selected_algorithm_name = algorithm_name

    def load_sensor(self, sensor_module):
        self.imported_sensor_module = sensor_module
        # Try to instantiate the first class that inherits from SensorModel
        for name, obj in sensor_module.__dict__.items():
            if inspect.isclass(obj) and issubclass(obj, sensors.SensorModel) and obj != sensors.SensorModel:
                self.selected_sensor = obj()
                print(f"Loaded sensor: {self.selected_sensor}")
                return
        print("No valid SensorModel found in the imported module.")
        self.selected_sensor = None

    def run_selected_algorithm(self):
        self.current_screen = "execution"
        self.execution_screen.reset()  # Reset execution screen state



