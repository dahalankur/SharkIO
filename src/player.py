"""
player.py
Implements a Player class
Authors: Ankur Dahal, Ellis Brown, Jackson Parsells, Rujen Amatya
"""
from chunk import Chunk
import uuid

class Player():
    """
    An instance of this class represents a player object which contains
    a list of chunks and it's camera view
    """
    def __init__(self, chunks_list = None, camera_view = None, 
                 name = "Example", unique_id = "TODO"):
        """
        Initialize the Player object with the list of chunk and camera view
        """
        # TODO: Generating id from this function currently not implemented
        self.__chunks = chunks_list if chunks_list else dict()
        self.__camera_view = camera_view
        self.__name = name
        self.__unique_id = unique_id
    
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
    
    def add_chunk(self, chunk):
        """
        Adds the chunk to the chunks_list
        """
        self.__chunks[chunk.get_id()] = chunk

    def remove_chunk(self, chunk):
        """
        Removes the chunk with the given chunk_id to the chunks_list
        """
        self.__chunks.pop(chunk.get_id())
    
    def get_chunks(self):
        """
        Returns the list of chunks
        """
        return self.__chunks

def tests():
    chunk1 = Chunk(0, 0, 10, 'blue', 1, 4, 7)
    chunk2 = Chunk(0, 1, 10, 'red', 2, 5, 8)
    chunk3 = Chunk(0, 2, 10, 'green', 3, 6, 9)

    player1 = Player(unique_id = 1, name="A")
    player2 = Player(unique_id = 2, name="B")

    # Add chunk to the players
    assert(len(player1.get_chunks()) == 0)
    assert(len(player2.get_chunks()) == 0)
    
    player1.add_chunk(chunk1)
    player2.add_chunk(chunk2)
    player2.add_chunk(chunk3)
    
    player1_chunk = player1.get_chunks()
    assert(len(player1_chunk) == 1)

    player2_chunk = player2.get_chunks()
    assert(len(player2_chunk) == 2)
    
    assert(player1_chunk[chunk1.get_id()] == chunk1)
    assert(player2_chunk[chunk2.get_id()] == chunk2)
    assert(player2_chunk[chunk3.get_id()] == chunk3)
   
    # Remove chunk
    player2.remove_chunk(chunk3)
    player2_chunk2 = player2.get_chunks()

    assert(len(player1_chunk) == 1)
    assert(len(player2_chunk2) == 1)
    assert(player2_chunk2[chunk2.get_id()] == chunk2)

    print("Passed")

if __name__ == '__main__':
    tests()
