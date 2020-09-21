import pygame

class Button:
    BUTTON_COLOR = 133,168,164,255
    TEXT_COLOR = 0,0,0,255

    def __init__(self, text, font, x, y, width, height):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, Button.BUTTON_COLOR, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", self.font)
        text = font.render(self.text, 1, Button.TEXT_COLOR)
        win.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + self.height // 2 - text.get_height() // 2))

    def click(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

