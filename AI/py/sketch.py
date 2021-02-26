from p5 import *
from Map import Map
import numpy as np

field = Map(10, 800, 800)
frame_rate = 140

def setup():
  size(800, 800)

def draw():
  background(0)

  field.update()
  field.show()

run()