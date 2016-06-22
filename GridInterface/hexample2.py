from SketchMode import SketchMode
from hexgrid import HexCell, HexagonHexGrid
from hexbots import HexBot

class Hexample2(SketchMode):
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
        self.grid = HexagonHexGrid(4, 'flat')
        
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
        return "Hexample 2: Hexagon-Shaped Grid"