from random import randint

from SketchMode import SketchMode
from basic import Cell, Grid
from bots import Bot, Wall, Chaser

AQUA = color(0, 128, 255)

class Example2(SketchMode):
    SCALE = 40
    
    ARROW_MAP = {
        UP: 'north',
        DOWN: 'south',
        LEFT: 'west',
        RIGHT: 'east'
    }
    
    def __init__(self):
        self.grid = Grid(10, 10)

        #Arrow key bot
        self.bot = Bot(AQUA)
        self.bot.put(self.grid, Cell(5, 6))
        
        self.chaser = Chaser(self.bot)
        self.chaser.put(self.grid, Cell(0, 0))
        
        self.create_walls()
    
    def create_walls(self):
        self.walls = []
        invalid_locations = [self.bot.cell, self.chaser.cell]
        for x in xrange(20):
            row = randint(0, 9)
            col = randint(0, 9)
            cell = Cell(row, col)
            if cell not in invalid_locations:
                wall = Wall()
                wall.put(self.grid, cell)
                self.walls.append(wall)
        

    def update(self):
        if frameCount % 30 == 0:
            self.chaser.act()

    def draw(self):
        background(0)

        #Make a 2-cell margin
        translate(self.SCALE * 3, self.SCALE * 3)
        #Scale the grid to be the desired size
        scale(self.SCALE)
        #strokeWeight should not vary with the scale
        strokeWeight(1.0 / self.SCALE)

        self.grid.draw()
        for wall in self.walls:
            wall.draw()
        self.bot.draw()
        self.chaser.draw()
    
    def keyReleased(self):
        if key == CODED and keyCode in self.ARROW_MAP:
            try:
                self.bot.move_dir(self.ARROW_MAP[keyCode])
            except ValueError as e:
                print e
    
    def __str__(self):
        return "Example 2: Chaser"