import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, size, pos):
        super().__init__()
        self.font = pygame.font.Font("font/Fyodor-BoldExpanded.ttf", size)
        self.surf = self.font.render(text, False, color)
        self.rect = self.surf.get_rect(midtop = pos)

class Score(Text):
    def __init__(self, text, color, size, pos):
        self.text = text
        super().__init__(text, color, size, pos)
    def set_score(self, new_text, color):
        self.text = new_text
        self.surf = self.font.render(new_text, False, color)
        