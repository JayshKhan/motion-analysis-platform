import pygame
import tkinter as tk
from tkinter import filedialog
import importlib.util
import sys

class SensorImportScreen:
    BUTTON_COLOR = (0, 128, 255)
    BUTTON_HOVER_COLOR = (0, 150, 255)
    TEXT_COLOR = (255, 255, 255)
    INFO_TEXT_COLOR = (0, 0, 0)

    def __init__(self):
        self.import_button_rect = None
        self.import_button_hovered = False
        self.imported_sensor_name = None

    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.current_screen = "main_menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if app.sensor_import_screen.import_button_rect and app.sensor_import_screen.import_button_rect.collidepoint(mouse_pos):
                SensorImportScreen.open_file_dialog(app)

    @staticmethod
    def update(app):
        mouse_pos = pygame.mouse.get_pos()
        if app.sensor_import_screen.import_button_rect:
            app.sensor_import_screen.import_button_hovered = app.sensor_import_screen.import_button_rect.collidepoint(mouse_pos)

    @staticmethod
    def draw(app):
        app.screen.fill((220, 220, 220))  # Light gray background
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        # Title
        title_text = font.render("Import Custom Sensor Model", True, SensorImportScreen.INFO_TEXT_COLOR)
        title_rect = title_text.get_rect(center=(app.screen_width // 2, 100))
        app.screen.blit(title_text, title_rect)

        # Import Button
        button_width = 200
        button_height = 40
        button_x = app.screen_width // 2 - button_width // 2
        button_y = 200
        app.sensor_import_screen.import_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_color = SensorImportScreen.BUTTON_HOVER_COLOR if app.sensor_import_screen.import_button_hovered else SensorImportScreen.BUTTON_COLOR
        pygame.draw.rect(app.screen, button_color, app.sensor_import_screen.import_button_rect)
        import_text = font.render("Import .py File", True, SensorImportScreen.TEXT_COLOR)
        import_text_rect = import_text.get_rect(center=app.sensor_import_screen.import_button_rect.center)
        app.screen.blit(import_text, import_text_rect)

        # Instructions
        instructions = [
            "Press ESC to go back to Main Menu",
            "Click 'Import .py File' to select your sensor model.",
            "Ensure your sensor class inherits from SensorModel.",
        ]
        y_offset = 300
        for line in instructions:
            text = small_font.render(line, True, SensorImportScreen.INFO_TEXT_COLOR)
            text_rect = text.get_rect(center=(app.screen_width // 2, y_offset))
            app.screen.blit(text, text_rect)
            y_offset += 30

        # Display Imported Sensor Name
        if app.imported_sensor_module:
            sensor_name = getattr(app.imported_sensor_module, '__name__', 'Unknown Sensor')
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
            app.imported_sensor_module = module # Store the imported module in app
            print(f"Successfully imported sensor model from: {file_path}")
        except Exception as e:
            print(f"Error importing sensor model: {e}")
            # Optionally display an error message on the screen