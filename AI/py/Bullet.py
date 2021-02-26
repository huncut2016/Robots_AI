from p5 import *
import numpy as np
from fromAngle import fromAngle

class Bullet:
    def __init__ (self, x, y, magni, demage, direction, ID):
        self.demage = demage
        self.ID = ID
        self.magni = magni
        self.vel = fromAngle(direction, magni)
        self.pos = np.array([x, y])
        self.direction = direction

    def update (self):
        self.pos = self.pos + self.vel


    def show(self) :
        stroke(255)
        fill(100)
        circle(self.pos[0] , self.pos[1], 10)