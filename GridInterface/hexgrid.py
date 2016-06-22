from base import CellBase, GridBase
from basic import Grid

from hexgraphics import draw_hex, hex_basis_vectors


# Hex Grid Cell ==================================

class HexCell(CellBase):
    """
    Hexagonal cell. The cell is stored
    in axial coordinates (row, col)
    but cells have properties for getting
    cube coordinates
    """
    
    """
    6 directions for each hexagon.
    These directions are labeled similar
    to NNW (North by Northwest), for example
    'xy' is the direction that goes towards the
    positive x-axis but angled slightly towards y
    whereas 'xz' is towards thex-axis and slightly
    towards z
    
    ASCII Art 
  
       +y   yx
         \  __
      yz __/  \__ 
        /  \__/  \ xy
        \__/  \__/ --> +x
        /  \__/  \
        \__/  \__/  xz
      zy   \__/
         /
        +z  zx
    
    
    The reason why I do this is so directions
    are invariant between flat/pointy topped hexagon
    grids. Rotate the above grid 30 degrees
    counterclockwise so the hexagons have points at the top
    and the labels are exactly the same
    """
    DIRECTIONS = {
        'xz': (0, 1),
        'zx': (1, 0),
        'zy': (1, -1),
        'yz': (0, -1),
        'yx': (-1, 0),
        'xy': (-1, 1)
    }
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def get_adjacent(self, direction):
        try:
            delta_row, delta_col = self.DIRECTIONS[direction]
            return HexCell(self.row + delta_row, self.col + delta_col)
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
        
        raise NotImplementedError
        #TODO: Determine how this method should work on
        #a hex grid.
        '''
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
        '''
        
    @property
    def x(self):
        return self.col

    @property
    def z(self):
        return self.row

    @property
    def y(self):
        return -self.row - self.col
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __str__(self):
        return "({}, {})".format(self.row, self.col)

    def __repr__(self):
        return "cell({}, {})".format(self.row, self.col)


# Hex Grid (Parallelogram) =================================

class HexGrid(Grid):
    """
    A hexagonal grid in the shape of a parallelogram
    """
    
    def __init__(self, rows, cols, top):
        """
        Create the grid
        :param int rows: the number of rows
        :param int cols: the number of columns
        :param str top: 'pointy', or 'flat' for which
        way the hexagons are oriented
        """
        self.rows = rows
        self.cols = cols
        self.grid = [
            [None for col in xrange(cols)]
            for row in xrange(rows)]
        
        #TODO: top is for display purposes only
        self.top = top
    
    def occupied_cells(self):
        return [
            HexCell(row, col)
            for row in xrange(self.rows)
            for col in xrange(self.cols)
            if self.grid[row][col] is not None]
    
    def __repr__(self):
        return "HexGrid({}, {})".format(self.rows, self.cols)
    
    #TODO: This is for graphics only
    def draw(self):
        stroke(255)
        noFill()
        
        row_basis, col_basis = hex_basis_vectors(self.top)
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                center = row * row_basis + col * col_basis
                draw_hex(center.x, center.y, self.top)

class HexagonHexGrid(HexGrid):
    """
    A hexagonal grid in the shape of a hexagon
    """
    def __init__(self, radius, top):
        """
        Constructor
        :param int radius: - the radius of the hexagon grid
            from center to side, including the center.
        :param str top: - "pointy" or "flat" for the part of
            the hexagonal cells that is at the top
        """
        #Radius -> min grid size needed
        # 1 -> 1x1
        # 2 -> 3x3
        # 3 -> 5x5
        # r -> (2r - 1) x (2r - 1)
        grid_size = 2 * radius - 1
        super(HexagonHexGrid, self).__init__(grid_size, grid_size, top)
        self.radius = radius
        
        #This is used for determining which cells in the grid
        #actually belong in the hexagon layout
        #Radius -> Center cell coordinates
        # 1 -> (0, 0)
        # 2 -> (1, 1)
        # 3 -> (2, 2)
        # r -> (r - 1, r - 1)
        self._center_cell = HexCell(radius - 1, radius - 1)
    
    def is_valid(self, cell):
        is_in_grid = super(HexagonHexGrid, self).is_valid(cell)
        if not is_in_grid:
            return False
    
        return abs(cell.y - self._center_cell.y) < self.radius

    #TODO: This is for graphics only
    def draw(self):
        stroke(255)
        noFill()
        
        #First, we need to translate the origin to the center of the screen
        row_basis, col_basis = hex_basis_vectors(self.top)
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if self.is_valid(HexCell(row, col)):
                    center = row * row_basis + col * col_basis
                    draw_hex(center.x, center.y, self.top)