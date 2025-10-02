import pygame

class Button:
    def __init__(self, rect, color, text, font, text_color=(0,0,0), action=None):
        """
        rect: pygame.Rect(x, y, width, height)
        color: button background
        text: string displayed on button
        font: pygame.font.Font object
        text_color: color of text
        action: callable to run when button is clicked
        """
        self.rect = rect
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


class NumberInputBox:
    def __init__(self, x, y, w, h, font, initial_text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (255, 127, 80)
        self.color_active = (50, 50, 50)
        self.color = self.color_inactive
        self.font = font
        self.text = initial_text
        self.active = False
        self.finished = False  # True when user presses Enter

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside box
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.finished = True
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():  # only allow numbers
                self.text += event.unicode

    def draw(self, screen):
        # Draw rectangle
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Draw text
        txt_surface = self.font.render(self.text, True, self.color)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_value(self):
        """Return the number as int, or None if empty."""
        if self.text == "":
            return None
        return int(self.text)

    def reset(self):
        self.text = ""
        self.active = False
        self.finished = False
        self.color = self.color_inactive
