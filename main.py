# import necessary libraries
import pygame, sys
import matplotlib.pyplot as plt
import numpy as np

# set up the colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 0)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)

def to_screen(x, y, win_width, win_height):
    return win_width//2 + x, win_height//2 - y

def from_screen(x, y, win_width, win_height):
    return x - win_width//2, win_height//2 - y

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
    def __init__(self, color=WHITE, background=BLACK, antialias=True, fontname="comicsansms", fontsize=16):
        pygame.font.init()
        self.font = pygame.font.SysFont(fontname, fontsize)
        self.color = color
        self.background = background
        self.antialias = antialias
    
    def draw(self, str1, screen, pos):
        text = self.font.render(str1, self.antialias, self.color, self.background)
        screen.blit(text, pos)

# Class that runs the Stimulation
class Simulation:
    def __init__(self, title):
        self.title = title
        self.paused = True
        self.cur_time = 0

    def init(self, state1, state2, mass1, mass2):
        self.state1 = state1
        self.state2 = state2
        self.mass1 = mass1
        self.mass2 = mass2
    
    def set_time(self, cur_time=0):
        self.cur_time = cur_time

    def set_dt(self, dt=0.033):
        self.dt = dt
    
    def step(self):
        self.cur_time += self.dt

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def save(self, filename):
        pass

    def load(self, filename):
        pass

# Main function
def main():
    # clock object that ensure that animation has the same
    # on all machines, regardless of the actual machine speed.
    clock = pygame.time.Clock()

    # initializing pygame
    pygame.init()

    # setting up necessary variables
    title = 'Car Collision Stimulation'
    text = MyText(BLACK)
    background = pygame.image.load("images/background.png")
    center = MyRect(color=BLACK, width=4, height=4)
    x_axis = MyRect(color=BLACK, width=620, height=1)
    y_axis = MyRect(color=BLACK, width=1, height=460)
    my_group = pygame.sprite.Group([x_axis, y_axis, center])

    # set up drawing canvas
    # top left corner is (0,0) top right (640,0) bottom left (0,480)
    # and bottom right is (640,480).
    win_width = 612 #612
    win_height = 408 # 408
    screen_size = (win_width, win_height)
    screen = pygame.display.set_mode(screen_size)
    screen.blit(background, [0, 0])
    pygame.display.set_caption(title)

    # setting up simulation
    # Average weight of a car stat: https://www.capitalone.com/cars/learn/finding-the-right-car/how-much-does-a-car-weigh/1248
    sim = Simulation(title)
    sim.init(state1=np.array([10,10,0,0], dtype='float32'), state2=np.array([20,-2,0,0], dtype='float32'), mass1=4000., mass2 = 200.)
    sim.set_time(0.0)
    sim.set_dt(0.1)

    print ('--------------------------------')
    print ('Usage:')
    print ('Press (r) to start/resume simulation')
    print ('Press (p) to pause simulation')
    print ('Press (q) to quit')
    print ('--------------------------------')

    # Transformation to screen coordinates
    # Here 0,0 refers to simulation coordinates
    # center.set_pos(to_screen(0, 0, win_width, win_height))


    while True:
        # 30 fps
        clock.tick(30)

        # update sprite x, y position using values
        # returned from the simulation
        # background.set_pos(to_screen(0, 0, win_width, win_height))
        
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            sim.pause()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            sim.resume()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            break
        else:
            pass

        # clear the background, and draw the sprites
        # screen.fill(BLACK)
        screen.blit(background, [0, 0])
        my_group.update()
        my_group.draw(screen)
        # text.draw("Time = %f" % sim.cur_time, screen, (5,5))


        # update simulation
        if not sim.paused:
            sim.step()
        else:
            pass

        pygame.display.flip()
    
    pygame.quit()
    sys.exit(0)






if __name__ == '__main__':
    main()