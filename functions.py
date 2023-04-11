import pygame, sys
from scipy.stats import chi2_contingency 

# read a file
def read_file(file_name):
    file_data = []
    read_file = open(file_name, 'r')
    read_str = read_file.readlines()

    for line in read_str:
        if(line != "EOF"):
            file_data.append(float(line))
        else:
            continue
    return file_data

def write_file(file_name,list_name):
    #write to the rand_pos_list_file
    with open(file_name, 'w') as f:
        for x in list_name:
            f.write(str(x)+ "\n")
        f.write("EOF")


# Test to check if there's a correlation between 2 sets of numbers
def chi_test(expected, actual, sig_level):
    stat, p, dof, expected = chi2_contingency(expected, actual) 
    # retrieve values using builin chi tester
    # if p is greater than the significance level, then the null hypothesis stands
    if p > sig_level: 
        return True
    else: 
        return False

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

expcted_result1 = True
expcted_result2 = True