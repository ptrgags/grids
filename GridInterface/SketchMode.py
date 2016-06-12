class SketchMode(object):
    """
    The SketchMode class is an interface
    for one mode in a multi-sketch Processing
    Sketch.
    
    The goal of this is to make it easy to switch
    between multiple modes of the same Processing sketch
    without needing multiple sketches.
    """
    
    def update(self):
        """
        Code to update the state of the sketch. Called
        just before draw()
        """
        pass
    
    def draw(self):
        """
        Code for drawing a frame of the sketch mode
        """
        pass
    
    def keyPressed(self):
        """
        Code for when a key is pressed.
        Use the key and keyCode variables
        for this.
        """
        pass
    
    def keyReleased(self):
        """
        Code for when a key is released.
        use the key and keyCode variables
        for this
        """
        pass