"""
gameobject.py
Implements a GameObject class
Written by Ankur Dahal <adahal01@cs.tufts.edu> on 03/16/2022
"""

from math import sqrt
import random

class GameObject():
    """
    An instance of this class represents a game object, and can be 
    of type virus, food, or a chunk
    """
    def __init__(self, pos_x, pos_y, radius, color, type, id):
        """
        Initialize the GameObject instance with the supplied position, radius,
        color, type, and a unique ID.
        Note: It is an invariant that the ID must be unique for each gameobject
              instantiated
        """
        self.__types = ['virus', 'food', 'chunk'] # list of allowed types
        if type.strip() not in self.__types:
            raise RuntimeError('Invalid GameObject type instantiation')
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__radius = radius
        self.__color = color
        self.__type = type
        self.__id = id
    
    def is_virus(self):
        """
        Return true if the GameObject instance is a virus, and false otherwise
        """
        return self.__type == 'virus'
    
    def is_food(self):
        """
        Return true if the GameObject instance is a food, and false otherwise
        """
        return self.__type == 'food'

    def is_chunk(self):
        """
        Return true if the GameObject instance is a chunk, and false otherwise
        """
        return self.__type == 'chunk'

    def get_id(self):
        """
        Return the unique id associated with this GameObject instance
        """
        return self.__id

    def get_pos(self):
        """
        Return the current position of the GameObject instance as a 2-tuple
        """
        return (self.__pos_x, self.__pos_y)

    def set_pos(self, pos_x, pos_y):
        """
        Set the current position of the GameObject instance to the x and y 
        positions supplied as the arguments
        """
        self.__pos_x = pos_x
        self.__pos_y = pos_y
    
    def get_type(self):
        """
        Return the type of the GameObject instance
        Note: The type can be one of 'virus', 'food', or 'chunk'
        """
        return self.__type
    
    def get_radius(self):
        """
        Return the radius of the GameObject instance
        """
        return self.__radius
    
    def set_radius(self, radius):
        """
        Set the radius of the GameObject instance to the radius supplied as the
        argument
        """
        self.__radius = radius
    
    def get_color(self):
        """
        Return the color of the GameObject instance
        """
        return self.__color
    
    def set_color(self, color):
        """
        Set the color of the GameObject instance to the color supplied as the 
        argument
        """
        self.__color = color
    
    def __distance_from(self, otherGameObject):
        """
        Return the distance between this GameObject instance and the other 
        GameObject instance supplied as the argument
        """
        other_object_pos_x, other_object_pos_y = otherGameObject.get_pos()
        return sqrt((self.__pos_x - other_object_pos_x) ** 2 + \
                    (self.__pos_y - other_object_pos_y) ** 2)
    
    def is_colliding(self, otherGameObject):
        """
        Return True if this GameObject instance is colliding with the other 
        GameObject instance supplied as the argument, and False otherwise
        Note: This returns True immediately when the game objects start touching
              and is OK to use for a player consuming food, but not optimal 
              for a player trying to "eat" another player
        """
        distance = self.__distance_from(otherGameObject)
        return distance < (self.__radius + otherGameObject.get_radius())


def tests():
    virus = GameObject(100, 102.345, 4, (0, 255, 0), 'virus', \
                       random.randint(1, 10))
    player1 = GameObject(100, 100, 3, (200, 0, 0), 'chunk', \
                        random.randint(1 , 2))
    player2 = GameObject(200, 100, 5, (200, 0, 222), 'chunk', \
                        random.randint(1 , 200))
    food1 = GameObject(2, 100, 5, (200, 222, 222), 'food', \
                        random.randint(1 , 200))
    food2 = GameObject(23, 10, 1, (1, 1, 222), 'food', \
                        random.randint(1 , 200))
    
    assert(player1.is_colliding(virus))
    assert(not player1.is_colliding(player2))
    assert(not player1.is_colliding(food1))
    assert(not player1.is_colliding(food2))
    assert(not food1.is_colliding(food2))

    assert(virus.get_color() == (0, 255, 0))
    assert(player1.get_color() == (200, 0, 0))

    assert(virus.get_type() == 'virus')
    assert(player1.get_type() == 'chunk')
    assert(player2.get_type() == 'chunk')
    assert(food1.get_type() == 'food')
    assert(food2.get_type() == 'food')

    assert(virus.is_virus())
    assert(player1.is_chunk())
    assert(player2.is_chunk())
    assert(food1.is_food())
    assert(food2.is_food())

    assert(food1.get_radius() == 5)
    assert(food2.get_radius() == 1)
    assert(virus.get_radius() == 4)

    assert(player1.get_pos() == (100, 100))
    assert(player2.get_pos() == (200, 100))
    assert(virus.get_pos() == (100, 102.345))

    print("Passed")

if __name__ == '__main__':
    tests()