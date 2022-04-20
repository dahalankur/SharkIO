"""
player.py
Implements a Player class
Authors: Ankur Dahal, Ellis Brown, Jackson Parsells, Rujen Amatya
"""
from gameobject import GameObject
from chunk import Chunk
from constants import PLAYER_RADIUS, RED, PLAYER_VELOCITY, BOARD_WIDTH, BOARD_HEIGHT
from random import randint, choice
from pygame import Color, image, transform
from os import listdir

class Player():
    """
    An instance of this class represents a player object which contains
    a list of chunks and it's camera view
    """
    def __init__(self, camera_view = None, 
                 name = "Example", unique_id = 0):
        """
        Initialize the Player object with the list of chunk and camera view
        """
        int_x = randint(0, BOARD_WIDTH)
        int_y = randint(0, BOARD_HEIGHT)
        
        self.__chunk = Chunk(int_x, int_y, PLAYER_RADIUS, \
                       self.__get_random_color(), unique_id, PLAYER_VELOCITY, 0)
        self.__camera_view = camera_view
        self.__name = name
        self.__unique_id = unique_id
      
    def __get_random_color(self):
      valid = False
      while not valid:
        valid = True
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        # make sure the color is not too light
        if (r > 220 and g > 220 and b > 220):
          valid = False
        # MAKE SURE NOT GREEN
        if (r < 25 and g > 220 and b < 25):
          valid = False
        # MAKE SURE NOT BLUE
        if (r < 25 and g < 25 and b > 220):
          valid = False
      
      return Color(r, g, b)


    def get_score(self):
      """
      Returns the score of the player
      """
      return self.__chunk.get_score()
    
    def set_score(self, score):
      """
      Sets the score of the player
      """
      self.__chunk.set_score(max(0, score))
    
    def get_id(self):
      """
      Returns the unique id of the player
      """
      return self.__unique_id
    
    def get_name(self):
        """
        Returns the name of the player
        """
        return self.__name

    def set_name(self, name):
        """
        Sets the name of the player
        """
        self.__name = name

    def set_chunk(self, chunk):
        """
        Sets the chunk of the player to chunk
        """
        self.__chunk = chunk

    def get_chunk(self):
        """
        Returns the chunk associated with the player
        """
        return self.__chunk
      
    def get_image(self):
        """
        Returns the image of the player
        """
        return self.__shark_image
    
    def get_shark(self):
        """
        Returns the shark associated with the player based on the id of the
        player.
        """
        # get number of sharks in image folder
        shark_images_dir = listdir("../shark_images")
        num_sharks = len(shark_images_dir)

        # get the shark image
        shark_image_name = "../shark_images/" + shark_images_dir[self.__unique_id % num_sharks]

        # load the shark image
        shark_image = image.load(shark_image_name)

        # return the shark image
        return shark_image
        


def tests():
    chunk1 = Chunk(0, 0, 10, 'blue', 1, 4, 7)
    chunk2 = Chunk(0, 1, 10, 'red', 2, 5, 8)

    player1 = Player(unique_id = 1, name="A")
    player2 = Player(unique_id = 2, name="B")

    player1.set_chunk(chunk1)
    player2.set_chunk(chunk2)

    assert(player1.get_chunk() == chunk1)
    assert(player2.get_chunk() == chunk2)

    assert(player1.get_chunk().get_color() == 'blue')
    assert(player2.get_chunk().get_color() == 'red')

    assert(player1.get_name() == "A")

    player1.set_score(92)
    player2.set_score(-2)
    
    assert(player1.get_score() == 92)
    assert(player2.get_score() == 0)

    print("Passed")

if __name__ == '__main__':
    tests()
