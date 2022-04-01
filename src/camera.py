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