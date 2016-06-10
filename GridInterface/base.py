class CellBase(object):
    """
    Abstract base class for cell objects.
    This class represents a single cell in
    an infinite grid, using whatever coordinate 
    system is appropriate
    """
    def get_adjacent(self, direction):
        """
        get a Cell object for a grid cell
        that is adjacent to this one.
        
        :param str direction: A string that represents a given
          direction. In C#, this probably will be an enum.
        :rtype: type(self)
        :returns: an adjacent cell
        :raises: ValueError if the direction is invalid.
        """
        raise NotImplementedError
    
    def get_all_adjacent(self):
        """
        Get all adjacent cells.
        :rtype: list(type(self))
        :returns: a list of adjacent Cell objects
        """
        raise NotImplementedError
    
    #TODO: Get direction toward cell?
    #TODO: Compare cells?

class GridBase(object):
    """
    Abstract Base Class for all Grids
    """
    
    def is_valid(self, cell):
        """
        Return True if cell is within
        the bounds of this grid
        """
        raise NotImplementedError

    def is_empty(self, cell):
        """
        Return True if the given
        cell in this grid is valid and empty
        """
        return self.get(cell) is None

    def put(self, cell, obj):
        """
        Put an object into the grid,
        potentially clobbering any existing 
        object in that cell.
        
        :returns: the clobbered object or None)
        :raises: ValueError if cell is not
           valid for this grid
        """
        raise NotImplementedError
    
    def remove(self, cell):
        """
        Remove and return the object in
        the grid at the given cell.
        """
        raise NotImplementedError
    
    def get(self, cell):
        """
        Get the object in the grid at the given cell
        """
        raise NotImplementedError
            
    def move(self, from_cell, to_cell):
        """
        Move an object from from_cell to to_cell.
        if the object in to_cell gets clobbered, 
        it is returned.
        """
        clobbered = self.remove(to_cell)
        moved = self.remove(from_cell)
        self.put(to_cell, moved)
        return clobbered
    
    def occupied_cells(self):
        """
        Get a list of occupied cells
        """
        raise NotImplementedError
                    
    def valid_adjacent_cells(self, cell):
        """
        Get all valid adjacent cells
        """
        adjacent_cells = cell.get_all_adjacent()
        return [cell for cell in adjacent_cells if self.is_valid(cel)]
  
    def empty_adjacent_cells(self, cell):
        """
        Get a list of all empty adjacent cells
        """
        cells = self.valid_adjacent_cells(cell)
        return [cell for cell in cells if self.is_empty(cell)]
    
    def occupied_adjacent_cells(self, cell):
        """
        Get a list of all occupied adjacent cells
        """
        cells = self.valid_adjacent_cells(cell)
        return [cell for cell in cells if not self.is_empty(cell)]

    def neighbors(self, cell):
        """
        Get a list of objects in the adjacent
        cells.
        """
        cells = self.valid_adjacent_cells(cell)
        neighbor_list = []
        for cell in cells:
            obj = self.get(cell)
            if obj is not None:
                neighbor_list.append(obj)
        return neighbor_list

    def draw(self):
        """
        Draw the grid lines for this grid
        """
        raise NotImplementedError

class EntityBase(object):
    """
    Abstract Base class for any object that
    goes into a grid
    """
    #TODO: Should this return the clobbered object if there is one?
    def put(self, grid, cell):
        """
        Put this entity into a grid, saving a reference to
        the cell and grid 
        :param GridBase grid: the grid into which this
            entity wil be added
        :param CellBase cell: the cell to put this
           entity at.
        """
        self.grid = grid
        self.cell = cell
        self.grid.put(self.cell, self)

    def remove(self):
        """
        Remove this entity from the grid
        """
        if self.cell:
            grid.remove(self.cell)
        self.cell = None
        self.grid = None

    def move_to(self, new_cell):
        """
        Move to a new cell in the grid
        
        :param CellBase new_cell: the new cell to move to
        """
        if not self.grid.is_empty(new_cell):
            raise ValueError("Whoops, there's something at {}!".format(new_cell))
        self.grid.move(self.cell, new_cell)
        self.cell = new_cell
    
    def move_dir(self, dir):
        """
        Move to an adjacent cell in the given direction
        
        :param str dir: the direction to move in
        """
        new_cell = self.cell.get_adjacent(dir)
        self.move_to(new_cell)
    
    def draw(self):
        """
        Paint this entity onto the screen.
        """
        raise NotImplementedError
    
    def act(self):
        """
        For entities that move on their own, this method is the
        action to be performed in a single time step
        """
        raise NotImplementedError
        
    def __repr__(self):
        return "Entity({}, {})".format(repr(self.grid), self.cell)