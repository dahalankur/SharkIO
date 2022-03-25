import math
import pygame

pygame.init()

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

FPS = 100
WIDTH, HEIGHT = 800, 800
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
WHITE = pygame.Color(255,255,255)

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

# starting position, velocity, and radius of "player"
posx = 200
posy = 200
velocity = 5
radius = 30

# radius and position of "stationary object"
radius2 = 25
object_posx = 100
object_posy = 100



running = True
while running:
    clock.tick(FPS)
    
    # get mouse position, and move the circle
    mousex, mousey = pygame.mouse.get_pos()
    if posx < mousex - (radius * 1.25):
        # move right
        posx = min(WIDTH, posx + velocity)
    elif posx > mousex + (radius * 1.25):
        # move left
        posx = max(0, posx - velocity)
    if posy > mousey + (radius * 1.25):
        # move down
        posy = max(0, posy - velocity)
    elif posy < mousey - (radius * 1.25):
        # move up
        posy = min(HEIGHT, posy + velocity)

    screen.fill(WHITE)
    
    # radius += 0.5 # make the player increase in size every frame

    # get distance between two circles
    dist = distance(posx, posy, object_posx, object_posy)
    print(dist)

    # circle collision detection
    if dist < (radius + radius2):
        print("COLLISTION!")
        collided = True
        color = RED
    else:
        collided = False
        color = GREEN

    # draw the circles
    
    # IDEA: for the actual game, iterate over the gameobject list 
    #       in the current player's camera view only, and call a general draw function passing in each object
    #       The draw function will call pygame.draw.circle(screen, object.get_color(), object.get_pos(), object.get_radius()).
    # also maybe render players that are larger at the end so that when they overlap, the bigger circle will be on top. (Is this how it works on pygame? Have to investigate.)

    pygame.draw.circle(screen, color, (posx, posy), radius) # player
    pygame.draw.circle(screen, (0, 255, 255), (object_posx, object_posy), radius2) # stationary circle
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# quit
pygame.quit()
