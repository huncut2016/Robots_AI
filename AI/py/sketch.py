from p5 import *
from .

field = 0

def  setup():
  createCanvas(800, 800)
  field = new fieldap(10)

def draw():
  background(0)

  fieldap.update()
  fieldap.show()

run()