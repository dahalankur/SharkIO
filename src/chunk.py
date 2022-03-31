"""
chunk.py
Implements a Chunk class that inherits GameObject 
Written by Ankur Dahal <adahal01@cs.tufts.edu> on 03/31/2022
"""

from gameobject import GameObject

class Chunk(GameObject):
    """
    An instance of this class represents a "chunk", which represents the 
    core player entities affected by game physics 
    """
    def __init__(self, pos_x, pos_y, radius, color, type, id, velocity, sub_id):
        """
        Initialize the Chunk instance with the supplied position, radius, color,
        type, id, velocity, and its unique sub_id
        Note: For each GameObject, a chunk's sub_id must be unique
              Each GameObject's id must be unique
        """
        super.__init__(pos_x, pos_y, radius, color, type, id)
        self.__velocity = velocity
        self.__sub_id = sub_id

    def get_velocity(self):
        """
        Return the velocity of the Chunk instance
        """
        return self.__velocity
    
    def set_velocity(self, velocity):
        """
        Set the velocity of the Chunk instance to the velocity supplied as the
        argument
        """
        self.__velocity = velocity

    def get_id(self):
        """
        Return a unique id (a string) of this chunk.
        Note: This method overrides the GameObject class's get_id method and 
              is guaranteed to return a unique id for any Chunk instance
              An id for a chunk is of the form parentID:chunkID
        """
        return str(self.__id) + ":" + str(self.__sub_id)