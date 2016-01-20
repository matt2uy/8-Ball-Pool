# Github repository: https://github.com/matt2uy/8-Ball-Pool
# To do:
    # Physics: "Fixed angle of the cue ball after impact"..."Fixed ball collisions bug (check out the '.in contact; variable"
        #..."maybe check the ball/wall collisions for every pixel of movement "
    # Gameplay: "Refined player turns (added previous ball count variable/cue ball sunk)"..."Ball in hand scenarios"..."End game scenarios"..."
    # Presentation: "Player names?"...
# Name: Matthew Uy
# Date: January 22, 2016
# Assignment: CPT - "8 Ball Pool"
# Description: 
# Lab requirements: Located inside the final report

import pygame, math
# Got the colour values from http://www.colorpicker.com/
# The variables below each colour initialization represent how...
# ... colour's RGB values will change as the sun "sets"

### Game variables ###
game_in_progress = False
# variables used in determine_player_turn(), to find out which player is currently controlling the cue
current_player_turn = "Red"
current_shot_count = 0
previous_shot_count = 0
ball_pocketed_in_this_shot = False

show_instructions = False # a variable for the menu
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
        self.colour = "unspecified"
        self.x = 220
        self.y = 200
        self.direction = 0 # angle is represented in degrees
        self.speed = 0
        self.pocketed = False
        self.in_contact = False # temp?

    
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
red_ball_1.colour = "Red"
red_ball_1.x = 467 
red_ball_1.y = 200

red_ball_2 = Ball() # second column, first row
red_ball_2.colour = "Red"
red_ball_2.x = 481
red_ball_2.y = 193

red_ball_3 = Ball() # third column, third row
red_ball_3.colour = "Red"
red_ball_3.x = 495
red_ball_3.y = 214

red_ball_4 = Ball() # fourth column, first row
red_ball_4.colour = "Red"
red_ball_4.x = 509
red_ball_4.y = 178

red_ball_5 = Ball() # fourth column, third row
red_ball_5.colour = "Red"
red_ball_5.x = 509
red_ball_5.y = 206

red_ball_6 = Ball() # fifth column, first row
red_ball_6.colour = "Red"
red_ball_6.x = 523
red_ball_6.y = 171

red_ball_7 = Ball() # fifth column, third row
red_ball_7.colour = "Red"
red_ball_7.x = 523
red_ball_7.y = 199

# player two's balls (blue)
blue_ball_1 = Ball() # second column, second row
blue_ball_1.colour = "Blue"
blue_ball_1.x = 481
blue_ball_1.y = 207

blue_ball_2 = Ball()
blue_ball_2.x = 495  # third column, first row
blue_ball_2.colour = "Blue"
blue_ball_2.y = 186

blue_ball_3 = Ball() # fourth column, second row
blue_ball_3.colour = "Blue"
blue_ball_3.x = 509
blue_ball_3.y = 192

blue_ball_4 = Ball() # fourth column, fourth row
blue_ball_4.colour = "Blue"
blue_ball_4.x = 509
blue_ball_4.y = 220

blue_ball_5 = Ball() # fifth column, second row
blue_ball_5.colour = "Blue"
blue_ball_5.x = 523
blue_ball_5.y = 185

blue_ball_6 = Ball() # fifth column, fourth row
blue_ball_6.colour = "Blue"
blue_ball_6.x = 523
blue_ball_6.y = 213

blue_ball_7 = Ball() # fifth column, fifth row
blue_ball_7.colour = "Blue"
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

def draw_scoreboard():
    num_of_red_left = 0
    num_of_blue_left = 0
    # get the number of red and blue balls
    for ball_instance in Ball:
        if ball_instance.pocketed == False:
            if ball_instance.colour == "Blue":
                num_of_blue_left += 1
            elif ball_instance.colour == "Red":
                num_of_red_left += 1
                
    # draw the red balls left
    for ball in range(num_of_red_left):
        pygame.draw.circle(screen, RED, (100+ball*20, 20), 7, 0)
    
    # draw the blue balls left
    for ball in range(num_of_blue_left):
        pygame.draw.circle(screen, BLUE, (500+ball*20, 20), 7, 0)

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

def ball_to_ball_collision(ball_direction, ball_speed, ball_x, ball_y):
    for ball_instance in Ball:
        # make sure the ball is not comparing it's location, with it's self
        if ball_x != ball_instance.x and ball_y != ball_instance.y:
            # check if the cue ball is touching/contacts the eight ball
            if ball_x > ball_instance.x-7 and ball_x < ball_instance.x+14: # check the x-axis
                if ball_y > ball_instance.y-14 and ball_y < ball_instance.y+14: # check the y-axis
                    # now it is confirmed that they are touching, or are in contact
                    if ball_instance.in_contact == False: # make sure it doesn't do the below twice, for only one contact
                        ball_instance.direction = get_angle(ball_instance.x, ball_instance.y, ball_x, ball_y)
                        ball_instance.speed = ball_speed*0.75
                        ball_speed *= 0.75
                            
                        ball_instance.in_contact = True
                else: # passed one test but is ultimately not in contact
                    if ball_instance.in_contact == True:
                        ball_instance.in_contact = False
            else: # not in contact
                if ball_instance.in_contact == True:
                        ball_instance.in_contact = False
    return ball_speed, ball_direction

def check_if_ball_pocketed(ball_x, ball_y):
    ball_pocketed = False # maght not be necessary, because it is assumed the only the unpocketed ball instances go through  'manage_ball_status()', and in turn, this function.
    # check the top left pocket
    if ball_x > 50 and ball_x < 70 and ball_y > 60 and ball_y < 80:
        # check to see if the ball is touches a 20x20 px zone ## may need to keep in mind that the x and y values of a ball may be at the top right of the sprite.
        ball_pocketed = True
    # check the top middle pocket
    elif ball_x > 350 and ball_x < 370 and ball_y > 60 and ball_y < 80:
        ball_pocketed = True
    # check the top right pocket
    elif ball_x > 630 and ball_x < 650 and ball_y > 60 and ball_y < 80:
        ball_pocketed = True
    # check the bottom right pocket
    elif ball_x > 630 and ball_x < 650 and ball_y > 320 and ball_y < 340:
        ball_pocketed = True
    # check the bottom middle pocket
    elif ball_x > 350 and ball_x < 370 and ball_y > 320 and ball_y < 340:
        ball_pocketed = True
    # check the bottom left pocket
    elif ball_x > 50 and ball_x < 70 and ball_y > 320 and ball_y < 340:
        ball_pocketed = True
        
    return ball_pocketed

def manage_ball_status(ball_direction, ball_x, ball_y, ball_speed, ball_pocketed):
    # check for a ball to wall collision
    ball_direction = ball_to_cushion_collision(ball_direction, ball_x, ball_y)
    # check for a ball to ball collision
    ball_speed, ball_direction = ball_to_ball_collision(ball_direction, ball_speed, ball_x, ball_y)
    
    ### change the ball's cartesian value based on its direction and speed
    ball_x_increment, ball_y_increment = angle_to_coordinates(ball_direction, ball_x, ball_y)
    ball_x += ball_x_increment*ball_speed
    ball_y += ball_y_increment*ball_speed
    # gradually reduce the ball's speed due to gravity
    ball_speed -= 0.095

    ## Check if it gets pocketed
    ball_pocketed = check_if_ball_pocketed(ball_x, ball_y)
    return ball_direction, ball_x, ball_y, ball_speed, ball_pocketed

def check_if_balls_moving():
    no_movement_so_far = True # will be true if the balls were moving in the last frame
    for ball_instance in Ball:   
        if ball_instance.speed <= 0 and no_movement_so_far == True:
            no_movement_so_far = True
        else:
            no_movement_so_far = False
                        
    if no_movement_so_far == True:
        return False
    else:
        return True

def check_if_game_over(game_in_progress, current_player_turn):
    # check if escape key is pressed
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_in_progress = False

    # check if black ball is pocketed
    if eight_ball.pocketed == True:
        game_in_progress = False
        ### if the game is actually over, run through the game end sequence
        # get the number of red and blue balls
        num_of_red_left = 0
        num_of_blue_left = 0
        for ball_instance in Ball:
            if ball_instance.pocketed == False:
                if ball_instance.colour == "Blue":
                    num_of_blue_left += 1
                elif ball_instance.colour == "Red":
                    num_of_red_left += 1

        # find out who won if rest of the player's balls have been pocketed
        if current_player_turn == "Blue":
            if num_of_blue_left == 0:
                winner = "Blue"
            else:
                winner = "Red"
                
        elif current_player_turn == "Red":
            if num_of_red_left == 0:
                winner = "Red"
            else:
                winner = "Blue"

        # print "game over" message, plus the player who won
        print "game over"
        print winner, "wins"
        
    return game_in_progress


def determine_player_turn(current_player_turn, current_shot_count, previous_shot_count, ball_pocketed_in_this_shot):
    # confirm that another shot has been made
    if previous_shot_count < current_shot_count:
        previous_shot_count += 1

        if ball_pocketed_in_this_shot == False or cue_ball.pocketed == True:            
            # toggle player turn if a ball hasn't been pocketed in this turn
            if current_player_turn == "Red":
                current_player_turn = "Blue"
            elif current_player_turn == "Blue":
                current_player_turn = "Red"
        else:
            print "ball has been sunk, don't change player turn" # need to test out this print line check later
            ball_pocketed_in_this_shot = False # reset the ball pocketed count (for the current shot)

    # Draw an indicator, showing which player's turn it is
    if current_player_turn == "Red":
        pygame.draw.rect(screen, RED, [338, 7, 25, 25], 0)
    elif current_player_turn == "Blue":
        pygame.draw.rect(screen, BLUE, [338, 7, 25, 25], 0)

    return current_player_turn, current_shot_count, previous_shot_count, ball_pocketed_in_this_shot

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

    # Show the menu
    if game_in_progress == False:
        # get mouse position and click status
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_left = get_mouse_press()

        if show_instructions == False:
            # if mouse is hovering over a button, then highlight that button
            if mouse_x > 270 and mouse_x < 400 and mouse_y > 195 and mouse_y < 235:     # start game
                myimage = pygame.image.load("Images/menu_play.png")
                if mouse_left == True:
                    game_in_progress = True
                    pygame.mouse.set_pos([100,200]) # set mouse to proper starting position
            elif mouse_x > 270 and mouse_x < 400 and mouse_y > 240 and mouse_y < 285:   # show instructions
                myimage = pygame.image.load("Images/menu_instructions.png")
                if mouse_left == True:
                    show_instructions = True
            elif mouse_x > 270 and mouse_x < 400 and mouse_y > 290 and mouse_y < 335:   # exit game
                myimage = pygame.image.load("Images/menu_quit.png")
                if mouse_left == True:
                    pygame.quit()
            else:
                myimage = pygame.image.load("Images/menu_unselected.png")
        else: # show the instructions
            if mouse_x > 20 and mouse_x < 160 and mouse_y > 20 and mouse_y < 65:     # start game
                myimage = pygame.image.load("Images/instructions_selected.png")
                if mouse_left == True:
                    show_instructions = False
            else:
                myimage = pygame.image.load("Images/instructions.png")
        
        # load and draw the menu
        imagerect = myimage.get_rect()
        screen.fill(BLACK)
        screen.blit(myimage, imagerect)
        pygame.display.flip()
    
    elif game_in_progress == True:       
        ### Drawing the playing area ###
        screen.fill(BLACK) # background
        draw_static_objects()
        draw_scoreboard()
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
                current_shot_count += 1
                cue_buffer = 0  # reset the cue buffer (the amount the cue moved while the mouse was being held)
                # set the cue ball variables and set the balls_in_movement variable in motion
                cue_ball.direction = mouse_degs
                balls_in_movement = True
                mouse_held = False 

        # Balls are currently moving        
        else:
            # update the all of the ball's variables
            for ball_instance in Ball:
                if ball_instance.speed > 0 and ball_instance.pocketed == False:
                    # one function that does it all, for this ball
                    ball_instance.direction, ball_instance.x, ball_instance.y, ball_instance.speed, ball_instance.pocketed = manage_ball_status(ball_instance.direction, ball_instance.x, ball_instance.y, ball_instance.speed, ball_instance.pocketed)
                    if ball_instance.pocketed == True:
                        ball_pocketed_in_this_shot = True
         
            # if all balls have stopped moving, then inform the if statement above
            balls_in_movement = check_if_balls_moving()
            
                
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

        # if the game seems to be done...
        game_in_progress = check_if_game_over(game_in_progress, current_player_turn)

        # switch player turn if necessary
        current_player_turn, current_shot_count, previous_shot_count, ball_pocketed_in_this_shot = determine_player_turn(current_player_turn, current_shot_count, previous_shot_count, ball_pocketed_in_this_shot)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
