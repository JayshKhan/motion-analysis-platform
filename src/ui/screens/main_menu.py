import pygame

from src.config import config_instance as CONFIG
from src.ui.assets import Background


class MainMenuScreen:


    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            app.environment_button_rect.handle_event(event)
            app.sensor_button_rect.handle_event(event)
            app.algorithm_button_rect.handle_event(event)


    @staticmethod
    def update(app):
        mouse_pos = pygame.mouse.get_pos()
        app.environment_button_rect.update(mouse_pos)
        app.sensor_button_rect.update(mouse_pos)
        app.algorithm_button_rect.update(mouse_pos)


    @staticmethod
    def draw(app):
        app.screen.fill((240, 240, 240))  # Light gray background
        font_title = pygame.font.Font(None, 64)
        font_button = pygame.font.Font(None, 36)

        BackGround = Background('../assets/background.jpg', [0, 0])
        app.screen.fill([255, 255, 255])
        app.screen.blit(BackGround.image, BackGround.rect)

        logo = pygame.image.load('../assets/logo.png')
        logo = pygame.transform.scale(logo, (300, 300))
        app.screen.blit(logo, (0, app.screen_height - 200))

        # Title
        title_text = font_title.render("Motion Analysis Platform", True, CONFIG.title_color)
        title_rect = title_text.get_rect(center=(app.screen_width // 2, 100))
        app.screen.blit(title_text, title_rect)

        app.environment_button_rect.draw(app.screen)
        app.sensor_button_rect.draw(app.screen)
        app.algorithm_button_rect.draw(app.screen)
