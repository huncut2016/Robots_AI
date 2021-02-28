import math
import random

import numpy as np

from .Character import Character


class Map:
    def __init__(self, populationSize: int, width: int, height: int):
        self.populationSize = populationSize  # Population size
        self.characters = []  # Characters in the game
        self.width = width  # Width of the map
        self.height = height  # Height of the map
        for i in range(populationSize):  # Create random populationSize
            character = Character(
                x=math.floor(random.random() * self.width),
                y=math.floor(random.random() * self.height),
                damage=200,
                magnitude=1,
                bulletMagnitude=2,
                HP=200,
                capacity=10,
                reloadTime=3000,
                direction=random.random() * math.pi * 2,
                ID=i
            )

            self.characters.append(character)

        self.bullets = []  # All bullets in the game
        self.rankCounter = 0

    def update(self):

        newCharacters = []

        for character in self.characters:
            if not character.visible:
                newCharacters.append(character)
                continue

            newBullets = []

            bulletDictionary = False
            setOfBulletDistances = False

            if len(self.bullets) != 0:
                firstBulletDistance = np.linalg.norm(
                    self.bullets[0].pos - character.pos)  # the first bullet distance from the character
                setOfBulletDistances = {firstBulletDistance}  # set of the distances
                bulletDictionary = {str(firstBulletDistance): self.bullets[0]}  # bullet distance: bullet dictionary

            for bullet in self.bullets:
                BULLET_CHARACTER_DISTANCE = np.linalg.norm(
                    bullet.pos - character.pos)  # The current bullet distance from the character

                bulletDictionary[str(BULLET_CHARACTER_DISTANCE)] = bullet
                setOfBulletDistances.add(BULLET_CHARACTER_DISTANCE)

                bullet.update()
                if (
                        bullet.pos[0] < 0 or
                        bullet.pos[0] > self.width or
                        bullet.pos[1] < 0 or
                        bullet.pos[1] > self.height
                ): continue  # if the bullet is died

                if bullet.ID == character.ID:  # If the bullet is coming from the current character
                    newBullets.append(bullet)
                    continue

                if BULLET_CHARACTER_DISTANCE < 15:  # if the bullet is hit the character
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

            ):  # if the character is died
                self.rankCounter += 1
                character.visible = False
                character.rank = self.rankCounter
                if self.rankCounter == self.populationSize:
                    print("Megdöglött az összes")
                    for person in self.characters:
                        print(person)
                    newCharacters.append(character)
                    break

            newCharacters.append(character)

        self.characters = newCharacters

    def show(self):

        for character in self.characters:
            if character.visible: character.show()

        for bullet in self.bullets:
            bullet.show()
