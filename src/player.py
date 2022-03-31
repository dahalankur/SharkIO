"""
gameobject.py
Implements a Player class
"""

class Player():
    """
    An instance of this class represents a player object which contains
    a list of chunks and it's camera view
    """
    def __init__(self, chunks_list, camera_view):
      """
      Initialize the Player object with the list of chunk and camera view
      """
      self.__chunks_list = chunks_list
      self.__camera_view = camera_view

    def add_chunk(self, chunk):
      """
      Adds the chunk with the given chunk_id to the chunks_list
      """
      self.__chunks_list.append(chunk)

    def remove_chunk(self, chunk_id):
      """
      Removes the chunk with the given chunk_id to the chunks_list
      """
      for chunk in self.__chunks_list:
        if chunk.get_id() == chunk_id:
          self.__chunks_list.remove(chunk)