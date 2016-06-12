from SketchMode import SketchMode
from hex import HexCell, HexGrid

class Hexample1(SketchMode):
    
    SCALE = 40
    
    def __init__(self):
        self.grid = HexGrid(5, 9, 'flat')
    
    def draw(self):
        background(0)
        translate(self.SCALE, self.SCALE)
        scale(self.SCALE)
        self.grid.draw()
    
    def __str__(self):
        return "Hexample 1: ???"