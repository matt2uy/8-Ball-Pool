
# Name: Matthew Uy
# Date: December 7, 2015
# Assignment: CPT - "8 Ball Pool"
# Description: maybe put it on github? (on monday jan 11?)
# Lab requirements: ?

import pygame
import math
from math import acos, asin, atan2, degrees, pi, sqrt
# Got the colour values from http://www.colorpicker.com/
# The variables below each colour initialization represent how...
# ... colour's RGB values will change as the sun "sets"



##################################3
         # TEMP

mouse_held = False   # if the mouse is currently holding the stick
cue_end_x = 0
cue_end_y = 0
cue_buffer = 0

##### will make an object for each ball
cue_ball_x = 220
cue_ball_y = 200
cue_ball_direction = 0 # angle is represented in degrees
cue_ball_speed = 0
balls_in_movement = False # balls are undergoing movement, means that the cue can't be moved at this time


#######Functions: ##########
# place imports at the top
def angle_to_coordinates(angle, x, y):
    # get the x value by using the cosine function
    x = 1 * math.cos(math.radians(angle)) # replace 22.6 with 'angle' and 13 with length
    # get the y value by using the sine function
    y = 1 * math.sin(math.radians(angle))
    return x, y
        
############################3

BROWN = (130, 84, 65) # house
brown_r = 130
brown_g = 84
brown_b = 65

BLUE = (68, 193, 242) # sky
blue_r = 68
blue_g = 193
blue_b = 242

GREEN = (51, 163, 47) # grass
green_r = 51
green_g = 163
green_b = 47

DARK_GREEN = (22, 110, 25) # grass
dark_green_r = 22
dark_green_g = 110
dark_green_b = 25

YELLOW = (242, 242, 68) # sun
yellow_r = 242
yellow_g = 242
yellow_b = 68

BLACK = (0, 0, 0) # roof
black_r = 0
black_g = 0
black_b = 0

WHITE = (255, 255, 255) # clouds
white_r = 255
white_b = 255
white_g = 255

GREY = (150, 150, 150) # moon

### Position/speed/direction presets


pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 400)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic should go here
 
    # --- Drawing code should go here

    ######## Menu
     
 
    # Fill the background with a blue sky
    screen.fill(BLACK)

    ### Draw the pool table
    # Draw the playing surface
    pygame.draw.rect(screen, GREEN, [50, 50, 600, 300], 0)
    # Draw the border/ledge?
    pygame.draw.rect(screen, BROWN, [50, 50, 600, 300], 20)
    # Draw the pockets
    pygame.draw.circle(screen, BLACK, (60, 60), 12, 0)
    pygame.draw.circle(screen, BLACK, (350, 60), 12, 0)
    pygame.draw.circle(screen, BLACK, (640, 60), 12, 0)
    pygame.draw.circle(screen, BLACK, (60, 340), 12, 0)
    pygame.draw.circle(screen, BLACK, (350, 340), 12, 0)
    pygame.draw.circle(screen, BLACK, (640, 340), 12, 0)
      
    # Draw the balls
    pygame.draw.circle(screen, WHITE, (int(cue_ball_x), int(cue_ball_y)), 8, 0)
    pygame.draw.circle(screen, YELLOW, (525, 200), 8, 0)
    pygame.draw.circle(screen, BLACK, (190, 90), 8, 0)


    # Get the mouse press values
    mouse_left = False
    mouse_middle = False
    mouse_right = False
    mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
    
    # Update the cue's position + check whether the cue has hit the ball
    if balls_in_movement == False:
        # the first moment that the mouse is clicked
        if mouse_left == True and mouse_held == False:
            print "c but not released yet"
            mouse_held = True
        # the duration of time WHILE the mouse is being clicked/held
        elif mouse_left == True and mouse_held == True:
            # The amount the stick will move will depend on ...
            # ... the distance between the current mouse ...
            # ... position and the position it was at when clicked
            orig_mouse_x = mouse_x
            orig_mouse_y = mouse_y
            curr_mouse_x, curr_mouse_y = pygame.mouse.get_pos()
            mouse_distance_travelled = sqrt((orig_mouse_x - curr_mouse_x)**2 + (orig_mouse_y - curr_mouse_y)**2)

            # now move the stick backwards along the same angle
            cue_buffer = mouse_distance_travelled
    
            # change the amount of power/ball speed it will transfer
            # ... depending of the distance between the cue and the cue ball
            cue_ball_speed = mouse_distance_travelled/10
            

        # mouse is released AFTER being clicked at first (previous elif statement)
        elif mouse_left == False and mouse_held == True:
            cue_buffer = 0  # reset the cue buffer (the amount the cue moved while the mouse was being held)
            print "ball hit at", mouse_degs, "degrees"
            # set the cue ball variables and set the balls_in_movement variable in motion
            cue_ball_direction = mouse_degs
            balls_in_movement = True
            mouse_held = False
        # mouse is not clicked yet
        elif mouse_left == False: 
            # keep updating cue position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
    else: # cue has hit the ball and the balls are moving
        # this means that the ball is not stationary at this frame
        if cue_ball_speed > 0: 
            ### Move the ball in the correct direction based on cue_ball_direction
            cue_ball_x_increment, cue_ball_y_increment = angle_to_coordinates(cue_ball_direction, cue_ball_x, cue_ball_y)
            cue_ball_x += cue_ball_x_increment*cue_ball_speed
            cue_ball_y += cue_ball_y_increment*cue_ball_speed
            # gradually reduce the ball's speed due to gravity
            cue_ball_speed -= 0.25
            
        # all balls have stopped moving
        else:
            balls_in_movement = False

            
    ### Updating the cue's
    
    # Get the angle between the mouse and the cue ball
    dx = cue_ball_x - mouse_x
    dy = cue_ball_y - mouse_y
    rads = atan2(dy,dx)
    rads %= 2*pi
    mouse_degs = degrees(rads)
    
    cue_front_x = mouse_x
    cue_back_x = mouse_x
    cue_front_y = mouse_y
    cue_back_y = mouse_y

    
    # Get cue end to ball length (AKA: length of the cue)
    mouse_to_ball_length = sqrt((cue_ball_x - cue_front_x)**2 + (cue_ball_y - cue_front_y)**2)
    
    # limit the length of the stick
    cue_length = mouse_to_ball_length-200-cue_buffer
    cue_front_x += cue_length * math.cos(math.radians(mouse_degs))
    # get the y value by using the sine function
    cue_front_y += cue_length * math.sin(math.radians(mouse_degs))

    # back end of the stick
    ball_to_cue_distance = mouse_to_ball_length-20-cue_buffer
    cue_back_x += ball_to_cue_distance * math.cos(math.radians(mouse_degs))
    # get the y value by using the sine function
    cue_back_y += ball_to_cue_distance * math.sin(math.radians(mouse_degs))


    # Draw the mouse pointer
    pygame.draw.rect(screen, BLACK, (mouse_x-5, mouse_y-5, 10, 10), 0)
    # draw the stick when the balls aren't moving
    if balls_in_movement == False:
        pygame.draw.line(screen, BROWN, (cue_front_x, cue_front_y), (cue_back_x, cue_back_y), 5)

    
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(30)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
