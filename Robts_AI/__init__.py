from p5 import *  # p5
from .components.Map import Map
from .components.Population import Population
from datetime import datetime


def Game(width=800, height=800, populationSize=10, train=False):
    if train:
        p = Population()
        p.create()
        p.play()

    isRun = True

    if isRun:
        field = Map(
            populationSize=populationSize,
            width=width,
            height=height
        )

        def setup():  # p5
            size(width, height)  # p5

        def draw():  # p5
            background(0)
            field.update()
            field.show()

        run(sketch_setup=setup, sketch_draw=draw, frame_rate=200)  # p5
