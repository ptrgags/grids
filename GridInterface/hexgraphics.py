"""
Methods for drawing hexagons.

The hexagons will be drawn with radius 1 and
need to be scaled when displaying them
"""


#Width, height of a pointy topped hexagon with 
#radius (center to vertex) 1
WIDTH_POINTY = sqrt(3)
HEIGHT_POINTY = 2.0

#Width, height of a flat-topped hexagon with radius
#(center to vertex) 1
WIDTH_FLAT = 2.0
HEIGHT_FLAT = sqrt(3)

#Basis vectors for drawing regular hexagons of radius 1
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

def hex_basis_vectors(top):
    """
    Get the basis vectors for a hexagon grid.
    
    :param str top: 'pointy' or 'flat' that corresponds to what
        part of the hexagon should be at the top.
    """
    return BASIS_VECTORS[top]['row'], BASIS_VECTORS[top]['col']

#TODO: This can be moved to a utility library if polar coords are needed elsewhere
def to_rect(radius, angle, flip_y = True):
    """
    Convert polar to rectangular coords
    """
    x = radius * cos(angle)
    y = -1 if flip_y else 1
    y *= radius * sin(angle)
    return x, y

def hex_points(top):
    """
    Generate 6 points for a hexagon with radius 1
    (center to vertex) measured from the center of the
    hexagon. These are used in draw_hex
    """
    angle_offset = 0 if top == 'flat' else PI / 6
    for i in xrange(6):
        angle = THIRD_PI * i + angle_offset
        yield to_rect(1, angle)

def draw_hex(center_x, center_y, top):
    beginShape()
    for x, y in hex_points(top):
        vertex(center_x + x, center_y + y)
    endShape(CLOSE)