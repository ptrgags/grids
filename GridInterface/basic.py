from base import CellBase, GridBase

class Cell(CellBase):
    """
    Cell in a basic Grid. A cell
    is identified by (row, col)
    """
    #Directions and the offsets needed to
    #go in that direction (delta_row, delta_col)
    DIRECTIONS = {
        'north': (-1, 0),
        'south': (1, 0),
        'east': (0, 1),
        'west': (0, -1)
    }
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def get_adjacent(self, direction):
        try:
            delta_row, delta_col = self.DIRECTIONS[direction]
            return Cell(self.row + delta_row, self.col + delta_col)
        except KeyError:
            raise ValueError("Not a valid direction")
    
    def get_all_adjacent(self):
        return [self.get_adjacent(dir) for dir in self.DIRECTIONS]

    def get_direction_toward(self, other):
        """
        Get a direction to travel to
        get to the other cell specified.
        
        This implementation has a slight tendency
        to move vertically rather than horizontally
        """
        
        #If we are at the destination cell, we do not 
        #have to go in any direction
        if self == other:
            return None
        
        #Get the displacement to reach the other cell
        row_delta = other.row - self.row
        col_delta = other.col - self.col
        
        #Get the absolute value of the deltas
        a_row_delta = abs(row_delta)
        a_col_delta = abs(col_delta)
        
        if a_row_delta >= a_col_delta:
            return "south" if row_delta >= 0 else "north"
        else:
            return "east" if col_delta >= 0 else "west"
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __str__(self):
        return "({}, {})".format(self.row, self.col)

    def __repr__(self):
        return "Cell({}, {})".format(self.row, self.col)

class Grid(GridBase):
    """
    Basic grid with (row, col) coordinates
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [
            [None for col in xrange(cols)]
            for row in xrange(rows)]
    
    def is_valid(self, cell):
        return 0 <= cell.row < self.rows and 0 <= cell.col < self.cols

    def put(self, cell, obj):
        if not self.is_valid(cell):
            raise ValueError(
                "Can't put {} in grid at {}, cell out of bounds!".format(
                    obj, cell))
        clobbered = self.get(cell)
        self.grid[cell.row][cell.col] = obj
        return clobbered
    
    def remove(self, cell):
        old = self.get(cell)
        self.grid[cell.row][cell.col] = None
        return old
    
    def get(self, cell):
        if not self.is_valid(cell):
            raise ValueError(
                "Can't get object at {}, cell out of bounds!".format(cell))
        return self.grid[cell.row][cell.col]
    
    def occupied_cells(self):
        return [
            Cell(row, col)
            for row in xrange(self.rows)
            for col in xrange(self.cols)
            if self.grid[row][col] is not None]

    def __str__(self):
        return "\n".join(str(row) for row in self.grid)
    
    def __repr__(self):
        return "Grid({}, {})".format(self.rows, self.cols)

    #TODO: This is graphics-only
    def draw(self):
        stroke(255)
        noFill()
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                rect(row, col, 1.0, 1.0)