from .Bullet import Bullet
from p5 import *  # p5
import numpy as np
import random
from .fromAngle import fromAngle


# noinspection PyTypeChecker
class Character:
    def __init__(self, ID: int, direction, x, y, magnitude, damage, HP, capacity, reloadTime, bulletMagnitude):
        self.magnitude = magnitude
        self.direction = direction
        self.vel = fromAngle(self.direction, self.magnitude)

        self.pos = np.array([x, y])
        self.ID = ID
        self.bulletMagnitude = bulletMagnitude
        self.damage = damage
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
        self.isShot = True if random.random() < 0.005 else False

    def show(self):
        fill(255)  # p5
        circle(self.pos[0], self.pos[1], 25)  # p5

    def dead(self, rank):
        self.HP = 0
        self.rank = rank

    def shot(self):
        if self.isShot and self.visible and self.capacity:
            self.capacity -= 1
            return Bullet(
                x=self.pos[0],
                y=self.pos[1],
                magnitude=self.bulletMagnitude,
                damage=self.damage,
                direction=self.direction,
                ID=self.ID
            )
        else:
            return None
