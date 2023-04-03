import pygame, sys

# Class that creates rectangles
class MyRect(pygame.sprite.Sprite):
    def __init__(self, color, width, height, alpha=255):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, self.rect)

        self.picked = False

    def set_pos(self, pos):
        self.rect.x = pos[0] - self.rect.width//2
        self.rect.y = pos[1] - self.rect.height//2

    def update(self):
        pass

# Class that creates text on screen
class MyText():
    def __init__(self, color, background, antialias=True, fontname="comicsansms", fontsize=16):
        pygame.font.init()
        self.font = pygame.font.SysFont(fontname, fontsize)
        self.color = color
        self.background = background
        self.antialias = antialias
    
    def draw(self, str1, screen, pos):
        text = self.font.render(str1, self.antialias, self.color, self.background)
        screen.blit(text, pos)
