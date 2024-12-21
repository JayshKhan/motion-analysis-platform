import pygame

class EnvironmentEditorScreen:
    GRID_COLOR = (200, 200, 200)
    OBSTACLE_COLOR = (50, 50, 50)
    START_COLOR = (0, 200, 0)
    GOAL_COLOR = (200, 0, 0)

    def __init__(self):
        self.cell_size = 20
        self.drawing_obstacle = False
        self.erasing_obstacle = False
        self.setting_start = False
        self.setting_goal = False

    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.current_screen = "main_menu"
            elif event.key == pygame.K_o:
                app.environment_editor_screen.start_drawing_obstacle()
            elif event.key == pygame.K_e:
                app.environment_editor_screen.start_erasing_obstacle()
            elif event.key == pygame.K_s:
                app.environment_editor_screen.start_setting_start()
            elif event.key == pygame.K_g:
                app.environment_editor_screen.start_setting_goal()
            elif event.key == pygame.K_c:
                EnvironmentEditorScreen.clear_environment(app)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // EnvironmentEditorScreen.get_cell_size()
            grid_y = mouse_pos[1] // EnvironmentEditorScreen.get_cell_size()
            if app.environment_editor_screen.drawing_obstacle:
                app.environment.add_obstacle(grid_x, grid_y)
            elif app.environment_editor_screen.erasing_obstacle:
                if (grid_x, grid_y) in app.environment.obstacles:
                    app.environment.obstacles.remove((grid_x, grid_y))
            elif app.environment_editor_screen.setting_start:
                app.environment.set_start(grid_x, grid_y)
                app.environment_editor_screen.setting_start = False
            elif app.environment_editor_screen.setting_goal:
                app.environment.set_goal(grid_x, grid_y)
                app.environment_editor_screen.setting_goal = False
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
        width = app.environment.width
        height = app.environment.height

        # Draw Grid
        for x in range(0, app.screen_width, cell_size):
            pygame.draw.line(app.screen, EnvironmentEditorScreen.GRID_COLOR, (x, 0), (x, app.screen_height))
        for y in range(0, app.screen_height, cell_size):
            pygame.draw.line(app.screen, EnvironmentEditorScreen.GRID_COLOR, (0, y), (app.screen_width, y))

        # Draw Obstacles
        for obs_x, obs_y in app.environment.obstacles:
            rect = pygame.Rect(obs_x * cell_size, obs_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(app.screen, EnvironmentEditorScreen.OBSTACLE_COLOR, rect)

        # Draw Start and Goal
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
            "Press 'O' to draw obstacles",
            "Press 'E' to erase obstacles",
            "Press 'S' to set start point",
            "Press 'G' to set goal point",
            "Press 'C' to clear environment"
        ]
        y_offset = 10
        for line in instructions:
            text = font.render(line, True, (0, 0, 0))
            app.screen.blit(text, (10, y_offset))
            y_offset += 20

    @staticmethod
    def get_cell_size():
        return 20

    def start_drawing_obstacle(self):
        self.drawing_obstacle = True
        self.erasing_obstacle = False
        self.setting_start = False
        self.setting_goal = False

    def start_erasing_obstacle(self):
        self.drawing_obstacle = False
        self.erasing_obstacle = True
        self.setting_start = False
        self.setting_goal = False

    def start_setting_start(self):
        self.drawing_obstacle = False
        self.erasing_obstacle = False
        self.setting_start = True
        self.setting_goal = False

    def start_setting_goal(self):
        self.drawing_obstacle = False
        self.erasing_obstacle = False
        self.setting_start = False
        self.setting_goal = True

    @staticmethod
    def clear_environment(app):
        app.environment.obstacles = set()
        app.environment.start = None
        app.environment.goal = None