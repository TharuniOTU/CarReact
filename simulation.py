# import necessary libraries
import pygame, sys 
import numpy as np
import random
from car import *
from object import *

MAX_COLL = 3

# Class that runs the Stimulation #
class Simulation:
    def __init__(self, title):
        self.title = title
        self.paused = True
        self.cur_time = 0

    def init(self, screen_size, weight1, image1, size1, ratio1, state1, weight2, image2, size2, ratio2, state2):
        # applied to both car and object
        self.screen_size = screen_size
        self.y = state1[1]
        self.curr_time = 0
        self.dt = 0.33

        # car initilization
        self.state1 = state1
        self.weight1 = weight1
        self.image1 = image1
        self.size1 = size1
        self.ratio1 = ratio1
        self.dv1 = np.array([20., 0.])
        self.car = Car(4000, self.image1, self.size1, 2.5, self.state1, self.screen_size)
        self.car.reset_car()

        # box initilization
        self.state2 = state2
        self.weight2 = weight2
        self.image2 = image2
        self.size2 = size2
        self.ratio2 = ratio2
        self.dv2 = np.array([0., 0.])
        self.box = Object(200, self.image2, self.size2, 3, self.state2, self.screen_size)
        self.box.hide_box()

        # setting up collision values
        self.tol_screen_right = self.screen_size[0]
        self.tol_screen_left = 0 - self.size1[0]/self.ratio1
        self.tol_object_dist = 380
        # self.tol_object_dist = (self.size2[0]/self.ratio2)*2
        self.collision_type = 0
        self.collision_num = 0

    def get_car(self):
        return self.car
    
    def get_box(self):
        return self.box

    def set_dv_car(self, dv):
        self.dv1 = dv
    
    def set_dv_obj(self, dv):
        self.dv2 = dv

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    # calc distance between the 2 objects
    def compute_dist(self, input1, input2):
        return abs(input1[0] - input2[0])
    

    def is_coll(self, input1, input2):
        distance = self.compute_dist(input1, input2)
        # if x pos of car exceeds the right side of the screen
        # if (input1[0] >= self.tol_screen_right or input1[0] < self.tol_screen_left):
        if (input1[0] >= self.tol_screen_right):
            self.collision_type = 1
        elif (input1[0] <= self.tol_screen_left):
            self.collision_type = 2
        elif (distance <= self.tol_object_dist):
            self.collision_type = 3
        # no collision
        else:
            self.collision_type = 0

        return self.collision_type
    
    # reset variables in collision computation
    def coll_var_reset(self, timestep, time_tmp, state_tmp, new_state, d, dv):
        timestep /= 2
        time_tmp += timestep
        force = dv * timestep
        new_state[:2] = state_tmp[:2] +  force
        new_state[3] = state_tmp[3] / time_tmp
        d = new_state[1]
        state_tmp = new_state
        new_state = np.zeros(4, dtype='float32')

        return timestep, time_tmp, state_tmp, new_state, d

    # apply binary serch method of dividing time in half
    def coll_response(self, input1, input2, t, dv):
        time_tmp = t
        timestep = self.dt
        state_tmp = input1
        d1 = state_tmp[0]
        d2 = self.compute_dist(state_tmp, input2)
        new_state = np.zeros(4, dtype='float32')
        final_state = np.zeros(4, dtype='float32')

        # handle disk-disk collision
        while (d2 > self.tol_object_dist):
            if (d2 > self.tol_object_dist):
                timestep, time_tmp, state_tmp, new_state, d2 = self.coll_var_reset(timestep, time_tmp, state_tmp, new_state, d2, dv)
                d2 = self.compute_dist(state_tmp, input2)
            else:
                time_tmp -= timestep
        final_state = [state_tmp[0], state_tmp[1], state_tmp[2], (-1*state_tmp[3])]  

        return final_state, time_tmp
    
    def step(self, frame, screen):
        # update car velocity 
        force1 = self.dv1 * self.dt
        new_state1 = np.zeros(4, dtype='float32')
        new_state1[:2] = self.car.get_state()[:2] +  force1
        new_state1[2] = self.car.get_state()[2] + (self.car.get_state()[0] / self.dt)

        # update box velocity
        rand_time = round(random.uniform(.95, 1.35), 2)	
        # rand_time = random.random()
        new_state2 = self.box.get_state()

        # Check if collision occured first then update simulation
        new_time = 0
        collision_val = self.is_coll(new_state1, self.box.get_state())

        # IF no collision
        if (collision_val == 0):
            self.car.set_state(new_state1) 
            new_time = self.curr_time + self.dt
            self.car.update_car_image(frame)
        # IF collision with wall on the right side
        elif (collision_val == 1):
            self.car.reset_car()
            self.box.hide_box()
            self.curr_time = 0
        # IF collision with wall on the right side
        elif (collision_val == 2):
            self.car.reset_car()
            self.box.hide_box()
            self.dv1 *= -1
            self.car.change_animation_images() # reverse animation of car  
            self.curr_time = 0
        # If collision with object
        elif(collision_val == 3):
            state_after_collision, collision_time = self.coll_response(new_state1, new_state2, self.curr_time, self.dv1) 
            self.state1 = state_after_collision
            new_time = collision_time
            self.dv1 *= -1
            self.car.change_animation_images() # reverse animation of car 

        self.curr_time += new_time  
        if ((self.curr_time <= rand_time+.5) and (self.curr_time >= rand_time-.5)):
            self.box.reset_box()    

    def save(self, filename):
        pass

    def load(self, filename):
        pass