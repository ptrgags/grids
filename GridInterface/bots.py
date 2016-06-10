from base import EntityBase

class Bot(EntityBase):
    """
    Bot with a color that doesn't actually
    do anything, but will be controlled by
    arrow keys in the main sketch
    """
    def __init__(self, c):
        self.color = c
        
    def draw(self):
        row = self.cell.row
        col = self.cell.col
        
        #This makes the assumption that 
        #the top left corner of the grid is (0, 0)
        #and each cell is 1x1 units after transformations
        stroke(255)
        fill(self.color)
        ellipse(col + 0.5, row + 0.5, 0.90, 0.90)

class AutoBot(EntityBase):
    """
    Bot that moves in a straight line, turning 90 degrees to the right
    when it runs into something.
    """
    DIR_ORDER = ['east', 'south', 'west', 'north']
    
    #coordinates for drawing the direction this bot is
    #facing
    DIR_COORDS = {
        'north': (0.5, 0.2),
        'south': (0.5, 0.8),
        'east': (0.8, 0.5),
        'west': (0.2, 0.5)
    }
    def __init__(self):
        self.dir_index = 0
        self.dir = self.DIR_ORDER[self.dir_index]
    
    def act(self):
        try:
            self.move_dir(self.dir)
        except ValueError as e:
            self.dir_index += 1
            self.dir_index %= len(self.DIR_ORDER)
            self.dir = self.DIR_ORDER[self.dir_index]
    
    def draw(self):
        row = self.cell.row
        col = self.cell.col
        
        stroke(255, 0, 0)
        noFill()
        rect(col + 0.2, row + 0.2, 0.6, 0.6)
        
        x, y = self.DIR_COORDS[self.dir]
        line(col + 0.5, row + 0.5, col + x, row + y)