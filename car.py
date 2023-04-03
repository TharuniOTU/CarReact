import numpy as np
import pygame, sys

# load images
car1 = pygame.image.load("images/car-sprites/car1.png")
car2 = pygame.image.load("images/car-sprites/car2.png")
car3 = pygame.image.load("images/car-sprites/car3.png")
car4 = pygame.image.load("images/car-sprites/car4.png")
car5 = pygame.image.load("images/car-sprites/car5.png")
car6 = pygame.image.load("images/car-sprites/car6.png")
car7 = pygame.image.load("images/car-sprites/car7.png")
car_list = [car1, car2, car3, car4, car5, car6, car7]
MAX_COLL = 3

# Car class
class Car(pygame.sprite.Sprite):
    
    def __init__(self, weight, image, car_size, ratio, state, screen_size):
        self.car_size = car_size
        self.screen_size = screen_size
        self.state = state
        self.y = self.state[1]
        self.weight = weight
        self.ratio = ratio
        self.curr_time = 0
        # change in time, and velocity
        self.dt = 0.33
        self.dv = np.array([20., 0.])
        # setting up collision 
        self.tol_screen_right = screen_size[0] 
        self.tol_object_dist = self.car_size[0]/2
        self.collision_tpye = 0
        self.collision_num = 0

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
        self.curr_car_img = car_list[index]
        self.car = self.curr_car_img
        self.car = pygame.transform.scale(self.car, (self.car_size[0]/self.ratio, self.car_size[1]/self.ratio))

    def get_car(self):
        return self.car
    
    def get_size(self):
        return self.car_size
    
    def get_pos(self):
        return self.state

    def set_pos(self, pos):
        self.state[0] = pos - self.car_size[0]//2
        self.state[1] = pos - self.car_size[1]//2

    def reset_car(self):
        self.state = [-(self.car_size[0]/self.ratio)/2,self.y,0,0]

    def compute_dist(self, input1, input2):
        return abs(input1[1] - input2[1])
    
    # TO DO: fix this is collision
    def is_coll(self, input1, input2):
        # if x pos of car exceeds the right side of the screen
        if (input1[0] >= self.tol_screen_right):
            self.collision_tpye = 1
        # TO DO: if dist between car and obj exceeds threshold, collision occured
        # elif (self.compute_dist(input1,input2) <= self.tol_object_dist):
        #     self.collision_tpye = 2
        # no collision
        else:
            self.collision_tpye = 0
        return self.collision_tpye

    def update(self,frames):
        default = np.zeros(4, dtype='float32')
        force1 = self.dv * self.dt
        new_state1 = np.zeros(4, dtype='float32')
        new_state1[:2] = self.state[:2] +  force1
        new_state1[2] = self.state[2] + (self.state[0] / self.dt)

        # Check if collision occured first then update simulation
        if (self.collision_num <= MAX_COLL):
            if (self.is_coll(new_state1, default) == 0):
                self.state = new_state1
                new_time = self.curr_time + self.dt
                self.curr_time += new_time
                self.update_car_image(frames)
            else:
                self.reset_car()
                self.collision_num += 1