from base import EntityBase

class HexBot(EntityBase):
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
        
        row_basis, col_basis = self.grid.basis_vectors
        
        pos = row * row_basis + col * col_basis
        
        ellipse(pos.x, pos.y, 0.90, 0.90)