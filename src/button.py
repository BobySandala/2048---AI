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
