from p5 import *
import numpy as np
from fromAngle import fromAngle

class Bullet:
    def __intit__ (x, y, velocity, demage, direction, ID):
        self.demage = demage
        self.ID = ID
        self.vel = velocity
        self.pos = createVector(x, y)
        self.direction = direction

    def update ():
        velocity = fromAngle(self.direction, self.vel)
        self.pos.add(velocity)


    def show() :
        stroke(255)
        fill('rgba(0,255,0, 0.25)')
        ellipse(self.pos[0] , self.pos[1], 10)