from SketchMode import SketchMode
from basic import Cell, Grid
from bots import Bot, AutoBot

AQUA = color(0, 128, 255)
ORANGE = color(255, 128, 0)

class Example1(SketchMode):
    SCALE = 40
    
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
    def __init__(self):
        self.grid = Grid(10, 10)

        #Arrow key bot
        self.bot1 = Bot(AQUA)
        self.bot1.put(self.grid, Cell(3, 3))

        #WASD key bot
        self.bot2 = Bot(ORANGE)
        self.bot2.put(self.grid, Cell(5, 5))

        #Automatic bot
        self.autobot = AutoBot()
        self.autobot.put(self.grid, Cell(0, 0))

    def update(self):
        if frameCount % 30 == 0:
            self.autobot.act()

    def draw(self):
        background(0)

        #Make a 2-cell margin
        translate(self.SCALE * 3, self.SCALE * 3)
        #Scale the grid to be the desired size
        scale(self.SCALE)
        #strokeWeight should not vary with the scale
        strokeWeight(1.0 / self.SCALE)

        self.grid.draw()
        self.bot1.draw()
        self.bot2.draw()
        self.autobot.draw()
    
    def keyReleased(self):
        if key == CODED and keyCode in self.ARROW_MAP:
            try:
                self.bot1.move_dir(self.ARROW_MAP[keyCode])
            except ValueError as e:
                print e
        elif key in self.WASD_MAP:
            try:
                self.bot2.move_dir(self.WASD_MAP[key])
            except ValueError as e:
                print e
        
    def __str__(self):
        return "Example 1: Basic Entities"