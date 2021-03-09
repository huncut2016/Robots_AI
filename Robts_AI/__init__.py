import random
import threading

from p5 import *  # p5
from tensorflow import keras

from .components.Map import Map
from .components.Population import Population
from .components.Character import Character

ch = []
newCh = []
lock = threading.Lock()


def TRAIN(character1, character2):
    global newCh, lock

    p = Population(chModels=[character1, character2])
    p.create()
    result = p.play()

    lock.acquire()

    newCh.append(result[0].model)
    newCh.append(result[1].model)
    lock.release()


def Game(width=800, height=800, populationSize=10, train=False):
    if train:
        global newCh
        global ch
        threads = []

        for i in range(8):
            ch.append(keras.models.load_model('weights1'))
            ch.append(keras.models.load_model('weights2'))

        for i in range(200):
            newCh = []
            for j in range(4):
                t = threading.Thread(target=TRAIN, args=(ch[j * 2], ch[j * 2 + 1]))
                t.start()
                threads.append(t)
            for th in threads:
                th.join()
            random.shuffle(newCh)
            threads = []
        ch[0].save("weights1")
        ch[1].save("weights2")

        p = Population(chModels=[ch[0], ch[1]])
        p.create()
        p.show()

        def setup():  # p5
            size(800, 800)  # p5

        def draw():  # p5
            background(0)
            field.update()
            field.show()

        run(sketch_setup=setup, sketch_draw=draw, frame_rate=200)  # p5
    else:
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
