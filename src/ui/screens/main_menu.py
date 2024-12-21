import pygame

class MainMenuScreen:
    @staticmethod
    def handle_input(app, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Example: Check for clicks on "Environment Editor" button
            if 100 < mouse_pos[0] < 300 and 100 < mouse_pos[1] < 150:
                app.current_screen = "environment_editor"
            elif 100 < mouse_pos[0] < 300 and 200 < mouse_pos[1] < 250:
                app.current_screen = "algorithm_selection"

    @staticmethod
    def update(app):
        pass

    @staticmethod
    def draw(app):
        font = pygame.font.Font(None, 36)
        text = font.render("Main Menu", True, (0, 0, 0))
        app.screen.blit(text, (app.screen_width // 2 - text.get_width() // 2, 50))

        # Example buttons (very basic)
        pygame.draw.rect(app.screen, (0, 128, 255), (100, 100, 200, 50))
        text_editor = font.render("Environment Editor", True, (255, 255, 255))
        app.screen.blit(text_editor, (110, 110))

        pygame.draw.rect(app.screen, (0, 128, 255), (100, 200, 200, 50))
        text_algo = font.render("Select Algorithm", True, (255, 255, 255))
        app.screen.blit(text_algo, (110, 210))