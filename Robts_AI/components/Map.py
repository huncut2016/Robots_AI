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
                magnitude=2,
                bulletMagnitude=7,
                HP=200,
                capacity=10,
                reloadTime=3000,
                direction=random.random() * math.pi * 2,
                ID=i,
                W=self.width,
                H=self.height
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

            bulletDictionary = {}  # bullet distance: bullet dictionary
            setOfBulletDistances = []  # set of the distances

            for bullet in self.bullets:

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
                else:
                    BULLET_CHARACTER_DISTANCE = np.linalg.norm(
                        bullet.pos - character.pos)  # The current bullet distance from the character

                    bulletDictionary[str(BULLET_CHARACTER_DISTANCE)] = bullet
                    setOfBulletDistances.append(BULLET_CHARACTER_DISTANCE)

                if BULLET_CHARACTER_DISTANCE < 15:  # if the bullet is hit the character
                    character.HP -= bullet.damage
                else:
                    newBullets.append(bullet)

            self.bullets = newBullets
            setOfBulletDistances = np.sort(setOfBulletDistances, kind="mergesort")

            nearestBullets = []
            for nearBullet in range(min(3, len(setOfBulletDistances))):
                currentBulletDistance = str(setOfBulletDistances[nearBullet])
                nearestBullets.append(bulletDictionary[currentBulletDistance])

            enemy = False

            for foe in self.characters:
                if foe.ID is not character.ID:
                    enemy = foe
                    break

            character.update(enemy=enemy, bullets= nearestBullets)

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
                character.HP = 0
                if self.rankCounter == self.populationSize:
                    print("Megdöglött az összes")
                    for person in self.characters:
                        print(person)
                    newCharacters.append(character)

            newCharacters.append(character)

        self.characters = newCharacters

    def show(self):

        for character in self.characters:
            if character.visible: character.show()

        for bullet in self.bullets:
            bullet.show()
