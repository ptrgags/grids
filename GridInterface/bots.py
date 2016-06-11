from base import EntityBase
from random import choice

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

class Wall(EntityBase):
    """
    Represents a wall
    """
    OPAQUE_COUCHE = color(74, 65, 52)
    
    def act(self):
        """
        All the world's a stage. Walls
        make terrible actors.
        """
        pass
    
    def draw(self):
        """
        Draw the most beautiful wall in the world.
        """
        row = self.cell.row
        col = self.cell.col
        noStroke()
        fill(self.OPAQUE_COUCHE)
        rect(col + 0.1, row + 0.1, 0.8, 0.8)
        

class Chaser(EntityBase):
    """
    Entity that chases after another
    entity. This entity is very simplistic, it tries
    to follow the target but changes direction randomly
    when it runs into an obstacle.
    """
    def __init__(self, target):
        self.target = target
        self.caught_target = False
    
    def act(self):
        """
        Move towards the target entity.
        If we collide with the target,
        we have caught the target. If there is a wall in the way,
        pick a random empty adjacent cell and move there.
        """
        dir = self.cell.get_direction_toward(self.target.cell)
        new_cell = self.cell.get_adjacent(dir)
        
        # If we find the target in the adjacent cell, we have "caught" the target
        if self.grid.is_valid(new_cell) and self.grid.get(new_cell) is self.target:
            self.caught_target = True
        
        #If the selected adjacent cell is empty, move to it. Otherwise, move
        #to a random valid adjacent cell
        if not self.caught_target:
            try:
                self.move_to(new_cell)
            except ValueError as e:
                cells = self.grid.empty_adjacent_cells(self.cell)
                if cells:
                    self.move_to(choice(cells))
    
    def draw(self):
        """
        Draw a red circle for a chaser.
        The chaser turns green if it
        has caught the target
        """
        row = self.cell.row
        col = self.cell.col
        
        stroke(0)
        fill("#00FF00" if self.caught_target else "#FF0000")
        ellipse(col + 0.5, row + 0.5, 0.5, 0.5)