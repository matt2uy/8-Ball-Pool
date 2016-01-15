# To do: git commit -m"Ball to ball collisions"..."Fixed pool table dimensions"..."Increased window size"..."Added menu"
# Name: Matthew Uy
# Date: December 7, 2015
# Assignment: CPT - "8 Ball Pool"
# Description: Github repo: https://github.com/matt2uy/8-Ball-Pool
# Lab requirements: ?

import pygame, math
# Got the colour values from http://www.colorpicker.com/
# The variables below each colour initialization represent how...
# ... colour's RGB values will change as the sun "sets"

### Game variables ###
mouse_held = False   # if the mouse is currently holding the cue
cue_end_x = 0
cue_end_y = 0
cue_buffer = 0
balls_in_movement = False # balls are undergoing movement, means that the cue can't be moved at this time

# this class allows the ball class to be iterable (which I use later in a few functions).
# Got this tip from: http://stackoverflow.com/questions/739882/iterating-over-object-instances-of-a-given-class-in-python
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

# Defining the ball class
class Ball():
    __metaclass__ = IterRegistry
    _registry = []
    
    def __init__(self):
        self._registry.append(self)
        self.x = 220
        self.y = 200
        self.direction = 0 # angle is represented in degrees
        self.speed = 0
        self.pocketed = False

for ball_instance in Ball:
    print ball_instance.x
    
# create an instance of each ball on the table
cue_ball = Ball()
cue_ball.x = 205 # exactly on the left third
cue_ball.y = 200

eight_ball = Ball() # third column, second row
# temp values for testing:
eight_ball.x = 295
eight_ball.y = 200
#eight_ball.x = 495 # exactly on the right third x-value
#eight_ball.y = 200

# player one's balls (red)     # maybe make a function to make initializing the 16 balls a bit shorter
red_ball_1 = Ball() # first column, first row
red_ball_1.x = 467 
red_ball_1.y = 200 

red_ball_2 = Ball() # second column, first row
red_ball_2.x = 481
red_ball_2.y = 193

red_ball_3 = Ball() # third column, third row
red_ball_3.x = 495
red_ball_3.y = 214

red_ball_4 = Ball() # fourth column, first row
red_ball_4.x = 509
red_ball_4.y = 178

red_ball_5 = Ball() # fourth column, third row
red_ball_5.x = 509
red_ball_5.y = 206

red_ball_6 = Ball() # fifth column, first row
red_ball_6.x = 523
red_ball_6.y = 171

red_ball_7 = Ball() # fifth column, third row
red_ball_7.x = 523
red_ball_7.y = 199

# player two's balls (blue)
blue_ball_1 = Ball() # second column, second row
blue_ball_1.x = 481
blue_ball_1.y = 207

blue_ball_2 = Ball()
blue_ball_2.x = 495  # third column, first row
blue_ball_2.y = 186

blue_ball_3 = Ball() # fourth column, second row
blue_ball_3.x = 509
blue_ball_3.y = 192

blue_ball_4 = Ball() # fourth column, fourth row
blue_ball_4.x = 509
blue_ball_4.y = 220

blue_ball_5 = Ball() # fifth column, second row
blue_ball_5.x = 523
blue_ball_5.y = 185

blue_ball_6 = Ball() # fifth column, fourth row
blue_ball_6.x = 523
blue_ball_6.y = 213

blue_ball_7 = Ball() # fifth column, fifth row
blue_ball_7.x = 523
blue_ball_7.y = 227

### Drawing Functions ###
def draw_static_objects():
    # Draw the playing surface
    pygame.draw.rect(screen, GREEN, [50, 50, 600, 300], 0)
    # Draw the border/ledge?
    pygame.draw.rect(screen, BROWN, [50, 50, 600, 300], 20)
    # Draw the pockets
    pygame.draw.circle(screen, BLACK, (60, 60), 12, 0)      # top left
    pygame.draw.circle(screen, BLACK, (350, 60), 12, 0)     # top middle
    pygame.draw.circle(screen, BLACK, (640, 60), 12, 0)     # top right
    pygame.draw.circle(screen, BLACK, (60, 340), 12, 0)     # bottom left
    pygame.draw.circle(screen, BLACK, (350, 340), 12, 0)    # bottom middle
    pygame.draw.circle(screen, BLACK, (640, 340), 12, 0)    # bottom right

def draw_balls():
    # draw the cue and eight balls
    if cue_ball.pocketed == False:
        pygame.draw.circle(screen, WHITE, (int(cue_ball.x), int(cue_ball.y)), 7, 0)
    if eight_ball.pocketed == False:
        pygame.draw.circle(screen, BLACK, (int(eight_ball.x), int(eight_ball.y)), 7, 0)
    # draw the red (player one) balls
    if red_ball_1.pocketed == False:
        pygame.draw.circle(screen, RED, (int(red_ball_1.x), int(red_ball_1.y)), 7, 0)
    if red_ball_2.pocketed == False:
        pygame.draw.circle(screen, RED, (int(red_ball_2.x), int(red_ball_2.y)), 7, 0)
    if red_ball_3.pocketed == False:
        pygame.draw.circle(screen, RED, (int(red_ball_3.x), int(red_ball_3.y)), 7, 0)
    if red_ball_4.pocketed == False:
        pygame.draw.circle(screen, RED, (int(red_ball_4.x), int(red_ball_4.y)), 7, 0)
    if red_ball_5.pocketed == False:
        pygame.draw.circle(screen, RED, (int(red_ball_5.x), int(red_ball_5.y)), 7, 0)
    if red_ball_6.pocketed == False:
        pygame.draw.circle(screen, RED, (int(red_ball_6.x), int(red_ball_6.y)), 7, 0)
    if red_ball_7.pocketed == False:
        pygame.draw.circle(screen, RED, (int(red_ball_7.x), int(red_ball_7.y)), 7, 0)
        
    # draw the blue (player two) balls
    if blue_ball_1.pocketed == False:
        pygame.draw.circle(screen, BLUE, (int(blue_ball_1.x), int(blue_ball_1.y)), 7, 0)
    if blue_ball_2.pocketed == False:
        pygame.draw.circle(screen, BLUE, (int(blue_ball_2.x), int(blue_ball_2.y)), 7, 0)
    if blue_ball_3.pocketed == False:
        pygame.draw.circle(screen, BLUE, (int(blue_ball_3.x), int(blue_ball_3.y)), 7, 0)
    if blue_ball_4.pocketed == False:
        pygame.draw.circle(screen, BLUE, (int(blue_ball_4.x), int(blue_ball_4.y)), 7, 0)
    if blue_ball_5.pocketed == False:
        pygame.draw.circle(screen, BLUE, (int(blue_ball_5.x), int(blue_ball_5.y)), 7, 0)
    if blue_ball_6.pocketed == False:
        pygame.draw.circle(screen, BLUE, (int(blue_ball_6.x), int(blue_ball_6.y)), 7, 0)
    if blue_ball_7.pocketed == False:
        pygame.draw.circle(screen, BLUE, (int(blue_ball_7.x), int(blue_ball_7.y)), 7, 0)

### User input functions ###
def get_mouse_press():
    mouse_left = False
    mouse_middle = False
    mouse_right = False
    mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
    return mouse_left
        
### Game functions ###
def angle_to_coordinates(angle, x, y):
    # get the x value by using the cosine function
    x = 1 * math.cos(math.radians(angle))
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

def ball_to_cushion_collision(ball_direction, ball_x, ball_y):                
    # hit the top cushion
    if ball_y < 72:
        if ball_direction > 270: # ball incoming from the left
            ball_direction = 360 - ball_direction
        else:                    # ball coming from the right
            ball_direction = 360 - ball_direction
            
    # hit the bottom cushion
    if ball_y > 330:
        if ball_direction < 90: # ball incoming from the left
            ball_direction = 360 - ball_direction
        else:                   # ball coming from the right                  ### problem with all sides -> the ball sometimes sticks at very low angles of reflection -> double bounces?
            ball_direction = 360 - ball_direction
    # hit the left cushion
    if ball_x < 72:
        if ball_direction > 180: # ball incoming from the bottom
            ball_direction += 90
        else:                   # ball coming from the top
            ball_direction -= 90
    # hit the right cushion
    if ball_x > 630:
        if ball_direction > 180: # ball incoming from the bottom
            ball_direction -= 90
        else:                   # ball coming from the top     
            ball_direction += 90
    return ball_direction

def check_if_ball_pocketed(ball_x, ball_y):
    ball_pocketed = False
    # check for top left pocket
    if ball_x > 60 and ball_x < 80 and ball_y > 60 and ball_y < 80:
        # check to see if the ball is touches a 20x20 px zone ## may need to keep in mind that the x and y values of a ball may be at the top right of the sprite.
        ball_pocketed = True
    return ball_pocketed
    '''# check for top middle pocket
    # check for top right pocket
    # check for bottom right pocket
    # check for bottom middle pocket
    # check for bottom left pocket'''

def manage_ball_status(ball_direction, ball_x, ball_y, ball_speed, ball_pocketed):
    # check for a ball to wall collision
    ball_direction = ball_to_cushion_collision(ball_direction, ball_x, ball_y)
    # check for a ball to ball collision
    #ball_direction = ball_to_ball_collision() # in the function -> if balls are touching and at least one is moving -> transfer 50% of first ball's speed? and subtract the first ball's speed by 50%? ... in terms of angle/direction, get the angle created between both balls at the time of impact, then deduce the resulting directions for each ball from that....?
    ### change the ball's cartesian value based on its direction and speed
    ball_x_increment, ball_y_increment = angle_to_coordinates(ball_direction, ball_x, ball_y)
    ball_x += ball_x_increment*ball_speed
    ball_y += ball_y_increment*ball_speed
    # gradually reduce the ball's speed due to gravity
    ball_speed -= 0.1

    ## Check if it gets pocketed
    ball_pocketed = check_if_ball_pocketed(ball_x, ball_y)
    return ball_direction, ball_x, ball_y, ball_speed, ball_pocketed

### Colours ###
BROWN = (130, 84, 65)   # cue
GREEN = (51, 163, 47)   # pool table surface
RED = (222, 24, 24)     # red balls
BLUE = (24, 24, 222)    # blue balls
BLACK = (0, 0, 0)       # background
WHITE = (255, 255, 255) # cue ball

pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 400)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("8 Ball Pool")
 
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
    screen.fill(BLACK) # background
    draw_static_objects()
    draw_balls()
    
    # Get the mouse press values
    mouse_left = get_mouse_press()

    # keep updating cue position
    mouse_x, mouse_y = pygame.mouse.get_pos()    
    
    # Update the cue's position + check whether the cue has hit the ball
    if balls_in_movement == False:
        # the first moment that the mouse is clicked
        if mouse_left == True and mouse_held == False:
            mouse_held = True
            orig_mouse_x = mouse_x
            orig_mouse_y = mouse_y
        # the duration of time WHILE the mouse is being clicked/held
        elif mouse_left == True and mouse_held == True:
            # The amount the cue will move will depend on ...
            # ... the distance between the current mouse ...
            # ... position and the position it was at when clicked
            
            mouse_distance_travelled = get_distance(orig_mouse_x, orig_mouse_y, mouse_x, mouse_y)
            if mouse_distance_travelled > 100: # limit the distance that the cue can be pulled back
                mouse_distance_travelled = 100

            # now move the cue backwards along the same angle
            cue_buffer = mouse_distance_travelled
    
            # change the amount of power/ball speed it will transfer
            # ... depending of the distance between the cue and the cue ball
            cue_ball.speed = mouse_distance_travelled/7
            
        # mouse is released AFTER being clicked at first (previous elif statement)
        elif mouse_left == False and mouse_held == True:
            cue_buffer = 0  # reset the cue buffer (the amount the cue moved while the mouse was being held)
            # set the cue ball variables and set the balls_in_movement variable in motion
            cue_ball.direction = mouse_degs
            balls_in_movement = True
            mouse_held = False 

    # Balls are currently moving        
    else:
        # update the all of the ball's variables
        if cue_ball.speed > 0:
            # one function that does it all, for this ball
            cue_ball.direction, cue_ball.x, cue_ball.y, cue_ball.speed, cue_ball.pocketed = manage_ball_status(cue_ball.direction, cue_ball.x, cue_ball.y, cue_ball.speed, cue_ball.pocketed)

        if eight_ball.speed > 0:
            eight_ball.direction, eight_ball.x, eight_ball.y, eight_ball.speed, eight_ball.pocketed = manage_ball_status(eight_ball.direction, eight_ball.x, eight_ball.y, eight_ball.speed, eight_ball.pocketed)
            
        # if all balls have stopped moving, then inform the if statement above
        if cue_ball.speed <= 0 and eight_ball.speed <= 0: # maybe loop through all balls in a function?
            balls_in_movement = False
            
    ### Updating the cue's position and drawing it ###
    # Get the angle between the mouse and the cue ball
    mouse_degs = get_angle(cue_ball.x, cue_ball.y, mouse_x, mouse_y)
    
    cue_front_x = mouse_x
    cue_back_x = mouse_x
    cue_front_y = mouse_y
    cue_back_y = mouse_y

    # Get cue end to ball length (AKA: length of the cue)
    mouse_to_ball_length = get_distance(cue_ball.x, cue_ball.y, cue_front_x, cue_front_y)
    
    # limit the length of the cue
    cue_length = mouse_to_ball_length-200-cue_buffer
    ball_to_cue_distance = mouse_to_ball_length-20-cue_buffer
    
    # get two pairs of the cue's coordinates from their polar coordinates (mouse angle + distance from the cue ball)
    cue_front_x, cue_front_y = convert_polar_coordinates_to_cartesian(cue_front_x, cue_front_y, mouse_degs, cue_length)
    cue_back_x, cue_back_y = convert_polar_coordinates_to_cartesian(cue_back_x, cue_back_y, mouse_degs, ball_to_cue_distance)

    # show the cue when the balls have stopped moving
    if balls_in_movement == False:
        pygame.draw.line(screen, BROWN, (cue_front_x, cue_front_y), (cue_back_x, cue_back_y), 5)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
