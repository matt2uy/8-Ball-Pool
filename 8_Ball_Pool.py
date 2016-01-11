# Name: Matthew Uy
# Date: December 7, 2015
# Assignment: CPT - "8 Ball Pool"
# Description: maybe put it on github? (on monday jan 11?)
# Lab requirements: ?

import pygame

# Got the colour values from http://www.colorpicker.com/
# The variables below each colour initialization represent how...
# ... colour's RGB values will change as the sun "sets"


##################################3
         # TEMP

mouse_released = False
cue_end_x = 0
cue_end_y = 0

##### will make an object for each ball
cue_ball_x = 220
cue_ball_y = 200
cue_ball_direction = 0 # angle is represented in degrees
cue_ball_speed = 0
balls_in_movement = False # balls are undergoing movement, means that the cue can't be moved at this time

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
    pygame.draw.circle(screen, WHITE, (cue_ball_x, cue_ball_y), 8, 0)
    pygame.draw.circle(screen, YELLOW, (525, 200), 8, 0)
    pygame.draw.circle(screen, BLACK, (190, 90), 8, 0)


    # Check for mouse press
    mouse_left = False
    mouse_middle = False
    mouse_right = False

    mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()


    
    # Update the cue's position + check whether the cue has hit the ball
    if balls_in_movement == False:
        if mouse_left == False:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_released = True
        else: # mouse is clicked
            if mouse_released == True: # hit the ball
                print "ball hit at", mouse_degs, "degrees"
                # set the cue ball variables and set the balls_in_movement variable in motion
                cue_ball_speed = 10
                cue_ball_direction = mouse_degs
                balls_in_movement = True
                mouse_released = False
    else: # cue has hit the ball and the balls are moving
        print "balls are moving now..."
        if cue_ball_speed > 0: # this means that the ball is not stationary at this frame
            # diagnostic stuff being printed...
            print "cue ball speed:", cue_ball_speed
            print "cue ball direction: ", cue_ball_direction
            ### Move the ball in the correct direction based on cue_ball_direction
            # if it's in q1 or q2, then we know for sure that the ball should move down at least one pixel
            if cue_ball_direction < 360 and cue_ball_direction > 180:
                cue_ball_y += cue_ball_speed

                ###### convert angle(polar coordinates) to coordinates
                ######### https://www.mathsisfun.com/polar-cartesian-coordinates.html
                ##### https://www.google.ca/search?q=python+polar+coordinates&ie=utf-8&oe=utf-8&gws_rd=cr,ssl&ei=39KNVtyaGcOzaYC_kpgM
                #cue_ball_x, cue_ball_y = angle_to_coordinates(cue_ball_direction)
            
            # ... then recalculate the resulting ball angle, and if it is greater, then move it up one. 
            # repeat the above if the ball angle is in q3 or 4
            
            ### Move the ball at the correct speed
            # gradually reduce the ball's speed due to gravity
            cue_ball_speed -= 1 

            
    
    # Draw the mouse pointer
    pygame.draw.rect(screen, BROWN, (mouse_x-5, mouse_y-5, 10, 10), 0)

    ########################
    
    # Get the angle between the mouse and the cue ball
    from math import atan2, degrees, pi
    dx = cue_ball_x - mouse_x
    dy = cue_ball_y - mouse_y
    rads = atan2(-dy,dx)
    rads %= 2*pi
    mouse_degs = degrees(rads)
    #print mouse_degs
    
    cue_end_x = mouse_x
    cue_end_y = mouse_y

    
    # Get cue end to ball length (AKA: length of the cue)
    from math import sqrt
    cue_length = sqrt((cue_ball_x - cue_end_x)**2 + (cue_ball_y - cue_end_y)**2)
    #print cue_length

    ''' #maybe for later... 11:32 am      1/6/16
    # if cue length is exceeded, then shorten it while keeping the angle
    if cue_length > 100:
        # while in "q2"
        if mouse_degs > 225 and mouse_degs < 315:
            ###### Fix the vertical movement of the cue (keep it around 80 px long)
            # bring cue down twenty px
            # Get cue end to ball length (AKA: length of the cue)
            from math import sqrt
            cue_length = sqrt((cue_ball_x - cue_end_x)**2 + (cue_ball_y - cue_end_y)**2)
            #print cue_length

            while cue_length > 80:
                cue_end_y += 1
                # get cue length
                cue_length = sqrt((cue_ball_x - cue_end_x)**2 + (cue_ball_y - cue_end_y)**2)
                print cue_length

            ###### Fix the lateral movement of the cue
            # Get the angle between the cue end and the cue ball
            from math import atan2, degrees, pi
            dx = cue_ball_x - cue_end_x
            dy = cue_ball_y - cue_end_y
            rads = atan2(-dy,dx)
            rads %= 2*pi
            cue_degs = degrees(rads)

            # if angle of cue is greater than 270, move left until the angles are equal?
            if cue_degs > 270:
                while cue_degs < mouse_degs-1 or cue_degs > mouse_degs+1:
                    cue_end_x += 1
                    # Get the angle between the cue end and the cue ball
                    from math import atan2, degrees, pi
                    dx = cue_ball_x - cue_end_x
                    dy = cue_ball_y - cue_end_y
                    rads = atan2(-dy,dx)
                    rads %= 2*pi
                    cue_degs = degrees(rads)
            # do the same if the angle is lesser than 270
            if cue_degs < 270:
                cue_end_x -= 20
                # Get the angle between the cue end and the cue ball
                from math import atan2, degrees, pi
                dx = cue_ball_x - cue_end_x
                dy = cue_ball_y - cue_end_y
                rads = atan2(-dy,dx)
                rads %= 2*pi
                cue_degs = degrees(rads)
            
            
            ##############
            # Get cue end to ball length (AKA: length of the cue)
            cue_length = sqrt((cue_ball_x - cue_end_x)**2 + (cue_ball_y - cue_end_y)**2)


            ##############
            
            if mouse_degs > 225:
                cue_end_y += 10
            else:
                cue_end_y -= 10'''
                
                
    '''
        ##############
        # Get the angle between the cue end and the cue ball
        from math import atan2, degrees, pi
        dx = cue_ball_x - cue_end_x
        dy = cue_ball_y - cue_end_y
        rads = atan2(-dy,dx)
        rads %= 2*pi
        cue_degs = degrees(rads)

        # move the cue end "inwards", which keeps the cue at a constant length
        if mouse_degs > 180 and mouse_degs < 360: # mouse to ball angle in q1 or 2
            cue_end_y -= 1
        else: # in q3-4
            cue_end_y += 1

        if cue_degs > mouse_degs: # maybe change variable name to mouse_angle?
            cue_end_x -= 1
        elif cue_degs < mouse_degs:
            cue_end_x += 1

        # Get cue end to ball length (AKA: length of the cue)
        cue_length = sqrt((cue_ball_x - cue_end_x)**2 + (cue_ball_y - cue_end_y)**2)
        '''
    
    # draw the stick when the balls aren't moving
    if balls_in_movement == False:
        pygame.draw.line(screen, BROWN, (cue_end_x, cue_end_y), (cue_ball_x, cue_ball_y), 5)
    


    '''
    while cue_and_stick_angle_aligned == False:
        if stick_length < 260:
            # fix horizontal movement of the cue
            if mouse_degs > 0 and mouse_degs < 180:
                if cue_degs != mouse_degs:
                    if cue_degs < mouse_degs:
                        cue_end_x += 1
                    elif cue_degs > mouse_degs:
                        cue_end_x -= 1
                        
                #if mouse_degs < 90: # mouse is in quadrant 1

                            
                #if mouse_degs >= 90: # mouse is in quadrant 2
            if mouse_degs > 180 and mouse_degs < 360:
                if cue_degs != mouse_degs:
                    if cue_degs < mouse_degs:
                        cue_end_x -= 1
                    elif cue_degs > mouse_degs:
                        cue_end_x += 1
                #if mouse_degs < 270: #mouse in q3
                #if mouse_degs >= 270: # mouse in q4
        cue_and_stick_angle_aligned = True
    '''
            
        
    
    '''if cue_end_x < mouse_x:
        cue_end_x += (mouse_x - cue_end_x)
    if cue_end_x > mouse_x:
        cue_end_x -= (cue_end_x - mouse_x)'''
    '''if cue_end_y < mouse_y:
        cue_end_y += (mouse_y - cue_end_y)
    if cue_end_y > mouse_y:
        cue_end_y -= (cue_end_y - mouse_y)'''
            

    
    '''

     keep moving to mouse until it meets the angle, but has one end with the ball and the other being made to match the cue to mouse angle
        
    '''
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(30)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
