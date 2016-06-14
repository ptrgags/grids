from base import CellBase, GridBase

class HexCell(CellBase):
    """
    Hexagonal cell. The cell is stored
    in axial coordinates (row, col)
    but cells have properties for getting
    cube coordinates
    """
    
    #6 directions for each hexagon.
    #These directions are labeled similar
    #to NNW (North by Northwest), for example
    #'xy' is the direction that goes towards the
    #positive x-axis but angled slightly towards y
    #whereas 'xz' is towards thex-axis and slightly
    #towards z
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

class HexGrid(GridBase):
    """
    A hexagonal grid in the shape of a parallelogram
    """
    #Width, height of a pointy topped hexagon with 
    #radius (center to vertex) 1
    WIDTH_POINTY = sqrt(3)
    HEIGHT_POINTY = 2.0
    #Width, height of a flat-topped hexagon with radius
    #(center to vertex)1
    WIDTH_FLAT = 2.0
    HEIGHT_FLAT = sqrt(3)
     
    BASIS_VECTORS = {
        'pointy': {
            'row': PVector(WIDTH_POINTY / 2, HEIGHT_POINTY * 3 / 4),
            'col': PVector(WIDTH_POINTY, 0)
        },
        'flat': {
            'row': PVector(0, HEIGHT_FLAT),
            'col': PVector(WIDTH_FLAT * 3 / 4, HEIGHT_FLAT / 2)
        }
    }
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
        self.top = top
    
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
            cell(row, col)
            for row in xrange(self.rows)
            for col in xrange(self.cols)
            if self.grid[row][col] is not None]

    def __str__(self):
        return "\n".join(str(row) for row in self.grid)
    
    def __repr__(self):
        return "Grid({}, {})".format(self.rows, self.cols)

    def to_rect(self, radius, angle, flip_y = True):
        x = radius * cos(angle)
        y = -1 if flip_y else 1
        y *= radius * sin(angle)
        return x, y

    def hex_points(self):
        angle_offset = 0 if self.top == 'flat' else PI / 6
        for i in xrange(6):
            angle = THIRD_PI * i + angle_offset
            yield self.to_rect(1, angle)

    def draw_hex(self, cx, cy):
        beginShape()
        for x, y in self.hex_points():
            vertex(cx + x, cy + y)
        endShape(CLOSE)
    
    @property
    def basis_vectors(self):
        row_basis = self.BASIS_VECTORS[self.top]['row']
        col_basis = self.BASIS_VECTORS[self.top]['col']
        return row_basis, col_basis
    

    def draw(self):
        stroke(255)
        noFill()
        
        row_basis, col_basis = self.basis_vectors
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                center = row * row_basis + col * col_basis
                self.draw_hex(center.x, center.y)