#from basic import Cell, Grid
#from bots import Bot, AutoBot
from example1 import Example1

def setup():
    global ex1
    size(640, 640)
    ex1 = Example1()

def draw():
    ex1.update()
    ex1.draw()

def keyReleased():
    ex1.keyReleased()