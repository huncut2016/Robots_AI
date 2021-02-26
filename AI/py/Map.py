import random
import math
from Caracter import *
from Bullet import *
import numpy as np
from fromAngle import fromAngle

class Map:
    def __init__ (self, population) :
        self.population = population
        self.caracters = []
        for i in range(population):
            caracter = Caracter(
                x = math.floor(random.random() * width),
                y = math.floor(random.random() * height),
                demage = 200,
                velocity = 1, 
                bulletVelocity = 5,
                HP = 200,
                capacity = 10,
                reloadTime = 3000,
                direction = random.random() * PI * 2,
                ID = i
            )


            self.caracters.append(caracter)
        
        self.bullets = []
        self.rankCounter = 0



    def update ():

        newCaracters = []

        for caracter in self.caracters:
            if (not caracter.visible) :
                newCaracters.append(caracter)
                continue

            newBullets = []
            for bullet in self.bullets:
                bullet.update()
                if (
                    bullet.pos.x < 0 or
                    bullet.pos.x > width or
                    bullet.pos.y < 0 or
                    bullet.pos.y > height
                ): continue



                if(bullet.ID == caracter.ID) :
                    newBullets.append(bullet)
                    continue

                if(np.linalg.norm(bullet.pos - caracter.pos) < 15):
                    caracter.HP -= bullet.demage    
                else: newBullets.append(bullet)

                self.bullets = newBullets
        
            caracter.update()
            shot = caracter.shot()

            if shot != None:
                self.bullets.append(shot)

            if(
                    caracter.pos[0] < 0 or 
                    caracter.pos[0] > width or
                    caracter.pos[1] < 0 or
                    caracter.pos[1] > height or
                    caracter.HP <= 0
                    
            ):
                self.rankCounter += 1
                caracter.visible = False
                caracter.rank = self.rankCounter
                if (self.rankCounter == self.population):
                    print("Megdöglött az összes")
            newCaracters.append(caracter)

        self.caracters = newCaracters



    def show ():

        for caracter in self.caracters:
            if (caracter.visible): caracter.show()

        for bullet in self.bullets:
            bullet.show()