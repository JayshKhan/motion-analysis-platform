import pygame

from src.core import algorithms


class ExecutionScreen:
    GRID_COLOR = (200, 200, 200)
    OBSTACLE_COLOR = (50, 50, 50)
    START_COLOR = (0, 200, 0)
    GOAL_COLOR = (200, 0, 0)
    PATH_COLOR = (0, 0, 255)

    def __init__(self):
        self.cell_size = 20
        self.start_pos = None
        self.goal_pos = None
        self.path = None
        self.run_button_rect = None
        self.run_button_hovered = False

    def reset(self):
        self.start_pos = None
        self.goal_pos = None
        self.path = None

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
                print(f"Setting start position to ({grid_x}, {grid_y})")
                app.execution_screen.start_pos = (grid_x, grid_y)
            elif not app.execution_screen.goal_pos:
                print(f"Setting goal position to ({grid_x}, {grid_y})")
                app.execution_screen.goal_pos = (grid_x, grid_y)
            elif app.execution_screen.run_button_rect and app.execution_screen.run_button_rect.collidepoint(mouse_pos):
                print("Running algorithm")
                ExecutionScreen.run_algorithm(app)

    @staticmethod
    def update(app):
        mouse_pos = pygame.mouse.get_pos()
        if app.execution_screen.run_button_rect:
            app.execution_screen.run_button_hovered = app.execution_screen.run_button_rect.collidepoint(mouse_pos)

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

        # Draw Start and Goal
        if app.execution_screen.start_pos:
            start_rect = pygame.Rect(app.execution_screen.start_pos[0] * cell_size, app.execution_screen.start_pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, ExecutionScreen.START_COLOR, start_rect)
        if app.execution_screen.goal_pos:
            goal_rect = pygame.Rect(app.execution_screen.goal_pos[0] * cell_size, app.execution_screen.goal_pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, ExecutionScreen.GOAL_COLOR, goal_rect)

        # Draw Path
        if app.execution_screen.path:
            points = [(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2) for x, y in
                      app.execution_screen.path]
            pygame.draw.lines(app.screen, ExecutionScreen.PATH_COLOR, False, points, 3)

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
    def get_cell_size():
        return 20

    @staticmethod
    def run_algorithm(app):
        if app.selected_algorithm_name and app.execution_screen.start_pos and app.execution_screen.goal_pos:
            # Set the start and goal in the environment
            app.environment.set_start(*app.execution_screen.start_pos)
            app.environment.set_goal(*app.execution_screen.goal_pos)

            # Find the selected algorithm class
            selected_algorithm_class = getattr(algorithms, app.selected_algorithm_name)
            print(selected_algorithm_class)

            # Instantiate the algorithm with the sensor if one is selected
            # TODO: This is a bit hacky, we should probably have a better way to pass the sensor to the algorithm
            # TODO: scenerio where algorithm does not require sensor
            if app.selected_sensor:
                planner = selected_algorithm_class(app.selected_sensor)
            else:
                planner = selected_algorithm_class()

            # Run the algorithm
            path = planner.plan(app.environment)
            print(path)
            app.execution_screen.path = path
