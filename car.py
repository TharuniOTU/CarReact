"""
Car Class
Defines car attributes like its size, state, weight, etc
Loads the image of the car onto the screen and updates it
Simulation class uses this to update the box's position and velocity 
"""

# import necessary libraries
import pygame, sys 
import numpy as np

car1 = pygame.image.load("images/car-sprites/car1.png")
car2 = pygame.image.load("images/car-sprites/car2.png")
car3 = pygame.image.load("images/car-sprites/car3.png")
car4 = pygame.image.load("images/car-sprites/car4.png")
car5 = pygame.image.load("images/car-sprites/car5.png")
car6 = pygame.image.load("images/car-sprites/car6.png")
car7 = pygame.image.load("images/car-sprites/car7.png")
car_list = [car1, car2, car3, car4, car5, car6, car7]

# Car class
class Car(pygame.sprite.Sprite):
    def __init__(self, weight, image, car_size, ratio, state, screen_size, dv):
        self.car_size = car_size
        self.screen_size = screen_size
        self.state = state
        self.y = self.state[1]
        self.weight = weight
        self.ratio = ratio
        self.curr_img_index = 0
        # change in time, and velocity
        self.dt = 0.33
        self.dv = dv
        
        self.curr_time = 0
        self.image_list = car_list

        # EXTRA
        pygame.sprite.Sprite.__init__(self)
        self.curr_car_img = image
        self.car = pygame.image.load(self.curr_car_img)
        self.car = pygame.transform.scale(self.car, (self.car_size[0]/ratio, self.car_size[1]/ratio))

        # pygame.sprite.Sprite.__init__(self)
        # self.car = pygame.image.load(image)
        # self.car = pygame.transform.scale(self.car, (self.car_size[0]/ratio, self.car_size[1]/ratio))

        # self.image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
        self.picked = False

    # EXTRA
    def update_car_image(self, frames):
        index = frames % 7
        self.curr_car_img = self.image_list[index]
        self.car = self.curr_car_img
        self.car = pygame.transform.scale(self.car, (self.car_size[0]/self.ratio, self.car_size[1]/self.ratio))

    def get_img(self):
        return self.car
    
    def get_size(self):
        return self.car_size
    
    def get_state(self):
        return self.state
    
    def get_dv(self):
        return self.dv

    def set_pos(self, pos):
        self.state[0] = pos - self.car_size[0]//2
        self.state[1] = pos - self.car_size[1]//2

    def set_state(self, new_state):
        self.state = new_state
    
    def set_dv(self, new_dv):
        self.dv = new_dv

    def reset_car(self):
        self.state = [-(self.car_size[0]/self.ratio)/2,self.y,0,0]

    def change_animation_images(self):
        new_list = []
        curr_index = self.curr_img_index
        for i in range(len(self.image_list)):
            new_list.append(self.image_list[curr_index])
            curr_index -= 1
        
        self.image_list = new_list