"""
camera.py
Implements a Camera class 
Authors: Ankur Dahal, Ellis Brown, Jackson Parsells, Rujen Amatya
"""
# class.
# parameter will be a playyer, and this will be held as a reference
# The camera will take the average weighted posistion of all the 
# chunks in the chunks_list from the player, and center the camera about
# that location. The size of the view will scale with the player's mass.
# If the camera reaches the boarder, we can (1) have the camera go off the wrap
# and view "nothingness" (2) have the camera wrap around the boarder and view the
# other side, implying the map can be traversed in a toroidal fashion. Or (3) have
# the camera be bounded by the corners, and not move off the boarder.
# The camera will be updated every time the server sends the client
# an update.

# Edits from Ankur:
# The camera will not be "updated" per se. The client will only be rendering 
# what the camera sees in its rectangle and it will do the calculation -> 
# the goal of the camera is to pick a center of mass of a player's chunks that 
# it is attached to and the client will look at this information, along with 
# the camera's bounds (width/height) and will render the relevant part of the 
# canvas on the client's screen. That's all, as far as I understand so far.