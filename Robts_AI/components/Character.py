from .Bullet import Bullet
from p5 import *  # p5
import numpy as np
import random
from .fromAngle import fromAngle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy


# noinspection PyTypeChecker
class Character:
    def __init__(self, ID: int, direction, x, y, magnitude, damage, W, H, HP, capacity, reloadTime, bulletMagnitude):
        self.magnitude = magnitude
        self.direction = direction
        self.vel = fromAngle(self.direction, self.magnitude)

        self.width = W
        self.height = H

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
            Dense(16, input_shape=(31,), activation='relu'),
            Dense(16, activation='relu'),
            Dense(9, activation='sigmoid')
        ])
        self.model.summary()
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
        
        input_data = np.array([
            self.width,
            self.height,
            self.pos[0],
            self.pos[1],
            self.vel[0],
            self.vel[1],
            self.HP,
            self.capacity,
            self.damage])
        
        for bullet in bullets:
            input_data = np.append(input_data, [bullet.pos[0], bullet.pos[1], bullet.damage, bullet.vel[0], bullet.vel[1]])

        input_data = np.append(input_data, [enemy.pos[0], enemy.pos[1], enemy.vel[0], enemy.vel[1], enemy.HP, enemy.capacity, enemy.damage])
        predict = self.model.predict(np.array([input_data]))

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
