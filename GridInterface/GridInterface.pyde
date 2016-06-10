from basic import Cell, Grid
from bots import Bot, AutoBot

SCALE = 50
 
def setup():
    global bot1, bot2, grid, autobot
    
    size(14 * SCALE, 14 * SCALE)
    
    grid = Grid(10, 10)
    bot1 = Bot(color(0, 128, 255))
    bot1.put(grid, Cell(3, 3))
    bot2 = Bot(color(255, 128, 0))
    bot2.put(grid, Cell(5, 5))
    autobot = AutoBot()
    autobot.put(grid, Cell(0, 0))

def draw():
    global last_second
    if frameCount % 30 == 0:
        autobot.act()
    
    background(0)
    
    #Make a 2-cell margin
    translate(SCALE * 2, SCALE * 2)
    #Scale the grid to be the desired size
    scale(SCALE)
    #strokeWeight should not vary with the scale
    strokeWeight(1.0 / SCALE)
    
    grid.draw()
    bot1.draw()
    bot2.draw()
    autobot.draw()

ARROW_MAP = {
    UP: 'north',
    DOWN: 'south',
    LEFT: 'west',
    RIGHT: 'east'
}

WASD_MAP = {
    'w': 'north',
    's': 'south',
    'a': 'west',
    'd': 'east'
}

def keyReleased():
    if key == CODED and keyCode in [UP, DOWN, LEFT, RIGHT]:
        try:
            bot1.move_dir(ARROW_MAP[keyCode])
        except ValueError as e:
            print e
    elif key in 'wasd':
        try:
            bot2.move_dir(WASD_MAP[key])
        except ValueError as e:
            print e
    #elif key == ' ':
    #    autobot.act()