# Name: Matthew Uy
# Date: December 7, 2015
# Assignment: CPT - "8 Ball Pool"
# Description: Github repo: https://github.com/matt2uy/8-Ball-Pool
# Lab requirements: ?

import pygame
import math
# Got the colour values from http://www.colorpicker.com/
# The variables below each colour initialization represent how...
# ... colour's RGB values will change as the sun "sets"

### Game variables ###
mouse_held = False   # if the mouse is currently holding the stick
cue_end_x = 0
cue_end_y = 0
cue_buffer = 0

# ball variable (will make objects/classes?
cue_ball_x = 220
cue_ball_y = 200
cue_ball_direction = 0 # angle is represented in degrees
cue_ball_speed = 0
balls_in_movement = False # balls are undergoing movement, means that the cue can't be moved at this time

### Game functions ###
def angle_to_coordinates(angle, x, y):
    # get the x value by using the cosine function
    x = 1 * math.cos(math.radians(angle)) # replace 22.6 with 'angle' and 13 with length
    # get the y value by using the sine function
    y = 1 * math.sin(math.radians(angle))
    return x, y

def get_angle(object1_x, object1_y, object2_x, object2_y):        
    difference_of_x = object1_x - object2_x
    difference_of_y = object1_y - object2_y
    radians = math.atan2(difference_of_y, difference_of_x)
    radians %= 2*math.pi
    angle = math.degrees(radians)
    return angle

# Get the distance between two points
def get_distance(point1_x, point1_y, point2_x, point2_y):
    distance = math.sqrt((point1_x - point2_x)**2 + (point1_y - point2_y)**2)
    return distance

def convert_polar_coordinates_to_cartesian(x, y, angle, length):
    # use the cos and sin functions to convert: shown here - https://www.mathsisfun.com/polar-cartesian-coordinates.html
    x += length * math.cos(math.radians(angle))
    y += length * math.sin(math.radians(angle))
    return x, y

### Colours ###
BROWN = (130, 84, 65) # cue
GREEN = (51, 163, 47) # pool table surface
RED = (222, 24, 24) # red balls
BLUE = (24, 24, 222) # blue balls
BLACK = (0, 0, 0) # background
WHITE = (255, 255, 255) # cue ball

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
            
    ### Drawing the playing area ###
    # Fill the background with a blue sky
    screen.fill(BLACK)

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
    pygame.draw.circle(screen, RED, (525, 200), 8, 0)
    pygame.draw.circle(screen, BLUE, (190, 90), 8, 0)

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
            mouse_distance_travelled = math.sqrt((orig_mouse_x - curr_mouse_x)**2 + (orig_mouse_y - curr_mouse_y)**2)

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

    # Balls are active        
    else: 
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

            
    ### Updating the cue's position and drawing it ###
    
    # Get the angle between the mouse and the cue ball
    mouse_degs = get_angle(cue_ball_x, cue_ball_y, mouse_x, mouse_y)
    
    cue_front_x = mouse_x
    cue_back_x = mouse_x
    cue_front_y = mouse_y
    cue_back_y = mouse_y

    # Get cue end to ball length (AKA: length of the cue)
    mouse_to_ball_length = get_distance(cue_ball_x, cue_ball_y, cue_front_x, cue_front_y)
    
    # limit the length of the stick
    cue_length = mouse_to_ball_length-200-cue_buffer
    ball_to_cue_distance = mouse_to_ball_length-20-cue_buffer
    
    # get two pairs of the cue's coordinates from their polar coordinates (mouse angle + distance from the cue ball)
    cue_front_x, cue_front_y = convert_polar_coordinates_to_cartesian(cue_front_x, cue_front_y, mouse_degs, cue_length)
    cue_back_x, cue_back_y = convert_polar_coordinates_to_cartesian(cue_back_x, cue_back_y, mouse_degs, ball_to_cue_distance)

    # draw the stick when the balls aren't moving
    if balls_in_movement == False:
        pygame.draw.line(screen, BROWN, (cue_front_x, cue_front_y), (cue_back_x, cue_back_y), 5)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
