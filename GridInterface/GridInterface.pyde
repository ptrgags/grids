from basic import Cell, Grid
from bots import Bot, AutoBot
from example1 import Example1
from example2 import Example2
from hexample1 import Hexample1A, Hexample1B

#Keep track of the Ctrl key.
#Ctrl + Left/Right switches between sketches
control_pressed = False

MODES = [Example1, Example2, Hexample1A, Hexample1B]
mode_index = 0


def setup():
    global mode, mode_index
    size(640, 640)
    init_mode()

def draw():
    mode.update()
    mode.draw()
    

def keyPressed():
    global control_pressed
    if key == CODED and keyCode == CONTROL:
        control_pressed = True
    else:
        mode.keyPressed()
        
def keyReleased():
    global control_pressed, mode, mode_index
    if key == CODED and keyCode == CONTROL:
        control_pressed = False
    elif key == CODED and keyCode == LEFT and control_pressed:
        mode_index = (mode_index - 1) % len(MODES)
        init_mode()
    elif key == CODED and keyCode == RIGHT and control_pressed:
        mode_index = (mode_index + 1) % len(MODES)
        init_mode()
    else:
        mode.keyReleased()

def init_mode():
    global mode
    mode = MODES[mode_index]()
    title_str = "({}/{}) {}".format(mode_index + 1, len(MODES), mode)
    frame.setTitle(title_str)