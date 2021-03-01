from p5 import *  # p5

from .components.Map import Map


def Game(width=800, height=800, populationSize=10):
    isRun = True

    if isRun:
        field = Map(
            populationSize=populationSize,
            width=width,
            height=height
        )

        for i in range(2000):
            field.update()

        #def setup():  # p5
        #    size(width, height)  # p5

       # def draw():  # p5
         #   background(0)

           # field.show()

      #  run(sketch_setup=setup, sketch_draw=draw, frame_rate=200)  # p5
