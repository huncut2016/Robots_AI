import math
import random

import numpy as np

from .Character import Character


class Map:
    def __init__(self, population, width, height):
        self.population = population
        self.characters = []
        self.width = width
        self.height = height
        for i in range(population):
            character = Character(
                x=math.floor(random.random() * self.width),
                y=math.floor(random.random() * self.height),
                damage=200,
                magnitude=1,
                bulletVelocity=2,
                HP=200,
                capacity=10,
                reloadTime=3000,
                direction=random.random() * math.pi * 2,
                ID=i
            )

            self.characters.append(character)

        self.bullets = []
        self.rankCounter = 0

    def update(self):

        newCharacters = []

        for character in self.characters:
            if not character.visible:
                newCharacters.append(character)
                continue

            newBullets = []
            for bullet in self.bullets:
                bullet.update()
                if (
                        bullet.pos[0] < 0 or
                        bullet.pos[0] > self.width or
                        bullet.pos[1] < 0 or
                        bullet.pos[1] > self.height
                ): continue

                if bullet.ID == character.ID:
                    newBullets.append(bullet)
                    continue

                if np.linalg.norm(bullet.pos - character.pos) < 15:
                    character.HP -= bullet.damage
                else:
                    newBullets.append(bullet)

                self.bullets = newBullets

            character.update()
            shot = character.shot()

            if shot is not None:
                self.bullets.append(shot)

            if (
                    character.pos[0] < 0 or
                    character.pos[0] > self.width or
                    character.pos[1] < 0 or
                    character.pos[1] > self.height or
                    character.HP <= 0

            ):
                self.rankCounter += 1
                character.visible = False
                character.rank = self.rankCounter
                if self.rankCounter == self.population:
                    print("Megdöglött az összes")
                    for person in self.characters:
                        print(person)
            newCharacters.append(character)

        self.characters = newCharacters

    def show(self):

        for character in self.characters:
            if character.visible: character.show()

        for bullet in self.bullets:
            bullet.show()
