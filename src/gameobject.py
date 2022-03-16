"""
gameobject.py
Implements a GameObject class
Written by Ankur Dahal <adahal01@cs.tufts.edu> on 03/16/2022
"""

class GameObject():
    """
    An instance of this class represents a game object, and can be 
    of type virus, food, or a chunk
    """
    def __init__(self, pos_x, pos_y, radius, color, type):
        """
        Initialize the GameObject with the supplied position, radius, color, 
        and type
        """
        self.types = ['virus', 'food', 'chunk'] # list of allowed types
        if type.strip() not in self.types:
            raise RuntimeError('Invalid GameObject type instantiation')
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.color = color
        self.type = type

    def get_pos(self):
        """
        Return the current position of the GameObject instance as a 2-tuple
        """
        return (self.pos_x, self.pos_y)

    def set_pos(self, pos_x, pos_y):
        """
        Set the current position of the GameObject instance to the x and y 
        positions supplied as the arguments
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
    
    def get_type(self):
        """
        Return the type of the GameObject instance
        Note: The type can be one of 'virus', 'food', or 'chunk'
        """
        return self.type
    
    def get_radius(self):
        """
        Return the radius of the GameObject instance
        """
        return self.radius
    
    def set_radius(self, radius):
        """
        Set the radius of the GameObject instance to the radius supplied as the
        argument
        """
        self.radius = radius
    
    def get_color(self):
        """
        Return the color of the GameObject instance
        """
        return self.color
    
    def set_color(self, color):
        """
        Set the color of the GameObject instance to the color supplied as the 
        argument
        """
        self.color = color
    
    
