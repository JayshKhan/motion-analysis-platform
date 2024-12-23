import pygame

from src.ui.config import BUTTON_HOVER_COLOR, BUTTON_COLOR, TEXT_COLOR


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image.set_alpha(128)  # make the background semi-transparent
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Button:
    """
    A simple button class for Pygame.
    """

    def __init__(self, x, y, width, height, text, font_size=36,
                 normal_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR, action=None):
        """
        Initializes the button.

        Args:
            x: The x-coordinate of the top-left corner.
            y: The y-coordinate of the top-left corner.
            width: The width of the button.
            height: The height of the button.
            text: The text to display on the button.
            font_size: The font size for the text.
            normal_color: The background color in the normal state (tuple: (R, G, B)).
            hover_color: The background color in the hover state (tuple: (R, G, B)).
            text_color: The color of the text (tuple: (R, G, B)).
            action: The function to call when the button is clicked (optional).
        """

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        """
        Draws the button on the screen.

        Args:
            screen: The Pygame surface to draw on.
        """

        # Change color on hover
        current_color = self.hover_color if self.is_hovered else self.normal_color

        # Draw the button rectangle
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Render and draw the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Handles events (e.g., mouse clicks, mouse motion).

        Args:
            event: The Pygame event.
        """

        # Check for mouse hover
        self.is_hovered = self.rect.collidepoint(event.pos)

        # Check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and self.is_hovered:  # Left mouse button

                if self.action:
                    self.action()

    def update(self, mouse_pos):
        """
        Updates the button's state (e.g., hover state).

        Args:
            mouse_pos: The current mouse position (tuple: (x, y)).
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
