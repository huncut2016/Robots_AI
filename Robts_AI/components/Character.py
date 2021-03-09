from threading import Timer

from p5 import *  # p5
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
import numpy as np

from .Bullet import Bullet
from .fromAngle import fromAngle
from .Mapping import Mapping


# noinspection PyTypeChecker
class Character:
    def __init__(self, ID: int, direction, x, y, magnitude, damage, W, H, HP, capacity, reloadTime, bulletMagnitude,
                 populationSize, model=False):
        self.magnitude = magnitude
        self.direction = direction
        self.vel = fromAngle(self.direction, self.magnitude)

        self.width = W
        self.height = H

        self.kills = 0
        self.predict = []
        self.fitnessVal = 0
        self.isReload = False
        self.x = x
        self.y = y
        self.pos = np.array([x, y])
        self.ID = ID
        self.bulletMagnitude = bulletMagnitude
        self.damage = damage
        self.capacity = capacity
        self.shots = capacity
        self.HP = HP

        self.deadVal = 1

        self.populationSize = populationSize
        self.rank = populationSize
        self.reloadTime = reloadTime
        self.isShot = False
        self.visible = True

        if model:
            self.model = model
        else:
            self.model = Sequential([
                Dense(42, input_shape=(31,), activation='sigmoid'),
                Dense(16, activation='sigmoid'),
                Dense(7, activation='sigmoid')
            ])
            # self.model.summary()
            self.model.compile(optimizer="Adam", loss="mse", metrics=["mae"])

    def __str__(self):
        return str(f"""
        ID: {self.ID} 
        RANK: {self.rank}
        """)

    def setDefault(self):
        self.kills = 0
        self.rank = self.populationSize
        self.visible = True
        self.pos = np.array([self.x, self.y])
        self.HP = 200
        self.deadVal = 1

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
        face = fromAngle(self.direction, 50) + self.pos
        fill(255)
        stroke(255)
        line(self.pos[0], self.pos[1], face[0], face[1])

    def usePredict(self):
        faceDirection = self.predict[0]

        lookup = {
            "0": np.array([0, self.magnitude]),
            "1": np.array([0, - self.magnitude]),
            "2": np.array([self.magnitude, 0]),
            "3": np.array([- self.magnitude, 0]),
            "4": np.array([0, 0])
        }

        newVelocities = self.predict[2:-1]
        velocitiesIndex = str(np.where(newVelocities == max(newVelocities))[0][0])
        isShot = True if self.predict[1] > 0.5 else False

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
                self.shots,
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
                self.shots,
                self.damage
            ])

    def dead(self, rank):
        self.HP = 0
        self.rank = rank

    def reload(self):
        self.shots = self.capacity
        self.isReload = False

    def shot(self):

        if self.shots == 0 and not self.isReload:
            self.isReload = True
            Timer(interval=self.reloadTime, function=self.reload).start()
            return None

        if self.isShot and self.visible and self.shots:
            self.shots -= 1
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

    def fitness(self):
        self.fitnessVal = ((self.rank + 2) ** 3) * ((self.kills + 2) ** 7) / self.deadVal
        # print(self.model.get_weights())
