import importlib
import importlib.util
import inspect
import os
import sys
import tkinter as tk
from tkinter import filedialog

import pygame

from src.core.sensors.sensor_model import SensorModel
from src.ui.assets import Button
from src.ui.config import INFO_TEXT_COLOR, SCREENWIDTH, TEXT_COLOR


def load_sensor_dynamically(module_name):
    """
    Dynamically loads a sensor class from a module.

    Args:
        module_name: The name of the module (e.g., "range_sensor").

    Returns:
        The sensor class (subclass of SensorModel) or None if not found.
    """
    try:
        module = importlib.import_module(f"src.core.sensors.{module_name}")  # Assuming sensors are in this package
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, SensorModel) and obj != SensorModel:
                return obj  # Return the first class that is a subclass of SensorModel
        print(f"No sensor class found in module: {module_name}")
        return None
    except ModuleNotFoundError:
        print(f"Module not found: {module_name}")
        return None

class SensorImportScreen:
    def __init__(self):
        self.import_button_rect = None
        self.imported_sensor_name = None
        self.available_sensors = []  # List to store available sensor names
        self.sensor_buttons = []  # List to store sensor selection buttons




    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.current_screen = "main_menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            app.sensor_import_screen.import_button_rect.handle_event(event)
            for name, button in app.sensor_import_screen.sensor_buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.handle_event(event)


    @staticmethod
    def update(app):
        mouse_pos = pygame.mouse.get_pos()
        if app.sensor_import_screen.import_button_rect:
            app.sensor_import_screen.import_button_rect.update(mouse_pos)
        app.sensor_import_screen.sensor_buttons

    @staticmethod
    def draw(app):
        app.screen.fill((220, 220, 220))  # Light gray background
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        button_y_start = 100
        button_height = 50
        button_spacing = 10
        button_width = 300

        # Title
        title_text = font.render("Import Custom Sensor Model", True, INFO_TEXT_COLOR)
        title_rect = title_text.get_rect(center=(app.screen_width // 2, 100))
        app.screen.blit(title_text, title_rect)

        available_sensors = SensorImportScreen.load_sensor_modules()
        app.sensor_import_screen.sensor_buttons = []
        for i, path in enumerate(available_sensors):
            module_name, module = SensorImportScreen.get_sensor_name_from_file(path)

            button_rect = Button(
                app.screen_width // 2 - button_width // 2,
                button_y_start + i * (button_height + button_spacing) + 20,
                button_width,
                button_height,
                module_name.replace("_", " ").title(),
                action=lambda: app.load_sensor(module)
            )

            app.sensor_import_screen.sensor_buttons.append((module_name, button_rect))
            button_rect.draw(app.screen)

            text_color = TEXT_COLOR
            text = font.render(module_name.replace("_", " ").title(), True, text_color)
            text_rect = text.get_rect(center=button_rect.rect.center)
            app.screen.blit(text, text_rect)

        # Import Button
        button_width = 200
        button_height = 40
        button_x = SCREENWIDTH // 2 - button_width // 2
        button_y = 200

        app.sensor_import_screen.import_button_rect = Button(
            button_x,
            button_y,
            button_width,
            button_height,
            "Import .py File",
            action=lambda: SensorImportScreen.open_file_dialog(app),
        )

        app.sensor_import_screen.import_button_rect.draw(app.screen)
        # button_color = BUTTON_HOVER_COLOR if app.sensor_import_screen.import_button_hovered else BUTTON_COLOR
        # pygame.draw.rect(app.screen, button_color, app.sensor_import_screen.import_button_rect)
        # import_text = font.render("Import .py File", True, TEXT_COLOR)
        # import_text_rect = import_text.get_rect(center=app.sensor_import_screen.import_button_rect.center)
        # app.screen.blit(import_text, import_text_rect)

        # Instructions
        instructions = [
            "Press ESC to go back to Main Menu",
            "Click 'Import .py File' to select your sensor model.",
            "Ensure your sensor class inherits from SensorModel.",
        ]
        y_offset = 300
        for line in instructions:
            text = small_font.render(line, True, INFO_TEXT_COLOR)
            text_rect = text.get_rect(center=(app.screen_width // 2, y_offset))
            app.screen.blit(text, text_rect)
            y_offset += 30

        # Display Imported Sensor Name
        if app.selected_sensor:
            sensor_name = app.selected_sensor.__class__.__name__
            imported_text = small_font.render(f"Imported Sensor: {sensor_name}", True, (0, 150, 0))
            imported_rect = imported_text.get_rect(center=(app.screen_width // 2, 400))
            app.screen.blit(imported_text, imported_rect)

    @staticmethod
    def open_file_dialog(app):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(
            title="Select Sensor Model (.py file)",
            filetypes=(("Python files", "*.py"), ("All files", "*.*"))
        )
        if file_path:
            SensorImportScreen.load_sensor_from_file(app, file_path)

    @staticmethod
    def load_sensor_from_file(app, file_path):
        try:
            spec = importlib.util.spec_from_file_location("custom_sensor_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["custom_sensor_module"] = module
            spec.loader.exec_module(module)
            # print([name for name, obj in inspect.getmembers(module)])
            app.load_sensor(module)  # Load the sensor in MAPApp
        except Exception as e:
            print(f"Error importing sensor model: {e}")

    @staticmethod
    def get_sensor_name_from_file(file_path):
        try:
            spec = importlib.util.spec_from_file_location("custom_sensor_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["custom_sensor_module"] = module
            spec.loader.exec_module(module)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, SensorModel) and obj != SensorModel:
                    return (obj.__name__, module)
        except Exception as e:
            print(f"Error importing sensor model: {e}")
        return None

    @staticmethod
    def load_sensor_modules():
        """Loads available sensor modules from the sensors directory."""
        available_sensors = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir))) + "\src"
        sensors_dir = os.path.join(src_dir, "core", "sensors", "example_sensors")

        for filename in os.listdir(sensors_dir):
            if filename.endswith(
                    ".py") and filename != "__init__.py" and filename != "sensor_model.py" and filename.startswith(
                    "__") == False:
                module_name = filename[:-3]
                path = os.path.join(sensors_dir, filename)
                available_sensors.append(path)
        return available_sensors

    @staticmethod
    def select_sensor(app, module_name):
        """Handles sensor selection."""
        sensor_class = load_sensor_dynamically(module_name)
        if sensor_class:
            app.load_sensor(sensor_class)
            print(f"Selected sensor: {module_name}")
            app.sensor_import_screen.imported_sensor_name = module_name
