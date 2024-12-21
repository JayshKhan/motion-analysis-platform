import pygame
from src.ui.screens.main_menu import MainMenuScreen
from src.ui.screens.environment_editor import EnvironmentEditorScreen
from src.ui.screens.algorithm_selection import AlgorithmSelectionScreen
from src.core.environment import Environment
from src.core.algorithms import random_walk  # Example import

class MAPApp:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Motion Analysis Platform")
        self.clock = pygame.time.Clock()
        self.current_screen = "main_menu"
        self.environment = Environment(50, 40) # Example environment

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def handle_input(self, event):
        if self.current_screen == "main_menu":
            MainMenuScreen.handle_input(self, event)
        elif self.current_screen == "environment_editor":
            EnvironmentEditorScreen.handle_input(self, event)
        elif self.current_screen == "algorithm_selection":
            AlgorithmSelectionScreen.handle_input(self, event)

    def update(self):
        if self.current_screen == "main_menu":
            MainMenuScreen.update(self)
        elif self.current_screen == "environment_editor":
            EnvironmentEditorScreen.update(self)
        elif self.current_screen == "algorithm_selection":
            AlgorithmSelectionScreen.update(self)

    def draw(self):
        self.screen.fill((255, 255, 255))  # White background
        if self.current_screen == "main_menu":
            MainMenuScreen.draw(self)
        elif self.current_screen == "environment_editor":
            EnvironmentEditorScreen.draw(self)
        elif self.current_screen == "algorithm_selection":
            AlgorithmSelectionScreen.draw(self)
        pygame.display.flip()

if __name__ == "__main__":
    app = MAPApp()
    app.run()