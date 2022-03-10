# Project TODO
* Set up classes for player, food, enemies
* Use thread-safe sockets for client side; and regular socket for the server
* Look into pygame and create a basic single-player game mockup
* Look into graphics, animation, and *audio*
* Idea: The canvas will be huge, and each client (player/thread) will have their own local "camera" entity that follows that player around on the canvas. The camera then renders a particular 
view specific to its client on each client application connected to the server. This ensures that 
all clients connected to the server do not see the same thing, and the camera moves around the canvas 
as the players move.