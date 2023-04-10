"""
Object Class
Defines box attributes like its size, state, weight, etc
Loads the image of the box onto the screen and updates it
Simulation class uses this to update the box's position and velocity 
"""


import pygame, sys 
import numpy as np
import random

# Object class for Box
class Object(pygame.sprite.Sprite):
    
    def __init__(self, weight, image, box_size, ratio, state, screen_size, dv):
        self.box_size = box_size
        self.state = state
        self.y = self.state[1]
        self.weight = weight
        self.ratio = ratio
        self.screen_size = screen_size
        self.dv = dv

        pygame.sprite.Sprite.__init__(self)
        self.obj = pygame.image.load(image)
        self.obj = pygame.transform.scale(self.obj, (self.box_size[0]/self.ratio, self.box_size[1]/self.ratio))

        # self.image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
        self.picked = False

    def get_img(self):
        return self.obj
    
    def get_size(self):
        return self.box_size
    
    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        self.state = new_state
    
    def get_dv(self):
        return self.dv
    
    def set_dv(self, new_dv):
        self.dv = new_dv
    
    def gen_rand(self):
        # set up boundaries
        min = self.screen_size[0]/2 
        min_left = min-2
        min_right = min+2
        max = self.screen_size[0] - self.box_size[0]/2
        max_left = max-2
        mid = self.screen_size[0]/2 + self.box_size[0]/2
        mid_left = mid-2
        mid_right = mid+2
        # temp_list = [min, min_left, min_right, max, max_left, mid, mid_right, mid_left]
        # each number and its weights
        prob = {min_left:.5/8., min:1.5/8., min_right:1.25/8., mid_left:1.5/8., mid:1.5/8.,
        mid_right:1./8., max_left:.5/8., max:.25/8.}

        num_list = list(prob.keys())
        num_prob = list(prob.values())
        rand_num = random.choices(num_list, num_prob)
        return rand_num[0]


    def reset_box(self):
        # TO DO: wait a random amount of time before displaying the obj on the screen
        num = self.gen_rand()
        self.state = [num,self.y,0,0]

    def hide_box(self):
        distance = self.screen_size[0] + self.box_size[0]
        self.state = [distance,self.y,0,0]

    def set_dv(self, new_dv):
        self.dv = new_dv

    def set_pos(self, pos):
        self.state[0] = pos - self.box_size[0]//2
        self.state[1] = pos - self.box_size[1]//2

    def update(self, screen):
        pass