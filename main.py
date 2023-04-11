"""
Project: Car Collision Detection & Response
Name: Tharuni Iranjan, 100694352
Course: CSCI3010 Simulation & Modelling 
Professor: Dr Faisal Quershi
Date: April 10, 2022
"""

"""
Main Function
Handles user interaction and calls on necessary classes to run the simulation
"""

# import necessary libraries
import pygame, sys
import numpy as np
import random
from functions import * 
from simulation import *

# Intializing Screen #
win_width = 1050 
win_height = 650  

# set up preset values
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 0)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)

# screen func
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

    # set up drawing canvas
    screen_size = (win_width, win_height)
    screen = pygame.display.set_mode(screen_size)
    screen.blit(background, [0, 0])
    pygame.display.set_caption(title)

    # intitialize collision detection to automatic or manual
    # NOTE to change to automatic, change the commented lines
    auto_or_man = "M"
    # auto_or_man = "A"

    # car object
    car_image = "images/car-sprites/car1.png"
    car_size = [1004, 450]
    fixed_y = win_height-car_size[1]/2
    # box object
    box_image = "images/box-sprites/box.png"
    box_size = [500, 470]
    # setting up simulation
    sim = Simulation(title)
    sim.init([win_width, win_height], 4000, car_image, car_size, 2.5, [0,fixed_y,0,0], 200, box_image, box_size, 3, [0,fixed_y,0,0], auto_or_man)


    # display to screen
    print ('--------------------------------')
    print ('Usage:')
    print ('Press (r) to start the car')
    print ('Press (b) to apply breaks')
    print ('Press (q) to quit')
    print ('--------------------------------')

    # Transformation to screen coordinates
    # Here 0,0 refers to simulation coordinates
    # center.set_pos(to_screen(0, 0, win_width, win_height))

    while True:
        # 30 fps
        clock.tick(30)

        # update sprite x, y position using values returned from the simulation
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            sim.resume()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            sim.slowDown()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sim.save()
            break
        else:
            pass

        # Display items onto the screen
        screen.blit(background, [0, 0])
        screen.blit(sim.get_car().get_img(), (sim.get_car().get_state()[0], sim.get_car().get_state()[1]))
        screen.blit(sim.get_box().get_img(), (sim.get_box().get_state()[0], sim.get_box().get_state()[1])) 

        frame += 1

        # update simulation
        if not sim.paused:
            sim.step(frame)
        else:
            pass

        pygame.display.flip()
    
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
