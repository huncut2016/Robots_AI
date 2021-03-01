from p5 import *  # p5
import numpy as np
from .fromAngle import fromAngle


class Bullet:
    def __init__(self, x, y, magnitude, damage, direction, ID):
        self.damage = damage
        self.ID = ID
        self.magnitude = magnitude
        self.vel = fromAngle(direction, magnitude)
        self.pos = np.array([x, y])
        self.direction = direction

    def update(self):
        self.pos = self.pos + self.vel

    def __str__(self):
        return str( f"""
            Bullet{self.ID}------------
            Pos: {self.pos}
        """)

    def show(self):
        stroke(255)  # p5
        fill(100)  # p5
        circle(self.pos[0], self.pos[1], 10)  # p5
