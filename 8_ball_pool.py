# Source code for this project can also be found in the github repository: https://github.com/matt2uy/8-Ball-Pool
# To do:
    # sounds
    # diamonds on the pool table edges
    # Gameplay: "refine ball guide line"
# Name: Matthew Uy
# Date: January 22, 2016
# Assignment: CPT - "8 Ball Pool"
# Description and Lab requirements: Located inside the final report

# draw text: http://stackoverflow.com/questions/10077644/python-display-text-w-font-color
# downloaded font .ttf file from here: http://www.fontsquirrel.com/fonts/PT-Sans

import pygame, math

### Colours ###
BROWN = (130, 84, 65)   # cue
GREY = (245, 245, 245)   # cue
DARK_BROWN = (110, 74, 55)   # pool table border
green_r = 51
green_g =  163
green_b = 47
GREEN = (green_r, green_g, green_b)   # pool table surface
RED = (222, 24, 24)     # red balls
BLUE = (24, 24, 222)    # blue balls
BLACK = (0, 0, 0)       # background
white_r = 255
white_g = 255
white_b = 255
WHITE = (white_r, white_g, white_b) # cue ball
# ball pulsing variable
ball_pulse_multiplier = -0.5
# in game message variables (the int represent the amount of time left - in milliseconds)
intro_message = 1200 # 240 fps, so 480 frames = 5 seconds
ball_in_hand_message = 0

### Game variables ###
game_in_progress = False
winner = "unknown"
win_screen = False # determine whether to show the win screen or not

# variables used in determine_player_turn(), to find out which player is currently controlling the cue
current_player_turn = "Red"
current_shot_count = 0
previous_shot_count = 0
ball_pocketed_in_this_shot = False
# ball in hand variables
cue_ball_in_hand = False
cue_ball_dragged = False
mouse_distance_travelled = 0

show_instructions = False # a variable for the menu
mouse_held = False   # if the mouse is currently holding the cue
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
        self.x = 380
        self.y = 300
        self.direction = 0 # angle is represented in degrees
        self.speed = 0
        self.pocketed = False
        self.in_contact = False # temp?

# create an instance of each ball on the table
cue_ball = Ball()
cue_ball.colour = "White"
eight_ball = Ball() # third column, second row
eight_ball.colour = "Black"
# player one's balls (red)     # maybe make a function to make initializing the 16 balls a bit shorter
red_ball_1 = Ball() # first column, first row
red_ball_1.colour = "Red"
red_ball_2 = Ball() # second column, first row
red_ball_2.colour = "Red"

red_ball_3 = Ball() # third column, third row
red_ball_3.colour = "Red"

red_ball_4 = Ball() # fourth column, first row
red_ball_4.colour = "Red"

red_ball_5 = Ball() # fourth column, third row
red_ball_5.colour = "Red"

red_ball_6 = Ball() # fifth column, first row
red_ball_6.colour = "Red"

red_ball_7 = Ball() # fifth column, third row
red_ball_7.colour = "Red"

# player two's balls (blue)
blue_ball_1 = Ball() # second column, second row
blue_ball_1.colour = "Blue"

blue_ball_2 = Ball()
blue_ball_2.colour = "Blue"

blue_ball_3 = Ball() # fourth column, second row
blue_ball_3.colour = "Blue"

blue_ball_4 = Ball() # fourth column, fourth row
blue_ball_4.colour = "Blue"

blue_ball_5 = Ball() # fifth column, second row
blue_ball_5.colour = "Blue"

blue_ball_6 = Ball() # fifth column, fourth row
blue_ball_6.colour = "Blue"

blue_ball_7 = Ball() # fifth column, fifth row
blue_ball_7.colour = "Blue"

def reset_ball_variables():
    ### reset common variables for every ball
    for ball_instance in Ball:
        ball_instance.pocketed = False
        ball_instance.direction = 0
        ball_instance.speed = 0
        ball_instance.in_contact = False # temp?

    ### reset inividual positions
    cue_ball.x = 380 # exactly on the left third
    cue_ball.y = 300
    # temp values for testing:
    #eight_ball.x = 470
    #eight_ball.y = 300
    eight_ball.x = 670 # exactly on the right third x-value
    eight_ball.y = 300

    red_ball_1.x = 642 
    red_ball_1.y = 300

    red_ball_2.x = 656
    red_ball_2.y = 293

    red_ball_3.x = 670
    red_ball_3.y = 314

    red_ball_4.x = 684
    red_ball_4.y = 278

    red_ball_5.x = 684
    red_ball_5.y = 306

    red_ball_6.x = 698
    red_ball_6.y = 271

    red_ball_7.x = 698
    red_ball_7.y = 299

    blue_ball_1.x = 656
    blue_ball_1.y = 307

    blue_ball_2.x = 670  # third column, first row
    blue_ball_2.y = 286

    blue_ball_3.x = 684
    blue_ball_3.y = 292

    blue_ball_4.x = 684
    blue_ball_4.y = 320

    blue_ball_5.x = 698
    blue_ball_5.y = 285

    blue_ball_6.x = 698
    blue_ball_6.y = 313

    blue_ball_7.x = 698
    blue_ball_7.y = 327

    ### reset ball colours
    red_ball_1.colour = "Red"
    red_ball_2.colour = "Red"
    red_ball_3.colour = "Red"
    red_ball_4.colour = "Red"
    red_ball_5.colour = "Red"
    red_ball_6.colour = "Red"
    red_ball_7.colour = "Red"

    blue_ball_1.colour = "Blue"
    blue_ball_2.colour = "Blue"
    blue_ball_3.colour = "Blue"
    blue_ball_4.colour = "Blue"
    blue_ball_5.colour = "Blue"
    blue_ball_6.colour = "Blue"
    blue_ball_7.colour = "Blue"

reset_ball_variables()  # original ball position at the start of the game

### Drawing Functions ###
def draw_menu(game_in_progress, show_instructions):
    # get mouse position and click status
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_left = get_mouse_press()

    if show_instructions == False:
        # if mouse is hovering over a button, then highlight that button
        if mouse_x > 410 and mouse_x < 595 and mouse_y > 295 and mouse_y < 350:     # start game
            myimage = pygame.image.load("Images/menu_play.png")
            if mouse_left == True:
                game_in_progress = True
                pygame.mouse.set_pos([250,300]) # set mouse to proper starting position
        elif mouse_x > 410 and mouse_x < 595 and mouse_y > 365 and mouse_y < 420:   # show instructions
            myimage = pygame.image.load("Images/menu_instructions.png")
            if mouse_left == True:
                show_instructions = True
        elif mouse_x > 410 and mouse_x < 595 and mouse_y > 435 and mouse_y < 490:   # exit game
            myimage = pygame.image.load("Images/menu_quit.png")
            if mouse_left == True:
                pygame.quit()
        else:
            myimage = pygame.image.load("Images/menu_unselected.png")
    else: # show the instructions
        if mouse_x > 30 and mouse_x < 240 and mouse_y > 30 and mouse_y < 90:     # start game
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

    return game_in_progress, show_instructions

def draw_win_screen(win_screen, winner):
    image_selected = "Images/blue_win_selected.png"
    image = "Images/blue_win.png"
    if winner == "Blue":
        image_selected = "Images/blue_win_selected.png"
        image = "Images/blue_win.png"
    elif winner == "Red":
        image_selected = "Images/red_win_selected.png"
        image = "Images/red_win.png"

    # get mouse position and click status
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_left = get_mouse_press()

    # if mouse is hovering over a button, then highlight that button
    if mouse_x > 380 and mouse_x < 630 and mouse_y > 295 and mouse_y < 410:
        myimage = pygame.image.load(image_selected)
        if mouse_left == True:
            win_screen = False # go to main menu
    else:
        myimage = pygame.image.load(image)


    imagerect = myimage.get_rect()
    screen.fill(BLACK)
    screen.blit(myimage, imagerect)
    pygame.display.flip()

    return win_screen

def draw_static_objects():
    # Draw the playing surface
    pygame.draw.rect(screen, GREEN, [225, 150, 600, 300], 0)
    # Draw the pool table border
    pygame.draw.rect(screen, DARK_BROWN, [225, 150, 600, 300], 20)
    # Draw the pockets
    pygame.draw.circle(screen, BLACK, (235, 160), 12, 0)      # top left
    pygame.draw.circle(screen, BLACK, (525, 160), 10, 0)     # top middle
    pygame.draw.circle(screen, BLACK, (815, 160), 12, 0)     # top right
    pygame.draw.circle(screen, BLACK, (235, 440), 12, 0)     # bottom left
    pygame.draw.circle(screen, BLACK, (525, 440), 10, 0)    # bottom middle
    pygame.draw.circle(screen, BLACK, (815, 440), 12, 0)    # bottom right

def draw_scoreboard(current_player_turn):
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
        pygame.draw.circle(screen, RED, (275+ball*20, 120), 7, 0)
    
    # draw the blue balls left
    for ball in range(num_of_blue_left):
        pygame.draw.circle(screen, BLUE, (675+ball*20, 120), 7, 0)

    # Draw an indicator, showing which player's turn it is
    draw_text("Current Player:", 433, 107, GREY, 20)
    if current_player_turn == "Red":
        pygame.draw.rect(screen, RED, [593, 107, 25, 25], 0)
    elif current_player_turn == "Blue":
        pygame.draw.rect(screen, BLUE, [593, 107, 25, 25], 0)

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

def draw_text(text, x, y, colour, font_size):
    font = pygame.font.Font("fonts/PTC55F.ttf", font_size) # the font file is found within this project's directory
    label = font.render(text, 1, colour)
    screen.blit(label, (x, y))  

def draw_intro_message(time_left):
    if time_left > 0:
        draw_text("Click and drag the cue to begin", 360, 380, WHITE, 20)
        time_left -= 1
    return time_left

def draw_ball_in_hand_message(time_left):
    if time_left > 0:
        draw_text("Click and drag the cue ball to move it", 340, 380, WHITE, 20)
        time_left -= 1
    return time_left

def pulse_cue_ball(white_r, white_g, white_b, ball_pulse_multiplier, WHITE):
        # if the ball is in hand -> make it flash
        # set the cue ball drawing to a fade in/out animation
        if ball_in_hand:
            white_r += 4*ball_pulse_multiplier
            white_g += 2*ball_pulse_multiplier
            white_b += 3*ball_pulse_multiplier
            # determine whether the ball pulses 'towaards' or 'against' green or white
            if white_g < green_g or white_g > 254: # 255 is the maximum rgb value, it is set to 250 to stay safe because white_r increments by 8
                ball_pulse_multiplier *= -1

        else:
            # when the ball is not at hand, reset the ball colour and keep it static
            white_r = 255
            white_g = 255
            white_b = 255
            
        # redefine the colour of the cue ball
        WHITE = (white_r, white_g, white_b)

        return white_r, white_g, white_b, ball_pulse_multiplier, WHITE
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

def ball_to_cushion_collision(ball_direction, ball_speed, ball_x, ball_y, ball_in_contact):  
    ball_hit_cushion = False  

    if ball_in_contact == False:            
        # hit the top cushion
        if ball_y < 172:
            ball_hit_cushion = True
            ball_direction = 360 - ball_direction
                
        # hit the bottom cushion
        if ball_y > 430:
            ball_hit_cushion = True
            ball_direction = 360 - ball_direction

        # hit the left cushion
        if ball_x < 245:
            ball_hit_cushion = True
            if ball_direction > 180 and ball_direction < 270: # ball incoming from the bottom
                ball_direction = 540 - ball_direction
            elif ball_direction > 90 and ball_direction < 180:                   # ball coming from the top
                ball_direction = 180 - ball_direction
            elif ball_direction == 180: # direct hit
                ball_direction = 180

        # hit the right cushion
        if ball_x > 805:
            ball_hit_cushion = True
            if ball_direction > 270 and ball_direction < 360: # ball incoming from the bottom
                ball_direction = 540- ball_direction
            elif ball_direction > 0 and ball_direction < 90:                   # ball coming from the top 
                ball_direction = 180 - ball_direction
            elif ball_direction == 0: # direct hit
                ball_direction = 0
    else:
        ball_in_contact = False
    return ball_direction, ball_speed, ball_in_contact

def ball_to_ball_collision(ball_direction, ball_speed, ball_x, ball_y):
    for ball_instance in Ball:
        # make sure the ball is not comparing it's location, with it's self
        if ball_x != ball_instance.x and ball_y != ball_instance.y:
            # check if the cue ball is touching/contacts the eight ball
            if ball_x > ball_instance.x-7 and ball_x < ball_instance.x+14: # check the x-axis
                if ball_y > ball_instance.y-14 and ball_y < ball_instance.y+14: # check the y-axis
                    # now it is confirmed that they are in contact
                    if ball_instance.in_contact == False: # make sure it doesn't do the below twice, for only one contact
                        ball_instance.direction = get_angle(ball_instance.x, ball_instance.y, ball_x, ball_y)
                        ball_instance.speed = ball_speed*0.97
                        ball_speed *= 0.90
                            
                        ball_instance.in_contact = True
                else: # passed one test but is ultimately not in contact
                    if ball_instance.in_contact == True:
                        ball_instance.in_contact = False
            else: # not in contact
                if ball_instance.in_contact == True:
                        ball_instance.in_contact = False
    return ball_direction, ball_speed

def check_if_ball_pocketed(ball_x, ball_y):
    ball_pocketed = False # maght not be necessary, because it is assumed the only the unpocketed ball instances go through  'manage_ball_status()', and in turn, this function.
    # check the top left pocket
    if ball_x > 225 and ball_x < 245 and ball_y > 160 and ball_y < 180:
        # check to see if the ball is touches a 20x20 px zone ## may need to keep in mind that the x and y values of a ball may be at the top right of the sprite.
        ball_pocketed = True
    # check the top middle pocket
    elif ball_x > 525 and ball_x < 545 and ball_y > 160 and ball_y < 172:
        ball_pocketed = True
    # check the top right pocket
    elif ball_x > 805 and ball_x < 825 and ball_y > 160 and ball_y < 180:
        ball_pocketed = True
    # check the bottom right pocket
    elif ball_x > 805 and ball_x < 825 and ball_y > 420 and ball_y < 440:
        ball_pocketed = True
    # check the bottom middle pocket
    elif ball_x > 525 and ball_x < 545 and ball_y > 430 and ball_y < 440:
        ball_pocketed = True
    # check the bottom left pocket
    elif ball_x > 225 and ball_x < 245 and ball_y > 420 and ball_y < 440:
        ball_pocketed = True
        
    return ball_pocketed

def manage_ball_status(ball_direction, ball_x, ball_y, ball_speed, ball_pocketed, ball_in_contact):
    # check for a ball to wall collision
    ball_direction, ball_speed, ball_in_contact = ball_to_cushion_collision(ball_direction, ball_speed, ball_x, ball_y, ball_in_contact)
    # check for a ball to ball collision
    ball_direction, ball_speed = ball_to_ball_collision(ball_direction, ball_speed, ball_x, ball_y)
    
    ### change the ball's cartesian value based on its direction and speed
    ball_x_increment, ball_y_increment = angle_to_coordinates(ball_direction, ball_x, ball_y)


    ball_x += ball_x_increment*ball_speed/4
    ball_y += ball_y_increment*ball_speed/4
    # gradually reduce the ball's speed due to gravity
    ball_speed -= 0.018 #0.095

    ## Check if it gets pocketed
    ball_pocketed = check_if_ball_pocketed(ball_x, ball_y)
    return ball_direction, ball_x, ball_y, ball_speed, ball_pocketed, ball_in_contact

def check_if_balls_moving():
    no_movement_so_far = True # will be true if the balls were moving in the last frame
    for ball_instance in Ball:   
        if ball_instance.speed <= 0.01 and no_movement_so_far == True:
            no_movement_so_far = True
        else:
            if ball_instance.pocketed == False:
                no_movement_so_far = False
                        
    if no_movement_so_far == True:
        return False
    else:
        return True

def ball_in_hand():
    # reset cue ball variables
    cue_ball.pocketed = False
    cue_ball.x = 380
    cue_ball.y = 300
    cue_ball.speed = 0
    cue_ball.direction = 0
    # reset mouse position
    pygame.mouse.set_pos([275,300])
    
def determine_guideline(cue_end_point_x, cue_end_point_y, cue_front_x, cue_front_y, mouse_degs):
    guideline_length = 0
    object_touched = False

    # limit to cushions
    while object_touched == False:
        cue_end_point_x, cue_end_point_y = convert_polar_coordinates_to_cartesian(cue_end_point_x, cue_end_point_y, mouse_degs, guideline_length)
        if cue_end_point_x < 245 or cue_end_point_x > 805 or cue_end_point_y < 172 or cue_end_point_y > 430:
            object_touched = True
        else:
            guideline_length += 1


    return cue_end_point_x, cue_end_point_y    

def check_if_game_over(game_in_progress, current_player_turn):
    winner = "unknown"
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
    return game_in_progress, winner

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
            ball_pocketed_in_this_shot = False # reset the ball pocketed count (for the current shot)

    return current_player_turn, current_shot_count, previous_shot_count, ball_pocketed_in_this_shot

pygame.init()
# Set the width and height of the screen [width, height]
size = (1050, 600)
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
        if win_screen == True:
            win_screen = draw_win_screen(win_screen, winner)
        
        else:
            win_screen = False
            game_in_progress = False
            winner = "unknown"  
            game_in_progress, show_instructions = draw_menu(game_in_progress, show_instructions)  

        reset_ball_variables()

    elif game_in_progress == True:       
        ### Drawing the playing area ###
        screen.fill(BLACK) # background
        draw_static_objects()
        draw_scoreboard(current_player_turn)
        draw_balls()

        # draw in-game messages
        intro_message = draw_intro_message(intro_message)
        ball_in_hand_message = draw_ball_in_hand_message(ball_in_hand_message)
        
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

                # enable ball dragging if the ball is in hand, AND the mouse has clicked on the ball
                if orig_mouse_x < cue_ball.x + 10 and  orig_mouse_x > cue_ball.x - 10:
                        if orig_mouse_y < cue_ball.y + 10 and orig_mouse_y > cue_ball.y - 10:
                            cue_ball_dragged = True
            # the duration of time WHILE the mouse is being clicked/held
            elif mouse_left == True and mouse_held == True:                
            # in the case that the ball is in hand
                if cue_ball_in_hand:
                    if cue_ball_dragged == True:
                            cue_ball.x = mouse_x
                            cue_ball.y = mouse_y
                else:
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
                
            # mouse is released AFTER being clicked at first
            elif mouse_left == False and mouse_held == True:
                # ensure that there are no false positive (ex. if the user clicks and releases the cue without dragging it)
                if mouse_distance_travelled > 5:
                    # if the ball is in hand, "remove" in from that hand...
                    if cue_ball_in_hand:
                        cue_ball_in_hand = False
                        cue_ball_dragged = False
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
                if ball_instance.speed > 0.01 and ball_instance.pocketed == False:
                    # one function that does it all, for this ball
                    ball_instance.direction, ball_instance.x, ball_instance.y, ball_instance.speed, ball_instance.pocketed, ball_instance.in_contact = manage_ball_status(ball_instance.direction, ball_instance.x, ball_instance.y, ball_instance.speed, ball_instance.pocketed, ball_instance.in_contact)
                    # check and see if the player has pocketed the correct ball (and use this later to determine whether the player retains possesion for the next shot)
                    if ball_instance.pocketed == True and ball_instance.colour == current_player_turn:
                        ball_pocketed_in_this_shot = True
         
            # if all balls have stopped moving, then inform the if statement above
            balls_in_movement = check_if_balls_moving()
                
        ### Updating the cue's position and drawing it ###
        # Ball is currently in the opponents hand...until the next shot is made
        if cue_ball.pocketed:
            cue_ball_in_hand = True
            # if the balls have stopped moving -> reset ball variable (should be a one time thing)
            if balls_in_movement == False:   
                ball_in_hand()
                ball_in_hand_message += 1200 # show user how to drag the ball - for 5 seconds

        # ball is able to be dragged around by the player currently in possession
        if cue_ball_in_hand:
            # pulse the cue ball, when the ball is in hand
            white_r, white_g, white_b, ball_pulse_multiplier, WHITE = pulse_cue_ball(white_r, white_g, white_b, ball_pulse_multiplier, WHITE)
        else:
            # reset the white colour values
            WHITE = (255, 255, 255) # cue ball            # duplicate?
        

        # show the cue when the balls have stopped moving
        if balls_in_movement == False:
            # switch player turn if necessary
            current_player_turn, current_shot_count, previous_shot_count, ball_pocketed_in_this_shot = determine_player_turn(current_player_turn, current_shot_count, previous_shot_count, ball_pocketed_in_this_shot)

            # Get the angle between the mouse and the cue ball
            mouse_degs = get_angle(cue_ball.x, cue_ball.y, mouse_x, mouse_y)
            
            cue_front_x = mouse_x
            cue_back_x = mouse_x
            cue_front_y = mouse_y
            cue_back_y = mouse_y

            # Get the length of the cue
            mouse_to_ball_length = get_distance(cue_ball.x, cue_ball.y, cue_front_x, cue_front_y)
            
            # limit the length of the cue
            cue_length = mouse_to_ball_length-200-cue_buffer
            ball_to_cue_distance = mouse_to_ball_length-20-cue_buffer
            
            # get two pairs of the cue's coordinates from their polar coordinates (mouse angle + distance from the cue ball)
            cue_front_x, cue_front_y = convert_polar_coordinates_to_cartesian(cue_front_x, cue_front_y, mouse_degs, cue_length)
            cue_back_x, cue_back_y = convert_polar_coordinates_to_cartesian(cue_back_x, cue_back_y, mouse_degs, ball_to_cue_distance)

            # draw the cue
            pygame.draw.line(screen, BROWN, (cue_front_x, cue_front_y), (cue_back_x, cue_back_y), 5)
            # we know one end of the guideline (the cue ball), now get the other end
            cue_end_point_x = cue_back_x
            cue_end_point_y = cue_back_y
            cue_end_point_x, cue_end_point_y = determine_guideline(cue_end_point_x, cue_end_point_y, cue_front_x, cue_front_y, mouse_degs)
            # draw the guideline
            pygame.draw.line(screen, WHITE, (cue_ball.x, cue_ball.y), (cue_end_point_x, cue_end_point_y), 1)

        ### Game end and player turns ###
        # if the game seems to be done -> show winner -> then return to main menu
        game_in_progress, winner = check_if_game_over(game_in_progress, current_player_turn)
        if game_in_progress == False:
            win_screen = True

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit frames per second
    clock.tick(240)
 
# Close the window and quit.
pygame.quit()