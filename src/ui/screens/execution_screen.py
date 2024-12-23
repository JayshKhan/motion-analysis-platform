import time

import pygame

from src.core import algorithms
from src.ui.assets import Button
from src.ui.config import GRID_COLOR, OBSTACLE_COLOR, START_COLOR, GOAL_COLOR, PATH_COLOR, EXPLORED_COLOR, \
    SENSOR_RANGE_COLOR


# from pygame.examples.go_over_there import reset

class ExecutionScreen:

    def __init__(self):
        self.cell_size = 20
        self.start_pos = None
        self.goal_pos = None
        self.path = None
        self.run_button_rect = None
        self.run_button_hovered = False
        self.reset_button_rect = None
        self.algorithm_generator = None  # Store the algorithm generator
        self.animation_speed = 0.05  # Adjust for visualization speed
        self.last_update_time = 0
        self.explored_cells = []
        self.nodes = []  # Initialize nodes here

    def reset(self):
        self.start_pos = None
        self.goal_pos = None
        self.path = None
        self.algorithm_generator = None
        self.explored_cells = []


    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.current_screen = "main_menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // ExecutionScreen.get_cell_size()
            grid_y = mouse_pos[1] // ExecutionScreen.get_cell_size()
            if not app.execution_screen.start_pos:
                app.execution_screen.start_pos = (grid_x, grid_y)
            elif not app.execution_screen.goal_pos:
                app.execution_screen.goal_pos = (grid_x, grid_y)
            elif app.execution_screen.run_button_rect and app.execution_screen.run_button_rect.rect.collidepoint(
                    mouse_pos):
                app.execution_screen.run_button_rect.handle_event(event)
            elif app.execution_screen.reset_button_rect and app.execution_screen.reset_button_rect.rect.collidepoint(
                    mouse_pos):
                app.execution_screen.reset_button_rect.handle_event(event)


    @staticmethod
    def update(app):
        if app.execution_screen.algorithm_generator:
            current_time = time.time()
            if current_time - app.execution_screen.last_update_time > app.execution_screen.animation_speed:
                try:
                    result = next(app.execution_screen.algorithm_generator)

                    app.execution_screen.path = result
                    app.execution_screen.explored_cells.extend(app.execution_screen.path)
                    # Remove duplicates
                    app.execution_screen.explored_cells = list(set(app.execution_screen.explored_cells))
                    app.execution_screen.last_update_time = current_time
                except StopIteration:
                    app.execution_screen.algorithm_generator = None  # Algorithm finished

    @staticmethod
    def draw(app):
        app.screen.fill((255, 255, 255))  # White background
        cell_size = ExecutionScreen.get_cell_size()

        # Draw Grid
        for x in range(0, app.screen_width, cell_size):
            pygame.draw.line(app.screen, GRID_COLOR, (x, 0), (x, app.screen_height))
        for y in range(0, app.screen_height, cell_size):
            pygame.draw.line(app.screen, GRID_COLOR, (0, y), (app.screen_width, y))

        # Draw Obstacles
        for obs_x, obs_y in app.environment.obstacles:
            rect = pygame.Rect(obs_x * cell_size, obs_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, OBSTACLE_COLOR, rect)

        # Draw Explored Cells
        for explored_x, explored_y in app.execution_screen.explored_cells:
            rect = pygame.Rect(explored_x * cell_size, explored_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, EXPLORED_COLOR, rect)

        # Draw Start and Goal
        if app.execution_screen.start_pos:
            start_rect = pygame.Rect(app.execution_screen.start_pos[0] * cell_size,
                                     app.execution_screen.start_pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, START_COLOR, start_rect)
        if app.execution_screen.goal_pos:
            goal_rect = pygame.Rect(app.execution_screen.goal_pos[0] * cell_size,
                                    app.execution_screen.goal_pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, GOAL_COLOR, goal_rect)

        # Draw Path
        if app.execution_screen.path:
            points = [(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2) for x, y in
                      app.execution_screen.path]
            if len(points) > 1:
                pygame.draw.lines(app.screen, PATH_COLOR, False, points, 3)



        # Draw Run Button
        if app.execution_screen.start_pos and app.execution_screen.goal_pos:
            button_width = 100
            button_height = 40
            button_x = app.screen_width - button_width - 10
            button_y = app.screen_height - button_height - 10
            app.execution_screen.run_button_rect = Button(
                button_x,
                button_y,
                button_width,
                button_height,
                "Run",
                action=lambda: ExecutionScreen.run_algorithm(app),
            )
            app.execution_screen.run_button_rect.draw(app.screen)

            # Reset Button
            app.execution_screen.reset_button_rect = Button(
                button_x,
                button_y - button_height - 10,
                button_width,
                button_height,
                "Reset",
                action=lambda: app.execution_screen.reset(),
            )
            app.execution_screen.reset_button_rect.draw(app.screen)

            # font = pygame.font.Font(None, 24)
            # text = font.render("Run", True, (255, 255, 255))
            # text_rect = text.get_rect(center=app.execution_screen.run_button_rect.rect.center)
            # app.screen.blit(text, text_rect)

        # Draw Sensor Range (if applicable)
        if app.selected_sensor and app.execution_screen.path:
            current_position = app.execution_screen.path[-1]  # Get last position in path
            sensor_range = app.selected_sensor.range_limit  # Assuming a 'range_limit' attribute
            ExecutionScreen.draw_sensor_range(app.screen, current_position, sensor_range,
                                              app.execution_screen.cell_size)

        # Instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Press ESC to Main Menu",
            "Click to set start position (green)",
            "Click to set goal position (red)",
            "Click 'Run' to execute the algorithm",

        ]
        y_offset = 10
        for line in instructions:
            text = font.render(line, True, (0, 0, 0))
            app.screen.blit(text, (10, y_offset))
            y_offset += 20

    @staticmethod
    def draw_sensor_range(screen, position, range_limit, cell_size):
        # Create a surface for the sensor range (for transparency)
        range_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

        # Calculate the center of the current position in pixel coordinates
        center_x = int(position[0] * cell_size + cell_size / 2)
        center_y = int(position[1] * cell_size + cell_size / 2)

        # Draw a circle to represent the sensor's range
        pygame.draw.circle(range_surface, SENSOR_RANGE_COLOR, (center_x, center_y),
                           int(range_limit * cell_size))

        # Blit the sensor range surface onto the main screen
        screen.blit(range_surface, (0, 0))

    @staticmethod
    def get_cell_size():
        return 20

    @staticmethod
    def run_algorithm(app):
        if app.selected_algorithm_name and app.execution_screen.start_pos and app.execution_screen.goal_pos:
            app.environment.set_start(*app.execution_screen.start_pos)
            app.environment.set_goal(*app.execution_screen.goal_pos)
            selected_algorithm_class = getattr(algorithms, app.selected_algorithm_name)

            if app.selected_sensor:
                planner = selected_algorithm_class(app.selected_sensor)
            else:
                planner = selected_algorithm_class()

            app.execution_screen.algorithm_generator = planner.plan(app.environment)
            app.execution_screen.explored_cells = []
