from p5 import *  # p5

from .components.Map import Map


def Game(width=800, height=800, population=10):
    isRun = True

    if isRun:
        field = Map(
            population=population,
            width=width,
            height=height
        )

        def setup():  # p5
            size(width, height)  # p5

        def draw():  # p5
            background(0)

            field.update()
            field.show()

        run(sketch_setup=setup, sketch_draw=draw)  # p5
