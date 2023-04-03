import numpy as np
import pygame, sys
import random


# Object class for Box
class Object(pygame.sprite.Sprite):
    
    def __init__(self, weight, image, box_size, ratio, state, screen_size):
        self.box_size = box_size
        self.state = state
        self.y = self.state[1]
        self.weight = weight
        self.ratio = ratio
        self.screen_size = screen_size

        pygame.sprite.Sprite.__init__(self)
        self.obj = pygame.image.load(image)
        self.obj = pygame.transform.scale(self.obj, (self.box_size[0]/self.ratio, self.box_size[1]/self.ratio))

        # self.image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
        self.picked = False

    def get_obj(self):
        return self.obj
    
    def get_size(self):
        return self.box_size
    
    def get_pos(self):
        return self.state

    def reset_box(self):
        # TO DO: wait a random amount of time before displaying the obj on the screen
        self.state = [self.screen_size[0] - self.box_size[0]/2,self.y,0,0]

    def set_pos(self, pos):
        self.state[0] = pos - self.box_size[0]//2
        self.state[1] = pos - self.box_size[1]//2

    def get_prob(self):
        # each number and its weights
        prob = {1:12./100., 2:13./100., 3:20./100., 4:10./100., 5:6./100.,
        6:4./100., 7:5./100., 8:9./100., 9:20.9/100., 10:0.1/100.}

        return prob

    def gen_randoms(self):
        prob = self.get_prob()
        # make a random number from the range of numbers 1-10 with its preset weights
        num_list = list(prob.keys())
        num_prob = list(prob.values())
        rand_num = random.choices(num_list, num_prob)
        return rand_num

    def update(self):
        pass