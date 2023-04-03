import numpy as np
import pygame, sys

# Class that runs the Stimulation #
class Simulation:
    def __init__(self, title):
        self.title = title
        self.paused = True
        self.cur_time = 0

    def init(self, state1, state2, mass1, mass2):
        self.state1 = state1
        self.state2 = state2
        self.mass1 = mass1
        self.mass2 = mass2
    
    def set_time(self, cur_time=0):
        self.cur_time = cur_time

    def set_dt(self, dt=0.033):
        self.dt = dt
    
    def step(self):
        pass
    
    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def save(self, filename):
        pass

    def load(self, filename):
        pass
        