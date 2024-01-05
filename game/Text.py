import pygame

FONT_PATH = "font/Fyodor-BoldExpanded.ttf"

class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, size, pos):
        super().__init__()
        self.font = pygame.font.Font(FONT_PATH, size)
        self.surf = self.font.render(text, False, color)
        self.rect = self.surf.get_rect(midtop = pos)

class Score(Text):
    def __init__(self, text, color, size, pos):
        self.text = text
        self.INIT_SCORE = 0.00
        super().__init__(text, color, size, pos)
    def set_score(self, new_score, color = "black"):
        new_score_2f = "{:.2f}".format(new_score)
        new_text = f"Score: {new_score_2f}"
        self.text = new_text
        self.surf = self.font.render(new_text, False, color)
    def reset(self):
        self.text = f"Score: {self.INIT_SCORE}"      