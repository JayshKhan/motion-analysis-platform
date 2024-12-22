import time

import pygame

from src.core import algorithms


class ExecutionScreen:
    GRID_COLOR = (200, 200, 200)
    OBSTACLE_COLOR = (50, 50, 50)
    START_COLOR = (0, 200, 0)
    GOAL_COLOR = (200, 0, 0)
    PATH_COLOR = (0, 0, 255)
    EXPLORED_COLOR = (200, 200, 0)  # Color for explored cells
    START_TREE_COLOR = (0, 0, 255)  # Color for the start tree (Bidirectional RRT)
    GOAL_TREE_COLOR = (255, 0, 0)  # Color for the goal tree (Bidirectional RRT)
    SENSOR_RANGE_COLOR = (0, 180, 0, 50)  # Semi-transparent green for sensor range

    def __init__(self):
        self.cell_size = 20
        self.start_pos = None
        self.goal_pos = None
        self.path = None
        self.run_button_rect = None
        self.run_button_hovered = False
        self.algorithm_generator = None  # Store the algorithm generator
        self.animation_speed = 0.05  # Adjust for visualization speed
        self.last_update_time = 0
        self.explored_cells = []
        self.start_tree_nodes = []  # Store nodes for visualization in Bidirectional RRT
        self.goal_tree_nodes = []
        self.nodes = []  # Initialize nodes here

    def reset(self):
        self.start_pos = None
        self.goal_pos = None
        self.path = None
        self.algorithm_generator = None
        self.explored_cells = []
        self.start_tree_nodes = []
        self.goal_tree_nodes = []

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
            elif app.execution_screen.run_button_rect and app.execution_screen.run_button_rect.collidepoint(mouse_pos):
                ExecutionScreen.run_algorithm(app)


    @staticmethod
    def update(app):
        if app.execution_screen.algorithm_generator:
            current_time = time.time()
            if current_time - app.execution_screen.last_update_time > app.execution_screen.animation_speed:
                try:
                    result = next(app.execution_screen.algorithm_generator)
                    if app.selected_algorithm_name == "BidirectionalRRTPlanner":
                        # Special handling for Bidirectional RRT
                        app.execution_screen.start_tree_nodes, app.execution_screen.goal_tree_nodes = result
                        app.execution_screen.explored_cells.extend(
                            [(node.x, node.y) for node in app.execution_screen.start_tree_nodes])
                        app.execution_screen.explored_cells.extend(
                            [(node.x, node.y) for node in app.execution_screen.goal_tree_nodes])
                        # Remove duplicates
                        app.execution_screen.explored_cells = list(set(app.execution_screen.explored_cells))
                    elif app.selected_algorithm_name == "RRTPlanner":
                        # Update nodes for RRT visualization
                        app.execution_screen.nodes = result
                        # app.execution_screen.explored_cells.extend([(node.x, node.y) for node in app.execution_screen.nodes])
                        # app.execution_screen.explored_cells = list(set(app.execution_screen.explored_cells))
                    else:
                        # For other algorithms, assume the result is the path
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
            pygame.draw.line(app.screen, ExecutionScreen.GRID_COLOR, (x, 0), (x, app.screen_height))
        for y in range(0, app.screen_height, cell_size):
            pygame.draw.line(app.screen, ExecutionScreen.GRID_COLOR, (0, y), (app.screen_width, y))

        # Draw Obstacles
        for obs_x, obs_y in app.environment.obstacles:
            rect = pygame.Rect(obs_x * cell_size, obs_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, ExecutionScreen.OBSTACLE_COLOR, rect)

        # Draw Explored Cells
        for explored_x, explored_y in app.execution_screen.explored_cells:
            rect = pygame.Rect(explored_x * cell_size, explored_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, ExecutionScreen.EXPLORED_COLOR, rect)

        # Draw Start and Goal
        if app.execution_screen.start_pos:
            start_rect = pygame.Rect(app.execution_screen.start_pos[0] * cell_size,
                                     app.execution_screen.start_pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, ExecutionScreen.START_COLOR, start_rect)
        if app.execution_screen.goal_pos:
            goal_rect = pygame.Rect(app.execution_screen.goal_pos[0] * cell_size,
                                    app.execution_screen.goal_pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, ExecutionScreen.GOAL_COLOR, goal_rect)

        # Draw Path
        if app.execution_screen.path:
            points = [(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2) for x, y in
                      app.execution_screen.path]
            if len(points) > 1:
                pygame.draw.lines(app.screen, ExecutionScreen.PATH_COLOR, False, points, 3)

        # Draw RRT Tree
        if app.selected_algorithm_name == "RRTPlanner" and app.execution_screen.nodes:
            for node in app.execution_screen.nodes:
                if node.parent:
                    pygame.draw.line(app.screen, ExecutionScreen.PATH_COLOR,
                                     (node.parent.x * cell_size + cell_size // 2,
                                      node.parent.y * cell_size + cell_size // 2),
                                     (node.x * cell_size + cell_size // 2, node.y * cell_size + cell_size // 2), 2)

            # Draw Bidirectional RRT Trees
        if app.selected_algorithm_name == "BidirectionalRRTPlanner":
            for node in app.execution_screen.start_tree_nodes:
                if node.parent:
                    pygame.draw.line(app.screen, ExecutionScreen.START_TREE_COLOR,
                                     (node.parent.x * cell_size + cell_size // 2,
                                      node.parent.y * cell_size + cell_size // 2),
                                     (node.x * cell_size + cell_size // 2, node.y * cell_size + cell_size // 2), 2)
            for node in app.execution_screen.goal_tree_nodes:
                if node.parent:
                    pygame.draw.line(app.screen, ExecutionScreen.GOAL_TREE_COLOR,
                                     (node.parent.x * cell_size + cell_size // 2,
                                      node.parent.y * cell_size + cell_size // 2),
                                     (node.x * cell_size + cell_size // 2, node.y * cell_size + cell_size // 2), 2)

        # Draw Run Button
        if app.execution_screen.start_pos and app.execution_screen.goal_pos:
            button_width = 100
            button_height = 40
            button_x = app.screen_width - button_width - 10
            button_y = app.screen_height - button_height - 10
            app.execution_screen.run_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_color = (0, 150, 255) if app.execution_screen.run_button_hovered else (0, 128, 255)
            pygame.draw.rect(app.screen, button_color, app.execution_screen.run_button_rect)

            font = pygame.font.Font(None, 24)
            text = font.render("Run", True, (255, 255, 255))
            text_rect = text.get_rect(center=app.execution_screen.run_button_rect.center)
            app.screen.blit(text, text_rect)

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
        pygame.draw.circle(range_surface, ExecutionScreen.SENSOR_RANGE_COLOR, (center_x, center_y),
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
            # Reset tree nodes for Bidirectional RRT and RRT
            if app.selected_algorithm_name == "BidirectionalRRTPlanner":
                app.execution_screen.start_tree_nodes = []
                app.execution_screen.goal_tree_nodes = []
            elif app.selected_algorithm_name == "RRTPlanner":
                app.execution_screen.nodes = []
