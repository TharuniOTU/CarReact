# import necessary libraries
import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
from functions import * 
from cars import *

# set up preset values
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 0)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)

#intializing frames
frame = 0

# load images
car1 = pygame.image.load("images/car-sprites/car1.png")
car2 = pygame.image.load("images/car-sprites/car2.png")
car3 = pygame.image.load("images/car-sprites/car3.png")
car4 = pygame.image.load("images/car-sprites/car4.png")
car5 = pygame.image.load("images/car-sprites/car5.png")
car6 = pygame.image.load("images/car-sprites/car6.png")
car7 = pygame.image.load("images/car-sprites/car7.png")
car_list = [car1, car2, car3, car4, car5, car6, car7]

win_width = 1050 
win_height = 650  

def to_screen(x, y, win_width, win_height):
    return win_width//2 + x, win_height//2 - y

def from_screen(x, y, win_width, win_height):
    return x - win_width//2, win_height//2 - y

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
        pass
    
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

    #intializing frame
    frame = 0 
    clock = pygame.time.Clock()

    # initializing pygame
    pygame.init()

    # setting up necessary variables
    title = 'Car Collision Stimulation'
    text = MyText(WHITE, BLACK)   
    background = pygame.image.load("images/backgrounds/background3.jpg")
    background = pygame.transform.scale(background, (win_width, win_height))
    center = MyRect(color=BLACK, width=4, height=4)
    x_axis = MyRect(color=BLACK, width=620, height=1)
    y_axis = MyRect(color=BLACK, width=1, height=460)

    # car
    car_image = pygame.image.load("images/car-sprites/car1.png") 
    car_width = 1004
    car_height = 450
    car_ratio = 2.5
    car_image = pygame.transform.scale(car_image, (car_width/car_ratio, car_height/car_ratio))
    car_rect = car_image.get_rect() 
    car_x = 0 
    car_y = win_height - car_height/2 
    my_group = pygame.sprite.Group([center, x_axis, y_axis])
    #  mass, size, state, dt, dv, pic_arr
    car = Car(4000, [car_width/car_ratio, car_height/car_ratio], [car_x, car_y, 5, 0], dt=0.33, dv=3, pic_arr=car_list)

    # set up drawing canvas
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
        car.animation(screen,frame)
        screen.blit(background, [0, 0])
        screen.blit(car_image, (car_x, car_y)) 
        my_group.update()
        my_group.draw(screen)

        frame += 1
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