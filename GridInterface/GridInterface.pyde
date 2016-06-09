class Location(object):
    DIRECTIONS = ['north', 'south', 'east', 'west']
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def get_adjacent(self, direction):
        if direction == 'east':
            return Location(self.row, self.col + 1)
        elif direction == 'west':
            return Location(self.row, self.col - 1)
        elif direction == 'north':
            return Location(self.row - 1, self.col)
        elif  direction == 'south':
            return Location(self.row + 1, self.col)
        else:
            raise ValueError("Not a valid direction")
    
    def get_all_adjacent(self):
        return [self.get_adjacent(dir) for dir in self.DIRECTIONS]
    
    #TODO: Get direction toward location?
    #TODO: Compare locations?
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __str__(self):
        return "({}, {})".format(self.row, self.col)

    def __repr__(self):
        return "Location({}, {})".format(self.row, self.col)

class Grid(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [
            [None for col in xrange(cols)]
            for row in xrange(rows)]
    
    def is_valid(self, location):
        return 0 <= location.row < self.rows and 0 <= location.col < self.cols

    def is_empty(self, location):
        return self.get(location) is None

    def put(self, location, obj):
        if not self.is_valid(location):
            raise ValueError(
                "Can't put {} in grid at {}, location out of bounds!".format(
                    obj, location))
        clobbered = self.get(location)
        self.grid[location.row][location.col] = obj
        return clobbered
    
    def remove(self, location):
        old = self.get(location)
        self.grid[location.row][location.col] = None
        return old
    
    def get(self, location):
        if not self.is_valid(location):
            raise ValueError(
                "Can't get object at {}, location out of bounds!".format(location))
        return self.grid[location.row][location.col]
    
    def move(self, from_loc, to_loc):
        clobbered = self.remove(to_loc)
        moved = self.remove(from_loc)
        self.put(to_loc, moved)
        return clobbered
    
    def occupied_locations(self):
        return [
            Location(row, col)
            for row in xrange(self.rows)
            for col in xrange(self.cols)
            if self.grid[row][col] is not None]
                    
    def valid_adjacent_locations(self, location):
        adjacent_locs = location.get_all_adjacent()
        return [loc for loc in adjacent_locs if self.is_valid(loc)]
  
    def empty_adjacent_locations(self, location):
        locs = self.valid_adjacent_locations(location)
        return [loc for loc in locs if self.get(loc) is None]
    
    def occupied_adjacent_locations(self, location):
        locs = self.valid_adjacent_locations(location)
        return [loc for loc in locs if self.get(loc) is not None]

    def neighbors(self, locations):
        locs = self.valid_adjacent_locations
        neighbor_list = []
        for loc in locs:
            obj = self.get(loc)
            if obj is not None:
                neighbor_list.append(obj)
        return neighbor_list

    def __str__(self):
        return "\n".join(str(row) for row in self.grid)
    
    def __repr__(self):
        return "Grid({}, {})".format(self.rows, self.cols)

    def draw(self):
        stroke(255)
        noFill()
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                rect(row, col, 1.0, 1.0)

class Actor(object):
    def put(self, grid, location):
        self.grid = grid
        self.location = location
        self.grid.put(self.location, self)

    def remove(self):
        if self.location:
            grid.remove(self.location)
        self.location = None
        self.grid = None

    def move_to(self, new_location):
        if not self.grid.is_empty(new_location):
            raise ValueError(
                "Whoops, there's something at {}!".format(new_location))
        self.grid.move(self.location, new_location)
        self.location = new_location
    
    def move_dir(self, dir):
        new_location = self.location.get_adjacent(dir)
        self.move_to(new_location)
    
    def draw(self):
        raise NotImplementedError
    
    def act(self):
        raise NotImplementedError
        
    def __repr__(self):
        return "Actor({}, {})".format(repr(self.grid), self.location)

class Bot(Actor):
    def __init__(self, c):
        self.color = c
        
    def draw(self):
        row = self.location.row
        col = self.location.col
        
        #This makes the assumption that 
        #the top left corner of the grid is (0, 0)
        #and each cell is 1x1 units after transformations
        stroke(255)
        fill(self.color)
        ellipse(col + 0.5, row + 0.5, 0.90, 0.90)

class AutoBot(Actor):
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
        row = self.location.row
        col = self.location.col
        
        stroke(255, 0, 0)
        noFill()
        rect(col + 0.2, row + 0.2, 0.6, 0.6)
        
        x, y = self.DIR_COORDS[self.dir]
        line(col + 0.5, row + 0.5, col + x, row + y)

SCALE = 50
 
def setup():
    global bot1, bot2, grid, autobot
    
    size(14 * SCALE, 14 * SCALE)
    
    grid = Grid(10, 10)
    bot1 = Bot(color(0, 128, 255))
    bot1.put(grid, Location(3, 3))
    bot2 = Bot(color(255, 128, 0))
    bot2.put(grid, Location(5, 5))
    autobot = AutoBot()
    autobot.put(grid, Location(0, 0))

def draw():
    global last_second
    if frameCount % 30 == 0:
        autobot.act()
    
    background(0)
    
    #Make a 2-cell margin
    translate(SCALE * 2, SCALE * 2)
    #Scale the grid to be the desired size
    scale(SCALE)
    #strokeWeight should not vary with the scale
    strokeWeight(1.0 / SCALE)
    
    grid.draw()
    bot1.draw()
    bot2.draw()
    autobot.draw()

ARROW_MAP = {
    UP: 'north',
    DOWN: 'south',
    LEFT: 'west',
    RIGHT: 'east'
}

WASD_MAP = {
    'w': 'north',
    's': 'south',
    'a': 'west',
    'd': 'east'
}

def keyReleased():
    if key == CODED and keyCode in [UP, DOWN, LEFT, RIGHT]:
        try:
            bot1.move_dir(ARROW_MAP[keyCode])
        except ValueError as e:
            print e
    elif key in 'wasd':
        try:
            bot2.move_dir(WASD_MAP[key])
        except ValueError as e:
            print e
    #elif key == ' ':
    #    autobot.act()