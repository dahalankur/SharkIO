"""
chunk.py
Implements a Chunk class that inherits GameObject 
Authors: Ankur Dahal, Ellis Brown, Jackson Parsells, Rujen Amatya
"""

from gameobject import GameObject
from constants import MIN_VELOCITY
import math

class Chunk(GameObject):
    """
    An instance of this class represents a "chunk", which represents the 
    core player entities affected by game physics 
    """
    def __init__(self, pos_x, pos_y, radius, color, id, velocity, sub_id, \
                 type='chunk'):
        """
        Initialize the Chunk instance with the supplied position, radius, color,
        type, id, velocity, and its unique sub_id
        Note: For each GameObject, a chunk's sub_id must be unique
              Each GameObject's id must be unique
        """
        super().__init__(pos_x, pos_y, radius, color, type, id)
        self.__velocity = velocity
        self.__sub_id = sub_id
        self.__score = 0
    
    def get_score(self):
      """
      Returns the score of the chunk
      """
      return self.__score
    
    def set_score(self, score):
      """
      Sets the score of the chunk
      """
      self.__score = max(0, score) # do not let score be negative

    def increase_radius(self, size):
        self.set_radius(size + self.get_radius())

    def get_velocity(self):
        """
        Return the velocity of the Chunk instance
        """
        return max(MIN_VELOCITY, 200 - 0.8 * math.sqrt(self.get_radius()))
    
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
        return str(super().get_id()) + ":" + str(self.__sub_id)


def tests():
    player1 = Chunk(100, 100, 12.5, (255, 0, 0), 1, 5.3, 1)
    player2 = Chunk(100, 105, 10.3, (255, 123, 0), 2, 5, 1)
    player3 = Chunk(0, 10, 12, (255, 123, 11), 3, 1, 3)
    
    assert(player1.is_colliding(player2))
    assert(player2.is_colliding(player1))
    assert(not player3.is_colliding(player1))
    assert(not player2.is_colliding(player3))

    assert(player3.get_id() == "3:3")
    assert(player1.get_id() == "1:1")
    assert(player2.get_id() == "2:1")

    # assert(player1.get_velocity() == 5.3)
    # assert(player2.get_velocity() == 5)
    # assert(player3.get_velocity() == 1)

    print("Passed")

if __name__ == '__main__':
    tests()