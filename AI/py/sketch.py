from p5 import *
from Map import Map
import numpy as np

field = 0

def  setup():
  createCanvas(800, 800)
  field = Map(10)

def draw():
  background(0)

  fieldap.update()
  fieldap.show()

run()