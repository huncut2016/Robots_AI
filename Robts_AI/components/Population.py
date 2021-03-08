import math
import threading
import random

from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from p5 import *

from .Character import Character
from .Map import Map


def mutation(parent, mutationRate):
    weights = parent.get_weights()
    randomNumber = np.random.uniform(0.4, 0.1)
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if np.random.random_sample() > mutationRate:
                weights[i][j] += np.random.uniform(-randomNumber, randomNumber)
    return weights


def crossOver(parent1, parent2):
    weight1 = parent1.get_weights()
    weight2 = parent2.get_weights()

    new_weight1 = weight1
    new_weight2 = weight2

    gene = np.random.randint(0, len(new_weight1) - 1)

    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]

    return np.asarray([new_weight1, new_weight2])


class Population:
    def __init__(self, populationSize=2, maxGeneration=200, characters=2):
        self.model = keras.models.load_model('weights')
        self.populationSize = populationSize
        self.maxGeneration = maxGeneration
        self.characters = characters
        self.evolution = []

    def create(self):
        characters = []
        for i in range(self.populationSize):
            character = Character(
                x=math.floor(random.random() * 700),
                y=math.floor(random.random() * 700),
                damage=200,
                magnitude=2,
                bulletMagnitude=7,
                HP=200,
                capacity=5,
                reloadTime=3.0,
                direction=random.random() * np.pi * 2,
                ID=i,
                W=800,
                H=800,
                populationSize=10
            )
            characters.append(character)
        self.characters = characters

    def play(self):
        field = Map(
            populationSize=self.populationSize,
            width=800,
            height=800,
            characters=self.characters
        )

        for i in range(100):
            for j in range(2000):
                state = field.update()
                if state: break

            self.evolution.append(self.characters[1].fitnessVal)
            self.evolution.append(self.characters[0].fitnessVal)

            if field.characters[0].rank < field.characters[1].rank:
                self.characters[0].model.set_weights(mutation(self.characters[0].model, 0.04))
            else:
                self.characters[1].model.set_weights(mutation(self.characters[1].model, 0.04))


            field = Map(
                populationSize=self.populationSize,
                width=800,
                height=800,
                characters=self.characters
            )

        field = Map(
            populationSize=self.populationSize,
            width=800,
            height=800,
            characters=self.characters
        )

        def setup():  # p5
            size(800, 800)  # p5

        def draw():  # p5
            background(0)
            if field.update(): print("vége")
            field.show()

        minimum = min(self.evolution)
        maximum = max(self.evolution)
        print(maximum, minimum)
        plt.plot([minimum, maximum])
        plt.show()

        run(sketch_setup=setup, sketch_draw=draw, frame_rate=200)




