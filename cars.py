import numpy as np

class Car():

    def __init__(self, mass, size, state, dt, dv, pic_arr):
        self.mass = mass
        self.size = size
        # [posx, posy, velx, vely]
        self.state = state
        # change in time
        self.dt = dt
        # change in speed
        self.dv = dv
        self.curr_time = 0
        self.pic_arr = pic_arr
    
    def set_x_speed(self,new_speed):
        self.state[2] = new_speed


    def is_coll(self,other):
        return 0
        
    def get_x(self):
        return self.state[2]

    def get_y(self):
        return self.state[3]
            

    #updates  the car animation and position 
    def animation(self,screen,frame):
        #moving speed based on 1 for now
        self.state[0] += 1

        index = frame % len(self.pic_arr)
        screen.blit(self.pic_arr[index], [self.get_x(),self.get_y()])

    def step(self):
        force1 = self.dv1 * self.dt
        new_state1 = np.zeros(4, dtype='float32')
        new_state1[:2] = self.state1[:2] +  force1
        new_state1[3] = self.state1[3] + (self.state1[1] / self.dt) 

        new_state2 = np.zeros(4, float) 

        # Collision detection
        new_time = 0
        # if not collision, update state1
        if (self.is_coll(new_state1, new_state2) == 0):
            self.state1 = new_state1
            new_time = self.curr_time + self.dt


