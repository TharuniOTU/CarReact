# import necessary libraries
import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
from functions import * 
from car import *
from object import *
from simulation import *

# set up preset values
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 0)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)

# Intializing Screen #
win_width = 1050 
win_height = 650  

def to_screen(x, y, win_width, win_height):
    return win_width//2 + x, win_height//2 - y

def from_screen(x, y, win_width, win_height):
    return x - win_width//2, win_height//2 - y

# Main function #
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

    # fixed y pos


    # car object
    car_image = "images/car-sprites/car1.png"
    car_size = [1004, 450]
    fixed_y = win_height-car_size[1]/2
    # Average weight of a car stat: https://www.capitalone.com/cars/learn/finding-the-right-car/how-much-does-a-car-weigh/1248
    car = Car(4000, car_image, car_size, 2.5, [0,fixed_y,0,0], [win_width, win_height])
    car.reset_car()

    # box object
    box_image = "images/box-sprites/box.png"
    box_size = [500, 470]
    box = Object(200, box_image, box_size, 2.5, [0,fixed_y,0,0], [win_width, win_height])
    box.reset_box()

    # set up drawing canvas
    screen_size = (win_width, win_height)
    screen = pygame.display.set_mode(screen_size)
    screen.blit(background, [0, 0])
    pygame.display.set_caption(title)

    # setting up simulation
    sim = Simulation(title)
    sim.init(state1=np.array([10,10,0,0], dtype='float32'), state2=np.array([20,-2,0,0], dtype='float32'), mass1=4000., mass2 = 200.)
    sim.set_time(0.0)
    sim.set_dt(0.1)

    # display to screen
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
            car.update(frame)
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            break
        else:
            pass

        # Display items onto the screen
        screen.blit(background, [0, 0])
        screen.blit(car.get_car(), (car.get_pos()[0], car.get_pos()[1]))
        screen.blit(box.get_obj(), (box.get_pos()[0], box.get_pos()[1])) 

        frame += 1
        # text.draw("Time = %f" % sim.cur_time, screen, (5,5))

        # update simulation
        if not sim.paused:
            sim.step()
            car.update(frame)
        else:
            pass

        pygame.display.flip()
    
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()