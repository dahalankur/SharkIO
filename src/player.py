"""
player.py
Implements a Player class
"""
from gameboard import GameBoard
from chunk import Chunk
import uuid

class Player():
    """
    An instance of this class represents a player object which contains
    a list of chunks and it's camera view
    """
    def __init__(self, chunks_list = {}, camera_view = None, 
                 name = "Example", unique_id = "TODO"):
        """
        Initialize the Player object with the list of chunk and camera view
        """
        # TODO: Generating id from this function currently not implemented
        self.__chunks = chunks_list
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
    # Create a new gameboard instance
    gb = GameBoard()
    # Create a new chunk
    chunk1 = Chunk(0, 0, 10, 'blue', 1, 4, 7)
    chunk2 = Chunk(0, 1, 10, 'red', 2, 5, 8)
    chunk3 = Chunk(0, 2, 10, 'green', 3, 6, 9)
    # TODO: Consider how to create unique IDs. Sequentially with a global count?
    # Add the chunks to the gameboard
    gb.add_object(chunk1)
    gb.add_object(chunk2)
    gb.add_object(chunk3)
    # Test that all 3 objects are in the gameboard
    assert len(gb.get_objects()) == 3
    objects = gb.get_objects()
    assert objects[chunk1.get_id()] == chunk1
    assert objects[chunk2.get_id()] == chunk2
    assert objects[chunk3.get_id()] == chunk3
    # Test that players can be added to the gameboard
    player1 = Player(unique_id = 1, name="A")
    player2 = Player(unique_id = 2, name="B")
    # Add the players to the gameboard
    gb.add_player(player1)
    assert len (gb.get_players()) == 1
    gb.add_player(player2)
    assert len (gb.get_players()) == 2
    players = gb.get_players()
    assert players[player1.get_id()] == player1
    assert players[player2.get_id()] == player2
    # Add chunk to the players
    print(len(player1.get_chunks()))
    print(len(player2.get_chunks()))
    player1.add_chunk(chunk1)
    player2.add_chunk(chunk2)
    player2.add_chunk(chunk3)
    print(len(player1.get_chunks()))
    print(len(player2.get_chunks()))
    player1_chunk = player1.get_chunks()
    print(len(player1_chunk))
    #assert len(player1_chunk) == 1
    player2_chunk = player2.get_chunks()
    print(len(player2_chunk))
    #assert len(player2_chunk) == 2
    assert player1_chunk[chunk1.get_id()] == chunk1
    assert player2_chunk[chunk2.get_id()] == chunk2
    assert player2_chunk[chunk3.get_id()] == chunk3
    # Remove chunk
    player2.remove_chunk(chunk3)
    player2_chunk2 = player2.get_chunks()
    print(len(player2_chunk2))
    print(len(player1_chunk))
    assert len(player2_chunk2) == 1
    assert player2_chunk2[chunk2.get_id()] == chunk2

    print("Passed")

if __name__ == '__main__':
    tests()
