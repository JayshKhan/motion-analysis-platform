import pygame

class MainMenuScreen:
    BUTTON_COLOR = (0, 128, 255)
    BUTTON_HOVER_COLOR = (0, 150, 255)
    TEXT_COLOR = (255, 255, 255)
    TITLE_COLOR = (0, 0, 0)

    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if app.algorithm_button_rect.collidepoint(mouse_pos):
                app.current_screen = "algorithm_selection"
            elif app.environment_button_rect.collidepoint(mouse_pos):
                app.current_screen = "environment_editor"
            elif app.sensor_button_rect.collidepoint(mouse_pos):
                app.current_screen = "sensor_import"

    @staticmethod
    def update(app):
        mouse_pos = pygame.mouse.get_pos()
        app.algorithm_button_hovered = app.algorithm_button_rect.collidepoint(mouse_pos)
        app.environment_button_hovered = app.environment_button_rect.collidepoint(mouse_pos)
        app.sensor_button_hovered = app.sensor_button_rect.collidepoint(mouse_pos)

    @staticmethod
    def draw(app):
        app.screen.fill((240, 240, 240))  # Light gray background
        font_title = pygame.font.Font(None, 64)
        font_button = pygame.font.Font(None, 36)

        # Title
        title_text = font_title.render("Motion Analysis Platform", True, MainMenuScreen.TITLE_COLOR)
        title_rect = title_text.get_rect(center=(app.screen_width // 2, 100))
        app.screen.blit(title_text, title_rect)

        # Buttons
        button_width = 250
        button_height = 50
        button_spacing = 20
        start_y = 200

        # Environment Editor Button
        app.environment_button_rect = pygame.Rect(
            app.screen_width // 2 - button_width // 2,
            start_y,
            button_width,
            button_height,
        )
        environment_button_color = MainMenuScreen.BUTTON_HOVER_COLOR if app.environment_button_hovered else MainMenuScreen.BUTTON_COLOR
        pygame.draw.rect(app.screen, environment_button_color, app.environment_button_rect)
        environment_text = font_button.render("Environment Editor", True, MainMenuScreen.TEXT_COLOR)
        environment_text_rect = environment_text.get_rect(center=app.environment_button_rect.center)
        app.screen.blit(environment_text, environment_text_rect)

        # Algorithm Selection Button
        app.algorithm_button_rect = pygame.Rect(
            app.screen_width // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width,
            button_height,
        )
        algorithm_button_color = MainMenuScreen.BUTTON_HOVER_COLOR if app.algorithm_button_hovered else MainMenuScreen.BUTTON_COLOR
        pygame.draw.rect(app.screen, algorithm_button_color, app.algorithm_button_rect)
        algorithm_text = font_button.render("Select Algorithm", True, MainMenuScreen.TEXT_COLOR)
        algorithm_text_rect = algorithm_text.get_rect(center=app.algorithm_button_rect.center)
        app.screen.blit(algorithm_text, algorithm_text_rect)

        # Sensor Import Button
        app.sensor_button_rect = pygame.Rect(
            app.screen_width // 2 - button_width // 2,
            start_y + 2 * (button_height + button_spacing),
            button_width,
            button_height,
        )
        sensor_button_color = MainMenuScreen.BUTTON_HOVER_COLOR if app.sensor_button_hovered else MainMenuScreen.BUTTON_COLOR
        pygame.draw.rect(app.screen, sensor_button_color, app.sensor_button_rect)
        sensor_text = font_button.render("Import Sensor Model", True, MainMenuScreen.TEXT_COLOR)
        sensor_text_rect = sensor_text.get_rect(center=app.sensor_button_rect.center)
        app.screen.blit(sensor_text, sensor_text_rect)