# import necessary libraries
import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
import random
from functions import * 

# Intializing Screen #
win_width = 1050 
win_height = 650  

# set up preset values
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 0)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)

# load car images
MAX_COLL = 3
car1 = pygame.image.load("images/car-sprites/car1.png")
car2 = pygame.image.load("images/car-sprites/car2.png")
car3 = pygame.image.load("images/car-sprites/car3.png")
car4 = pygame.image.load("images/car-sprites/car4.png")
car5 = pygame.image.load("images/car-sprites/car5.png")
car6 = pygame.image.load("images/car-sprites/car6.png")
car7 = pygame.image.load("images/car-sprites/car7.png")
car_list = [car1, car2, car3, car4, car5, car6, car7]

# screen func
def to_screen(x, y, win_width, win_height):
    return win_width//2 + x, win_height//2 - y

def from_screen(x, y, win_width, win_height):
    return x - win_width//2, win_height//2 - y

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
        self.curr_img_index = 0
        # change in time, and velocity
        self.dt = 0.33
        self.dv = np.array([70., 0.])
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

    def set_pos(self, pos):
        self.state[0] = pos - self.car_size[0]//2
        self.state[1] = pos - self.car_size[1]//2

    def set_state(self, new_state):
        self.state = new_state

    def reset_car(self):
        self.state = [-(self.car_size[0]/self.ratio)/2,self.y,0,0]


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

    def get_img(self):
        return self.obj
    
    def get_size(self):
        return self.box_size
    
    def get_state(self):
        return self.state
    
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

    def set_pos(self, pos):
        self.state[0] = pos - self.box_size[0]//2
        self.state[1] = pos - self.box_size[1]//2

    def update(self):
        pass


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
        self.dv1 = np.array([70., 0.])
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
        self.box.reset_box()

        # setting up collision values
        self.tol_screen_right = self.screen_size[0]
        self.tol_object_dist = (self.size2[0]/self.ratio2)*2
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

    def is_coll(self, input1, input2):
        distance = abs(abs(input1[0]) - abs(input2[0]))
        # if x pos of car exceeds the right side of the screen
        if (input1[0] >= self.tol_screen_right):
            self.collision_type = 1
        elif (distance <= self.tol_object_dist):
            self.collision_type = 2
        # no collision
        else:
            self.collision_type = 0
        return self.collision_type
    
    def step(self, frame):
        # self.car.update(frame)
        default = np.zeros(4, dtype='float32')
        force1 = self.dv1 * self.dt
        new_state1 = np.zeros(4, dtype='float32')
        new_state1[:2] = self.car.get_state()[:2] +  force1
        new_state1[2] = self.car.get_state()[2] + (self.car.get_state()[0] / self.dt)

        # Check if collision occured first then update simulation
        new_time = 0
        if (self.collision_num <= MAX_COLL):
            if (self.is_coll(new_state1, self.box.get_state()) == 0):
                self.car.set_state(new_state1) 
                new_time = self.curr_time + self.dt
                self.car.update_car_image(frame)
            else:
                self.car.reset_car()
                self.collision_num += 1  
        self.curr_time += new_time      

    def save(self, filename):
        pass

    def load(self, filename):
        pass
        

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

    # car object
    car_image = "images/car-sprites/car1.png"
    car_size = [1004, 450]
    fixed_y = win_height-car_size[1]/2
    # box object
    box_image = "images/box-sprites/box.png"
    box_size = [500, 470]
    # setting up simulation
    sim = Simulation(title)
    sim.init([win_width, win_height], 4000, car_image, car_size, 2.5, [0,fixed_y,0,0], 200, box_image, box_size, 3, [0,fixed_y,0,0])


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
            # sim.get_car().update(frame)
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            break
        else:
            pass

        # Display items onto the screen
        screen.blit(background, [0, 0])
        screen.blit(sim.get_car().get_img(), (sim.get_car().get_state()[0], sim.get_car().get_state()[1]))
        screen.blit(sim.get_box().get_img(), (sim.get_box().get_state()[0], sim.get_box().get_state()[1])) 

        frame += 1
        # text.draw("Time = %f" % sim.cur_time, screen, (5,5))

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