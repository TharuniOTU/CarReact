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
        self.stopped = False
        self.applyBrakes = False
        self.collRespond = False

    def init(self, screen_size, weight1, image1, size1, ratio1, state1, weight2, image2, size2, ratio2, state2):
        # applied to both car and object
        self.screen_size = screen_size
        self.y = state1[1]
        self.curr_time = 0
        self.dt = 0.33

        # car initilization
        self.state1 = state1 #self.state1[2]
        self.weight1 = weight1
        self.image1 = image1
        self.size1 = size1
        self.ratio1 = ratio1
        # [change in velocity in x direction, change in velocity in y direction]
        # 0 = no change in y direction
        self.dv1 = np.array([70., 0.])
        self.car = Car(4000, self.image1, self.size1, 2.5, self.state1, self.screen_size, self.dv1)
        self.car.reset_car()

        # box initilization
        # state = [x position, y position, velocity in x direction, velocity in y direction]
        self.state2 = state2
        self.weight2 = weight2
        self.image2 = image2
        self.size2 = size2
        self.ratio2 = ratio2
        # dv = change in velocity 
        self.dv2 = np.array([0., 0.])
        self.box = Object(200, self.image2, self.size2, 3, self.state2, self.screen_size, self.dv2)
        self.box.hide_box()

        # breaking values
        self.db = [self.dv1[0]/4, 0] # change in break force
        self.b = [0, 0]
        self.BrakeRatioResetVal = 0.85
        self.BrakeRatio = self.BrakeRatioResetVal
        self.maxBreakIntervals = 30
        self.BrakeForceIncr = (1 - self.BrakeRatio)/self.maxBreakIntervals

        # collision values
        self.CollRatioResetVal = 0.85
        self.CollRatio = self.CollRatioResetVal
        self.maxCollIntervals = 30
        self.CollForceIncr = (1 - self.CollRatio)/self.maxCollIntervals

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
        self.BrakeRatio = self.BrakeRatioResetVal
        self.CollRatio = self.CollRatioResetVal
        self.applyBrakes = False
        self.collRespond = False

    def slowDown(self):
        self.applyBrakes = True

    def set_db(self, new_force):
        self.db = new_force

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
        new_state[2] = state_tmp[2] / time_tmp
        d = new_state[0]
        state_tmp = new_state
        new_state = np.zeros(4, dtype='float32')

        return timestep, time_tmp, state_tmp, new_state, d

    # apply binary serch method of dividing time in half
    def coll_response(self, input1, input2, t):
        time_tmp = t
        timestep = self.dt
        state_tmp = input1
        d2 = self.compute_dist(state_tmp, input2)
        new_state = np.zeros(4, dtype='float32')
        new_state2 = np.zeros(4, dtype='float32')

        # handle disk-disk collision
        while (d2 > self.tol_object_dist):
            if (d2 > self.tol_object_dist):
                timestep, time_tmp, state_tmp, new_state, d2 = self.coll_var_reset(timestep, time_tmp, state_tmp, new_state, d2, self.dv1)
                d2 = self.compute_dist(state_tmp, input2)
            else:
                time_tmp -= timestep
        
        force = self.dv2 * timestep
        new_state2[:2] = input2[:2] +  force
        new_state2[2] = input2[2] / time_tmp

        # update velocitites after collision
        final_state1 = [state_tmp[0], state_tmp[1], state_tmp[2], state_tmp[3]] 
        final_state2 = [new_state2[0], new_state2[1], new_state2[2], new_state2[3]] 

        return final_state1, final_state2, time_tmp
    
    # Function that makes the car move
    def step(self, frame):        
        # update car velocity 
        # force = [force in x direction, force in y direction]
        # Note force in y = 0, and will always be 0
        # car_dv = [float(self.car.get_dv()[0]), float(self.car.get_dv()[1])]
        # force1 = car_dv * self.dt
        force1 = self.dv1 * self.dt
        new_state1 = np.zeros(4, dtype='float32')
        # [x pos, y pos] + new_force
        new_state1[:2] = self.car.get_state()[:2] +  force1 
        new_state1[2] = self.car.get_state()[2] + (self.car.get_state()[0] / self.dt)

        # update box velocity
        rand_time = round(random.uniform(.95, 1.35), 2)	
        # force2 = self.box.get_dv() * self.dt
        force2 = self.dv2 * self.dt
        new_state2 = np.zeros(4, dtype='float32')
        new_state2[:2] = self.box.get_state()[:2] +  force2
        new_state2[2] = self.box.get_state()[2] + (self.box.get_state()[0] / self.dt)

        # if break is applied, change car to rolling speed
        if(self.applyBrakes):
            brakeForce = force1 * self.BrakeRatio
            new_state1[:2] = self.car.get_state()[:2] +  force1 - brakeForce

            if(self.BrakeRatio != 1):
                self.BrakeRatio+=self.BrakeForceIncr
            else:
                #Car is at rest now
                self.paused = True
        else:
            new_state1[:2] = self.car.get_state()[:2] +  force1 

        # if collision occured change velocity and position of car and object
        if(self.collRespond):
            collForce1 = force1 * self.CollRatio
            new_state1[:2] = self.car.get_state()[:2] +  force1 - collForce1

            collForce2 = force2 * self.CollRatio
            new_state2[:2] = self.box.get_state()[:2] +  force2 + collForce2

            if(self.CollRatio != 1):
                self.CollRatio += self.CollForceIncr
            else:
                #Car is at rest now
                self.paused = True
        else:
            new_state1[:2] = self.car.get_state()[:2] +  force1 
            new_state2[:2] = self.box.get_state()[:2] +  force2

        # Check if collision occured first then update simulation
        new_time = 0
        collision_val = self.is_coll(new_state1, self.box.get_state())

        # IF no collision
        if (collision_val == 0):        
            self.car.set_state(new_state1) 
            self.car.update_car_image(frame)
            new_time = self.curr_time + self.dt

        # IF collision with wall on the right side
        elif (collision_val == 1):
            self.car.reset_car()
            self.box.hide_box()
            self.curr_time = 0
        # IF collision with wall on the right side
        elif (collision_val == 2):
            self.car.reset_car()
            self.box.hide_box()
            self.dv1 = -self.dv1
            # self.car.set_dv(-self.car.get_dv())
            self.car.change_animation_images() # reverse animation of car  
            self.curr_time = 0
        # If collision with object
        elif(collision_val == 3):
            coll_state1, coll_state2, coll_time = self.coll_response(new_state1, new_state2, self.curr_time) 
            self.state1 = coll_state1
            self.state2 = coll_state2
            # self.car.set_state(coll_state1) 
            self.dv1 = -self.dv1
            self.collRespond = True
            # self.car.set_dv(-self.car.get_dv())
            self.car.change_animation_images() # reverse animation of car 
            # self.box.set_state(coll_state2) 
            new_time = coll_time
            
        self.curr_time += new_time  
        if ((self.curr_time <= rand_time+.5) and (self.curr_time >= rand_time-.5)):
            self.box.reset_box() 

    def save(self, filename):
        pass

    def load(self, filename):
        pass