import pygame

from src.config import config_instance as CONFIG


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
                 normal_color=CONFIG.button_color, hover_color=CONFIG.button_hover_color, text_color=CONFIG.text_color,
                 action=None):
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
        if event.pos:
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


class ColorPicker:
    def __init__(self, position, swatch_size=25, title="Select Color", colors=None, initial_color=(255, 255, 255),
                 action=None):
        """
        Initializes the ColorPickerComponent.

        Args:
            position (tuple): The (x, y) coordinates of the top-left corner of the color picker.
            swatch_size (int): The size (width and height) of each color swatch.
            colors (list of tuples): A list of RGB color tuples for the swatches.
                                     If None, a default set of basic colors will be used.
            initial_color (tuple): The initially selected RGB color tuple.
        """
        self.position = position
        self.swatch_size = swatch_size
        self.selected_color = initial_color
        self.colors = colors or [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (0, 255, 255), (255, 0, 255),
            (255, 255, 255), (0, 0, 0),
            (192, 192, 192), (128, 128, 128), (24, 115, 119), (24, 150, 119), (0, 180, 0, 50)
        ]
        self.calculate_swatch_rects()
        self.title = title
        self.action = action

    def calculate_swatch_rects(self):
        """Calculates the Rect objects for each color swatch."""
        self.swatch_rects = []
        x, y = self.position
        for i, color in enumerate(self.colors):
            rect = pygame.Rect(x + i * (self.swatch_size + 2), y, self.swatch_size, self.swatch_size)
            self.swatch_rects.append((rect, color))

    def handle_event(self, event):
        """Handles mouse click events for the color picker."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if self.action:
                    print(f" {self.title} clicked")
                    self.action()
                    # setattr(CONFIG, self.title, self.selected_color)
                for rect, color in self.swatch_rects:
                    if rect.collidepoint(mouse_pos):
                        self.selected_color = color
                        return True  # Indicate a color was selected
        return False

    def update(self, *args, **kwargs):
        """Optional update method (can be used for animations or dynamic behavior)."""
        pass  # No specific update logic needed for this simple picker

    def draw(self, screen):
        """Draws the color picker on the screen."""
        # title
        font = pygame.font.Font(None, 36)
        title_text = font.render(self.title, True, (0, 0, 0))
        title_rect = title_text.get_rect(x=20, y=self.position[1])
        screen.blit(title_text, title_rect)

        for rect, color in self.swatch_rects:
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Outline

            # Indicate the selected color (optional)
            if color == self.selected_color:
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # Highlight

    def get_selected_color(self):
        """Returns the currently selected color."""
        return self.selected_color
