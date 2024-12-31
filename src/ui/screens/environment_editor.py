import json
import random
import time
import tkinter as tk
from tkinter import filedialog

import pygame

from src.config import config_instance as CONFIG


class EnvironmentEditorScreen:
    GRID_COLOR = (200, 200, 200)
    OBSTACLE_COLOR = (50, 50, 50)
    START_COLOR = (0, 200, 0)
    GOAL_COLOR = (200, 0, 0)

    def __init__(self):
        self.cell_size = 20
        self.drawing_obstacle = True
        self.erasing_obstacle = False

    @staticmethod
    def handle_input(app, event):
        # Handling the Key Down Event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.current_screen = "main_menu"
            elif event.key == pygame.K_o:
                app.environment_editor_screen.start_drawing_obstacle()
            elif event.key == pygame.K_e:
                app.environment_editor_screen.start_erasing_obstacle()
            elif event.key == pygame.K_c:
                EnvironmentEditorScreen.clear_environment(app)
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                EnvironmentEditorScreen.save_environment(app)
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                EnvironmentEditorScreen.load_environment(app)
            elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                EnvironmentEditorScreen.generate_random_maze(app)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // EnvironmentEditorScreen.get_cell_size()
            grid_y = mouse_pos[1] // EnvironmentEditorScreen.get_cell_size()
            if app.environment_editor_screen.drawing_obstacle:
                app.environment.add_obstacle(grid_x, grid_y)
            elif app.environment_editor_screen.erasing_obstacle:
                if (grid_x, grid_y) in app.environment.obstacles:
                    app.environment.obstacles.remove((grid_x, grid_y))
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // EnvironmentEditorScreen.get_cell_size()
            grid_y = mouse_pos[1] // EnvironmentEditorScreen.get_cell_size()
            if event.buttons[0]: # Left mouse button held
                if app.environment_editor_screen.drawing_obstacle:
                    app.environment.add_obstacle(grid_x, grid_y)
                elif app.environment_editor_screen.erasing_obstacle:
                    if (grid_x, grid_y) in app.environment.obstacles:
                        app.environment.obstacles.remove((grid_x, grid_y))


    @staticmethod
    def update(app):
        pass

    @staticmethod
    def draw(app):
        app.screen.fill((255, 255, 255))  # White background
        cell_size = EnvironmentEditorScreen.get_cell_size()

        # Draw Grid
        for x in range(0, app.screen_width, cell_size):
            pygame.draw.line(app.screen, EnvironmentEditorScreen.GRID_COLOR, (x, 0), (x, app.screen_height))
        for y in range(0, app.screen_height, cell_size):
            pygame.draw.line(app.screen, EnvironmentEditorScreen.GRID_COLOR, (0, y), (app.screen_width, y))

        # Draw Obstacles
        for obs_x, obs_y in app.environment.obstacles:
            rect = pygame.Rect(obs_x * cell_size, obs_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, EnvironmentEditorScreen.OBSTACLE_COLOR, rect)

        # Draw Start and Goal (if set, even though editing)
        if app.environment.start:
            start_rect = pygame.Rect(app.environment.start[0] * cell_size, app.environment.start[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, EnvironmentEditorScreen.START_COLOR, start_rect)
        if app.environment.goal:
            goal_rect = pygame.Rect(app.environment.goal[0] * cell_size, app.environment.goal[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, EnvironmentEditorScreen.GOAL_COLOR, goal_rect)

        # Instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Press ESC to Main Menu",
            "Press 'C' to clear environment",
            "Press 'O' to draw obstacles",
            "Press 'E' to erase obstacles",
            "Ctrl+S to Save Environment",
            "Ctrl+L to Load Environment",
            "Ctrl+R to Generate Random Maze",
        ]
        y_offset = 20
        for line in instructions:
            text = font.render(line, True, (150, 0, 150))
            app.screen.blit(text, (20, y_offset))
            y_offset += 20

    @staticmethod
    def get_cell_size():
        return CONFIG.grid_resolution

    def start_drawing_obstacle(self):
        self.drawing_obstacle = True
        self.erasing_obstacle = False

    def start_erasing_obstacle(self):
        self.drawing_obstacle = False
        self.erasing_obstacle = True

    @staticmethod
    def clear_environment(app):
        app.environment.obstacles = set()
        app.environment.start = None
        app.environment.goal = None
        app.environment.add_boundary()

    @staticmethod
    def save_environment(app):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump({
                        "width": app.environment.width,
                        "height": app.environment.height,
                        "obstacles": list(app.environment.obstacles),
                        "start": app.environment.start,
                        "goal": app.environment.goal
                    }, f, indent=4)
                print(f"Environment saved to {file_path}")
            except Exception as e:
                print(f"Error saving environment: {e}")

    @staticmethod
    def load_environment(app):

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    app.environment.width = data.get("width", app.environment.width)
                    app.environment.height = data.get("height", app.environment.height)
                    app.environment.obstacles = set(tuple(obs) for obs in data.get("obstacles", []))
                    app.environment.start = tuple(data.get("start")) if data.get("start") else None
                    app.environment.goal = tuple(data.get("goal")) if data.get("goal") else None
                print(f"Environment loaded from {file_path}")
            except Exception as e:
                print(f"Error loading environment: {e}")

    @staticmethod
    def generate_random_maze(app, density=0.3, animate=False):
        """
        Generates a random maze or obstacle layout based on the given density.

        Parameters:
            app: The main app instance.
            density (float): The proportion of the grid to fill with obstacles (0 to 1).
            animate (bool): Whether to animate the maze generation process.
        """
        if not (0 <= density <= 1):
            print("Density must be between 0 and 1.")
            return

        app.environment.obstacles = set()

        cells = [(x, y) for x in range(app.environment.width) for y in range(app.environment.height)]
        random.shuffle(cells)

        for x, y in cells:
            if random.random() < density:
                # Avoid placing obstacles at start and goal positions
                if (x, y) != app.environment.start and (x, y) != app.environment.goal:
                    app.environment.obstacles.add((x, y))

                    if animate:
                        EnvironmentEditorScreen.draw(app)
                        pygame.display.flip()
                        time.sleep(0.001)  # Adjust delay for speed of animation

        app.environment.add_boundary()
        print(f"Random maze generated with density {density}.")
