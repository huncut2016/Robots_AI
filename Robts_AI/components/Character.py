import random

from p5 import *  # p5
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
import numpy as np

from .Bullet import Bullet
from .fromAngle import fromAngle
from .Mapping import Mapping


# noinspection PyTypeChecker
class Character:
    def __init__(self, ID: int, direction, x, y, magnitude, damage, W, H, HP, capacity, reloadTime, bulletMagnitude):
        self.magnitude = magnitude
        self.direction = direction
        self.vel = fromAngle(self.direction, self.magnitude)

        self.width = W
        self.height = H

        self.predict = []
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

        self.model = Sequential([
            Dense(42, input_shape=(31,), activation='sigmoid'),
            Dense(16, activation='sigmoid'),
            Dense(10, activation='sigmoid')
        ])
        # self.model.summary()
        self.model.compile(optimizer="Adam", loss="mse", metrics=["mae"])

    def __str__(self):
        return str(f"""
        ID: {self.ID} 
        RANK: {self.rank}
        """)

    def update(self, enemy, bullets):
        for i in range(3 - len(bullets)):
            bullets.append(Bullet(
                x=self.width * 3,
                y=self.height * 3,
                magnitude=self.bulletMagnitude,
                damage=self.damage,
                direction=self.direction,
                ID=self.ID
            ))

        input_data = np.array([self.getInfo()])

        for bullet in bullets:
            input_data = np.append(input_data, bullet.getInfo())

        input_data = np.append(input_data, enemy.getInfo(enemy=True))
        self.predict = self.model(np.array([input_data]), training=False).numpy()[0]
        self.usePredict()

        self.pos = self.pos + self.vel
        # self.isShot = True if random.random() < 0.005 else False

    def show(self):
        fill(255)  # p5
        circle(self.pos[0], self.pos[1], 25)  # p5

    def usePredict(self):
        faceDirection = self.predict[2] if self.predict[0] > self.predict[1] else self.predict[3]
        lookup = {
            "0": np.array([0, self.magnitude]),
            "1": np.array([0, - self.magnitude]),
            "2": np.array([self.magnitude, 0]),
            "3": np.array([- self.magnitude, 0]),
            "4": np.array([0, 0])
        }
        newVelocities = self.predict[5:]
        velocitiesIndex = str(np.where(newVelocities == max(newVelocities))[0][0])
        isShot = True if self.predict[4] > 0.5 else False

        self.direction = Mapping(faceDirection, 0, 1, 0, 2 * np.pi)
        self.isShot = isShot
        self.vel = lookup[velocitiesIndex]

    def getInfo(self, enemy=False):
        if enemy:
            return np.array([
                self.pos[0],
                self.pos[1],
                self.vel[0],
                self.vel[1],
                self.HP,
                self.capacity,
                self.damage
            ])
        else:
            return np.array([
                self.width,
                self.height,
                self.pos[0],
                self.pos[1],
                self.vel[0],
                self.vel[1],
                self.HP,
                self.capacity,
                self.damage
            ])

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
