from Bullet import Bullet
from p5 import *
import numpy as np
import random
from fromAngle import fromAngle


class Caracter:
    def __init__(self, ID, direction, x, y, magni, demage, HP, capacity, reloadTime, bulletVelocity):
        self.magni = magni
        self.direction = direction
        self.vel = fromAngle(self.direction, self.magni)

        self.pos = np.array([x, y])
        self.ID = ID
        self.bulletVelocity = bulletVelocity
        self.demage = demage
        self.capacity = capacity
        self.HP = HP
        self.rank = None
        self.reloadTime = reloadTime
        self.isShot = False
        self.visible = True

    def __str__(self):
        return str(f"""
        ID: {self.ID} 
        RANK: {self.rank}
        """)

    def update(self):
        self.pos = self.pos + self.vel
        self.isShot = random.random() < 0.005 if True else False

    def show(self):
        fill(255)
        circle(self.pos[0], self.pos[1], 25)

    def dead(self, rank):
        self.HP = 0
        self.rank = rank

    def shot(self):
        if(self.isShot and self.visible and self.capacity):
            self.capacity -= 1
            return Bullet(
                x= self.pos[0],
                y= self.pos[1],
                magni= self.bulletVelocity,
                demage= self.demage,
                direction= self.direction,
                ID= self.ID
            )
        else:
            return None