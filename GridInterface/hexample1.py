from SketchMode import SketchMode
from hex import HexCell, HexGrid
from hexbots import HexBot

class Hexample1A(SketchMode):
    
    #40 pixel radius for each
    #hexagon (distance from center to vertex)
    SCALE = 40
    
    WEADZX_MAP = {
        'w': 'yx',
        'e': 'xy',
        'a': 'yz',
        'd': 'xz',
        'z': 'zy',
        'x': 'zx'
    }
    
    def __init__(self):
        self.grid = HexGrid(5, 9, 'flat')
        
        self.bot = HexBot(color(255, 0, 0))
        self.bot.put(self.grid, HexCell(3, 3))
    
    def draw(self):
        background(0)
        translate(self.SCALE, self.SCALE)
        scale(self.SCALE)
        self.grid.draw()
        
        self.bot.draw()
    
    def keyReleased(self):
        if key in self.WEADZX_MAP:
            try:
                self.bot.move_dir(self.WEADZX_MAP[key])
            except ValueError as e:
                print e
    
    def __str__(self):
        return "Hexample 1A: WEADZX Movement: Flat Top Grid"

class Hexample1B(Hexample1A):
    def __init__(self):
        self.grid = HexGrid(9, 5, 'pointy')
        
        self.bot = HexBot(color(128, 255, 0))
        self.bot.put(self.grid, HexCell(3, 3))
    
    def __str__(self):
        return "Hexample 1B: WEADZX Movement: Pointy Top Grid"