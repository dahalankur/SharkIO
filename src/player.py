"""
player.py
Implements a Player class
"""
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
