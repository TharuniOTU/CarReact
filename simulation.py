"""
Simulation Class
Updates the entire simulation
Defines the objects, updates their states and
handles the interactions between the objects
"""

# import necessary libraries
import pygame, sys 
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from car import *
from object import *
from functions import *

# Class that runs the Stimulation #
class Simulation:
    def __init__(self, title):
        self.title = title
        self.paused = True
        self.stopped = False
        self.applyBrakes = False
        self.collRespond = False

        self.hasCollided = False
        self.isResetted = False

    def init(self, screen_size, weight1, image1, size1, ratio1, state1, weight2, image2, size2, ratio2, state2, auto_or_man):
        # applied to both car and object
        self.screen_size = screen_size
        self.y = state1[1]
        self.curr_time = 0
        self.dt = 0.33
        self.auto_or_man = auto_or_man

        # car initilization
        self.state1 = state1 #self.state1[2]
        self.weight1 = weight1
        self.image1 = image1
        self.size1 = size1
        self.ratio1 = ratio1
        # [change in velocity in x direction, change in velocity in y direction]
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
        self.dv2 = np.array([5., 0.])
        self.box = Object(200, self.image2, self.size2, 3, self.state2, self.screen_size, self.dv2)
        self.box.hide_box()

        # breaking values
        self.BrakeRatioResetVal = 0.85
        self.BrakeRatio = self.BrakeRatioResetVal
        self.maxBreakIntervals = 10
        self.BrakeForceIncr = (1 - self.BrakeRatio)/self.maxBreakIntervals

        # setting up collision values
        self.tol_screen_right = self.screen_size[0]
        self.tol_screen_left = 0 - self.size1[0]/self.ratio1
        self.tol_object_dist = 380
        # self.tol_object_dist = (self.size2[0]/self.ratio2)*2
        self.collision_type = 0

        # store data for pytest
        self.car_pos_before_brake = 0
        self.rand_pos_list_file = "Data/RandPos_Actual.txt"
        self.react_dist_list_file = "Data/ReactDistance_Actual.txt"

        self.rand_pos_list = [] # first list
        self.react_dist_list = [] # second list

        self.total_runs = 0
        self.not_collided_count = 0
        self.collided_count = 0

    # Accessors
    def get_car(self):
        return self.car
    
    def get_box(self):
        return self.box

    # Mutators
    def set_dv_car(self, dv):
        self.dv1 = dv
    
    def set_dv_obj(self, dv):
        self.dv2 = dv

    # Reset values for simulation variables
    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.collRespond = False
        self.applyBrakes = False
        self.BrakeRatio = self.BrakeRatioResetVal

    def slowDown(self):
        if(not self.hasCollided):
            self.car_pos_before_brake = self.car.get_state()[0] 
        self.applyBrakes = True

    # reset car/object position/velocity and simulation variables
    def reset_sim(self):
        time.sleep(0.5)

        if(self.hasCollided):
            self.dv1 = -1 * self.dv1
        
        self.paused = True
        self.isResetted = False
        self.collRespond = False
        self.hasCollided = False
        self.applyBrakes = False

        self.BrakeRatio = self.BrakeRatioResetVal
        self.curr_time = 0 

        #reset car and box
        self.car.change_animation_images()
        self.car.reset_car()
        self.box.hide_box() 
               
        
    # Calculate the amount of brake force that needs to be applied
    def calculateBrakeForce(self,force1):
        #brakes can only be applied before collision
        if(self.applyBrakes and not self.hasCollided):
            brakeForce = force1 * self.BrakeRatio

            if(self.BrakeRatio < 1):
                self.BrakeRatio+=self.BrakeForceIncr
            else:
                #Car is at rest now
                dist_diff = abs(self.car_pos_before_brake - self.car.get_state()[0])
                self.react_dist_list.append(dist_diff)
                self.total_runs += 1
                self.not_collided_count += 1
                self.reset_sim() 
                
        # calculate force to apply after a collsion
        elif(self.hasCollided):
            brakeForce = -1 * force1 * self.BrakeRatio

            if(self.BrakeRatio < 1):
                self.BrakeRatio+=self.BrakeForceIncr
            else:
                #Car is at rest now
                self.total_runs += 1
                self.reset_sim() 
        else:
            brakeForce = 0
        

        return brakeForce


    # calc distance between the 2 objects
    def compute_dist(self, input1, input2):
        return abs(input1[0] - input2[0])
    
    # check if a collision occured, and return the type of collision that occured
    def is_coll(self, input1, input2):
        distance = self.compute_dist(input1, input2)
        # if x pos of car exceeds the right side of the screen
        if (input1[0] >= self.tol_screen_right):
            self.collision_type = 1
        # if x pos of car exceeds the left side of the screen
        elif (input1[0] <= self.tol_screen_left):
            self.collision_type = 2
        # if car and object are close to colliding
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

    # apply binary serch method of dividing time in half to find exact time of collision
    def coll_response(self, input1, input2, t):
        time_tmp = t
        timestep = self.dt
        state_tmp = input1
        d2 = self.compute_dist(state_tmp, input2)
        new_state = np.zeros(4, dtype='float32')
        new_state2 = input2

        # handle disk-disk collision
        while (d2 > self.tol_object_dist):
            if (d2 > self.tol_object_dist):
                timestep, time_tmp, state_tmp, new_state, d2 = self.coll_var_reset(timestep, time_tmp, state_tmp, new_state, d2, self.dv1)
                d2 = self.compute_dist(state_tmp, input2)
            else:
                time_tmp -= timestep
        
        # update velocitites after collision
        final_state1 = [state_tmp[0], state_tmp[1], state_tmp[2], state_tmp[3]] 
        final_state2 = [new_state2[0], new_state2[1], new_state2[2], new_state2[3]] 

        return final_state1, final_state2, time_tmp
    
    # Apply auto-breaking if in auto mode
    def auto_brake(self):
        self.tol_auto_brake_dist = (self.car.get_size()[0]/self.ratio1)/2 + (self.box.get_size()[0]/self.ratio2)/2
        self.tol_auto_brake_dist = self.tol_auto_brake_dist + self.car.get_size()[0]/self.ratio1
        distance = self.compute_dist(self.car.get_state(), self.box.get_state())
        # # if x pos of car exceeds the right side of the screen
        if (distance <= self.tol_auto_brake_dist):
            self.slowDown()
    
    # Main function that makes the car move
    def step(self, frame):  
        # update car velocity 
        # force = [force in x direction, force in y direction]
        force1 = self.dv1 * self.dt
        new_state1 = np.zeros(4, dtype='float32')
        new_state2 = np.zeros(4, dtype='float32')

        # [x pos, y pos] + new_force
        new_state1[:2] = self.car.get_state()[:2] +  force1 
        new_state1[2] = self.car.get_state()[2] + (self.car.get_state()[0] / self.dt)

        # update box velocity
        rand_time = round(random.uniform(.95, 1.35), 2)	

        #removing this code breaks it why? idk
        force2 = self.box.get_dv() * self.dt
        force2 = self.dv2 * self.dt
        new_state2[:2] = self.box.get_state()[:2] +  force2
        new_state2[2] = self.box.get_state()[2] + (self.box.get_state()[0] / self.dt)

        # check if auto detection is applied
        if (self.auto_or_man == "A"):
            self.auto_brake()

        # if break is applied, change car to rolling speed
        brakeForce = self.calculateBrakeForce(force1)

        # if simulation is not paused, apply brake foce where needed
        if(self.paused == False):
            if(self.collRespond):
                new_state1[:2] = new_state1[:2] + brakeForce
                # TO DO: apped to both lists, need calculate time
                self.react_time_list = []
            elif (self.applyBrakes):
                new_state1[:2] = new_state1[:2] - brakeForce
       
        # Check if collision occured first then update simulation
        new_time = 0
        collision_val = self.is_coll(self.car.get_state(), self.box.get_state())

        #IF no collision
        if (collision_val == 0): 
            new_time = self.curr_time + self.dt

        # IF collision with wall on the right side
        elif (collision_val == 1 ):
            self.total_runs += 1
            self.reset_sim()

        # IF collision with wall on the left side
        elif (collision_val == 2):
            self.dv1 = -self.dv1
            self.total_runs += 1
            self.reset_sim()

        # If collision with object
        elif(collision_val == 3 and self.hasCollided ==False):
            self.hasCollided = True
            coll_state1, coll_state2, coll_time = self.coll_response(new_state1, new_state2, self.curr_time) 
            new_state1 = coll_state1
            new_state2 = coll_state2
            self.dv1 = -self.dv1
            self.collRespond = True
            new_time = coll_time
            self.car.change_animation_images() # reverse animation of car 
            self.slowDown()

        # update time to new time, after all calculations done    
        self.curr_time += new_time
        # if current time is equal to random time generated, make the box appear  
        if ((self.curr_time <= rand_time+.5) and (self.curr_time >= rand_time-.5)):
            self.box.reset_box() 
            self.rand_pos_list.append(self.box.get_state()[0])

        #update car image
        if(not self.paused):
            self.car.set_state(new_state1)
            self.car.update_car_image(frame)   
            # if a collision occured, update the box image as well
            if(self.hasCollided):
                self.box.set_state(new_state2)

    def save(self):
        print("rand_pos_list: ",self.rand_pos_list) # first list
        print("react_dist_list: ",self.react_dist_list)# second list

        #UPDATE FILE AND SAVE ALL VARIABLES
        write_file(self.react_dist_list_file,self.react_dist_list)
        write_file(self.rand_pos_list_file,self.rand_pos_list)

        #plot the graph
        self.load()

    def load(self):
        
        self.collided_count = self.total_runs - self.not_collided_count
        # TO DO: plot the data
        # plt.title("Histogram for Sample Size: " + str(self.total_runs))
        # plt.hist(self.collided_count, self.not_collided_count, 2)
        # plt.show()
        # Data for the bar graph
        x = ['Collided','Not Collided']
        y = [self.collided_count,self.not_collided_count]

        # Create a bar graph
        plt.bar(x, y)

        # Set labels and title
        plt.xlabel('Has Collided')
        plt.ylabel('Number of Runs')
        plt.title('Bar Graph Example')

        # Display the graph
        plt.show()
