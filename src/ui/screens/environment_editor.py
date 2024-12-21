import pygame


class EnvironmentEditorScreen():
    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.current_screen = "main_menu"

    @staticmethod
    def update(app):
        pass

    @staticmethod
    def draw(app):
        app.environment.draw(app.screen)
        pygame.display.flip()