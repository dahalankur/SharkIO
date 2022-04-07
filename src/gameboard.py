"""
gameboard.py
A gameboard represents the state of the entire game for a particular game lobby
Authors: Ankur Dahal, Ellis Brown, Jackson Parsells, Rujen Amatya
"""

import uuid
from random import randint
from gameobject import GameObject
import pygame
from constants import (BOARD_HEIGHT,
                       BOARD_WIDTH, FOOD_RADIUS,
                       INIT_VIRUS_COUNT,
                       INIT_FOOD_COUNT,
                       VIRUS_RADIUS_MIN,
                       VIRUS_RADIUS_MAX,
                       GREEN,
                       BLUE)

class GameBoard():
    """
    An instance of this class tracks all players and game objects
    during runtime
    """
    def __init__(self, width = BOARD_WIDTH, height = BOARD_HEIGHT,
                objects = None, players = None, unique_id = uuid.uuid4()):
        self.__objects = objects if objects else dict()
        self.__players = players if players else dict()
        self.__width = width
        self.__height = height
        self.__unique_id = unique_id

        # Note, uuid4() is random, and therefore it is possible, but unlikely, 
        # that two GameBoard instances have the same unique id
        # Edit: This is not relevant to us as of now because we are planning 
        #       on having exactly one instance of GameBoard, but might be 
        #       different once we experiment with hosting multiple server/rooms

    def get_height(self):
        """
        Return the height of the GameBoard instance
        """
        return self.__height

    def get_width(self):
        """
        Return the width of the GameBoard instance
        """
        return self.__width  

    def get_unique_id(self):
        """
        Return the unique id of the GameBoard instance
        """
        return self.__unique_id
    
    def get_objects(self):
        """
        Return the dict of game objects
        """
        return self.__objects
    
    def remove_object(self, obj):
        """
        Remove the object from the dict of objects
        """
        # Note, we remove the object based on the unique_id of the obj.
        self.__objects.pop(obj.get_id())
        
    def get_players(self):
        """
        Return the dict of players
        """
        return self.__players

    def add_object(self, obj):
        """
        Add the game object to the dict of game objects
        """
        self.__objects[obj.get_id()] = obj
    
    def add_player(self, player):
        """
        Add the player to the dict of players
        """
        self.__players[player.get_id()] = player
    
    def remove_player(self, player):
        """
        Remove the player from the dict of players
        """
        self.__players.pop(player.get_id())
    
    def gen_init_state(self,
                       num_virus = INIT_VIRUS_COUNT,
                       num_food = INIT_FOOD_COUNT):
        """
        Populates the gameboard with viruses and foods in random coordinates
        They have to spawn within bounds of BOARD_WIDTH, BOARD_HEIGHT
        """
        
        for viruses in range(num_virus):
            virus_radius = randint(VIRUS_RADIUS_MIN, VIRUS_RADIUS_MAX)
            self.add_object(GameObject(randint(0, self.__width), 
                                    randint(0, self.__height),
                                    virus_radius, GREEN, 'virus', uuid.uuid4()))
        for foods in range(num_food):
            self.add_object(GameObject(randint(0, self.__width), 
                                    randint(0, self.__height),
                                    FOOD_RADIUS, BLUE, 'food', uuid.uuid4()))
            
        

def tests(): 
    from player import Player
    
    # Create a new gameboard instance
    gb = GameBoard(BOARD_WIDTH, BOARD_HEIGHT)
    # Create a new gameobject
    virus = GameObject(0, 0, 10, 'red', 'virus', uuid.uuid4())
    food  = GameObject(0, 0, 10, 'green', 'food', uuid.uuid4())
    chunk = GameObject(0, 0, 10, 'blue', 'chunk', uuid.uuid4())
    # TODO: Consider how to create unique IDs. Sequentially with a global count?
    # Add the game objects to the gameboard
    gb.add_object(virus)
    gb.add_object(food)
    gb.add_object(chunk)
    # Test that all 3 objects are in the gameboard
    assert(len(gb.get_objects()) == 3)
    objects = gb.get_objects()
    assert(objects[virus.get_id()] == virus)
    assert(objects[food.get_id()] == food)
    assert(objects[chunk.get_id()] == chunk)
    # Test that objects can be removed from the gameboard
    gb.remove_object(virus)
    assert(len(gb.get_objects()) == 2)
    assert(objects[food.get_id()] == food)
    assert(objects[food.get_id()].get_type() == 'food')
    assert(objects[chunk.get_id()] == chunk)
    assert(objects[chunk.get_id()].get_type() == 'chunk')
    # Test that players can be added to the gameboard
    player1 = Player(unique_id = uuid.uuid4())
    player2 = Player(unique_id = uuid.uuid4())
    # Add the players to the gameboard
    gb.add_player(player1)
    assert(len (gb.get_players()) == 1)
    gb.add_player(player2)
    assert(len (gb.get_players()) == 2)
    players = gb.get_players()
    assert(players[player1.get_id()] == player1)
    assert(players[player2.get_id()] == player2)
    # Test that players can be removed from the gameboard
    gb.remove_player(player1)
    assert(len (gb.get_players()) == 1)
    assert(players[player2.get_id()] == player2)

    # Test generating inital state
    gb2 = GameBoard()
    gb2.gen_init_state()
    assert(len(gb2.get_objects()) == INIT_VIRUS_COUNT + INIT_FOOD_COUNT)
    print("Passed")

    

# Testing adding and removing game objects
if __name__ == '__main__':
    tests()