#Snake Game Program
#Ms. Stretten - Grade 10 Computer Science
#5/6/2021
#Joy Li

import pygame
from pygame import mixer
import tkinter
from tkinter import messagebox
import math
import random

#Defining Functions

#draw_screen method updates the win surface with the new display
def draw_screen():

    win.fill(background)
    fontSnake = pygame.font.SysFont("Agency FB", 75)  # Importing font "Agency FB" for title
    snake = fontSnake.render("SNAKE GAME", True, green)  # Rendering text for title
    win.blit(snake, (25, 25))  # Printing "SNAKE GAME" on game

    fontScoreTime = pygame.font.SysFont("Microsoft Sans Serif",
                                        20)  # Importing font "Microsoft Sans Serif" for Score and Time
    score = fontScoreTime.render("Score: " + str(scoreValue), True, green)
    win.blit(score, (25, 125))
    timeprint = fontScoreTime.render("Time: " + str(math.floor(timeValue/1000)), True, green)
    win.blit(timeprint, (425, 125))
    levelprint = fontScoreTime.render("Level: " + str(levelValue), True, green)
    win.blit(levelprint, (225, 125))


    win.blit(currentSound, (525, 25)) # Showing Sound On image default on screen

    #Draws the game space that the snake will be in
    pygame.draw.rect(win,green,(0,150,600,750))

    for i in range(len(snakeXValues)):
        pygame.draw.rect(win, snakeColor[i], (snakeXValues[i], snakeYValues[i], bodySize, bodySize)) # Drawing the snake

    for i in range(len(foodXValues)):
        pygame.draw.rect(win, apple, (foodXValues[i], foodYValues[i], 25, 25))  # Drawing the Apples

# Initiating programs
pygame.init()
mixer.init()

#Colors
background = (235, 255, 179)
green = (126, 205, 128)
head = (10, 200, 129)
a = 100
b = 230
c = 130
body = (a,b,c)
black = (0,0,0)
apple = (255,223,120)

#Set Screen
height = 900
width = 600
win = pygame.display.set_mode((width, height)) #Setting Window
pygame.display.set_caption("Snake Game") #Naming Program Window
win.fill(background)

playX = 550 #Play Area X Width
playY = 750 #Play Area Y Length
pygame.draw.rect(win, green, (25, 150, playX, playY)) #Active Playing Area

#Playing Music
bgMusic = mixer.music.load("BackgroundMusic.wav") #imports music
mixer.music.play(-1) #Playing Music Infinitely

#Sound Graphics
soundOn = pygame.image.load("Sound on.png") #Loading Sound On Image
soundOff = pygame.image.load("Sound off.png") #Loading Sound Off Image
currentSound = soundOn

#Score Time and Level
scoreValue = 0
timeValue = 0
levelValue = 0

#Snake Properties
bodySize = 25
snakeX = playX/2
snakeY = playY/2
moveX = 25
moveY = 25

snakeXValues = [snakeX]
snakeYValues = [snakeY]
snakeColor = [head]

speedX = 0
speedY = moveY

pauseX = 0
pauseY = 0


# Speed of the game
speedGame = 75

#Apple Values
foodX = random.randrange(25, playX + 25, 25) #Generating Random X coordinate for apple
foodY = random.randrange(150, playY + 150, 25) #Generating Random Y coordinate for apple

foodXValues = [foodX]
foodYValues = [foodY]

#Apple timer
newappletime = 0


#Updating the screen before the game starts
draw_screen()

pause = False
game = True
#Main program
while game: #Running Pygame
    pygame.time.delay(speedGame) #Updates the screen at the interval of the variable speedGame

    spacePressed = False

    #Detects pygame actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        keys = pygame.key.get_pressed()
        # act upon key events
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            game = False


        if keys[pygame.K_SPACE]:

            #Adds 1 to the score and increases the snakes length by 1
            if spacePressed == False:
                # Add length to snake
                snakeXValues.append(snakeXValues[0])
                snakeYValues.append(snakeYValues[0])

                # Changes the color of the snakes body by a little bit
                if a < 255:
                    a = a + 1
                if b > 0:
                    b = b - 1
                if c < 255:
                    c = c + 1
                body = (a, b, c)

                # Adds the color of the snake to the snakeColor array
                snakeColor.append(body)

                # Increases the score by 1
                scoreValue = scoreValue + 1

                #Fixes a problem that increases the length by 2 when pressing the space bar
                spacePressed = True
            else:
                spacePressed = False

        #Changes the direction of the snake to the left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not speedX == moveX or len(snakeXValues) == 1:
                speedX = -moveX
                speedY = 0

        #Changes the direction of the snake to the right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not speedX == -moveX or len(snakeXValues) == 1:
                speedX = moveX
                speedY = 0

        #Changes the direction of the snake to the up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if not speedY == moveY or len(snakeXValues) == 1:
                speedX = 0
                speedY = -moveY

        #Changes the direction of the snake to the down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if not speedY == -moveY or len(snakeXValues) == 1:
                speedX = 0
                speedY = moveY

        #Pauses game
        if keys[pygame.K_TAB]:
            if (not speedX == 0 or not speedY == 0) and pause == False:
                pauseX = speedX
                pauseY = speedY
                speedX = 0
                speedY = 0
                pause = True
            #Unpauses game
            else:
                speedX = pauseX
                speedY = pauseY
                pause = False

        #Obtaining Mouse Coordinates - Storing them in mouse (x, y)
        mouseX, mouseY = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN: #If Mouse is pressed
            if 525 <= mouseX <= 575 and 25 <= mouseY <= 75 and pygame.mixer.music.get_busy() == True: #If mouse is pressed on
                # Sound Icon and music is playing, pause music
                pygame.draw.rect(win, background, (525, 25, 50, 50)) #Hide Sound Icon below
                currentSound = soundOff #Changes the image to the soundOff image
                pygame.mixer.music.pause() #Pause music
                draw_screen()

            elif 525 <= mouseX <= 575 and 25 <= mouseY <= 75 and pygame.mixer.music.get_busy() == False:  #If mouse is pressed on
                # Sound Icon and music is not playing, play music
                pygame.draw.rect(win, background, (525, 25, 50, 50)) #Hide Sound Icon below
                currentSound = soundOn #Changes the image to the soundOn image
                pygame.mixer.music.unpause() #Play music
                draw_screen()
    pygame.display.update()

    if pause:
        continue

    for i in range(len(snakeXValues) - 1, 0, -1):  # start from the tail, and go backwards
        snakeXValues[i] = snakeXValues[i - 1]  # every segment takes the coordinates
        snakeYValues[i] = snakeYValues[i - 1]  # of the previous one
    # move the head
    snakeXValues[0] = snakeXValues[0] + speedX
    snakeYValues[0] = snakeYValues[0] + speedY

    #Boolean variable to check if the snake as hit itself
    hitItself = False

    #Checks if the snakes head's coordinates are the same as any of the snakes body's coordinates
    for i in range(1,len(snakeXValues)):
        if snakeXValues[0] == snakeXValues[i] and snakeYValues[0] == snakeYValues[i]:
            hitItself = True
            break


    #Ends the game if the snake has left the frame of the game or the hitItself boolean is True
    if snakeXValues[0] < 0 or snakeXValues[0] > 575 or snakeYValues[0] > 875 or snakeYValues[0] < 150 or hitItself:
        pygame.quit()
        game = False
        break

    #Checks to see if an apple has been eaten
    for i in range(len(foodXValues)):
        #Checks if the head of the snake is touching any of the apples
        if snakeXValues[0] == foodXValues[i] and snakeYValues[0] == foodYValues[i]:

            #Creates a new apple randomly placed anywhere that is not on the snake
            for j in range(len(snakeXValues)):
                while foodXValues[i] == snakeXValues[j] and foodYValues[i] == snakeYValues[j]:
                    foodXValues[i] = random.randrange(25, playX + 25, 25)
                    foodYValues[i] = random.randrange(150, playY + 150, 25)

            #Add length to snake
            snakeXValues.append(snakeXValues[0])
            snakeYValues.append(snakeYValues[0])

            #Changes the color of the snakes body by a little bit
            if a < 255:
                a = a + 1
            if b > 0:
                b = b - 1
            if c < 255:
                c = c + 1
            body = (a,b,c)

            #Adds the color of the snake to the snakeColor array
            snakeColor.append(body)

            #Increases the score by 1
            scoreValue = scoreValue + 1

            #Resets the 10 second new apple timer
            newappletime = 0

    # If the apple timer reached 10 seconds, create a new apple and reset the timer
    if newappletime > 10000:
        foodXValues.append(random.randrange(25, playX + 25, 25))
        foodYValues.append(random.randrange(150, playY + 150, 25))
        newappletime = 0
    # Else add the current speed of the game to the apple timer
    else:
        newappletime = newappletime + speedGame

    #Draw the new screen using the draw_screen method
    draw_screen()

    # Update the time
    timeValue = timeValue + speedGame

    #Change the speed of the game and the level of the game according to the user's scoreaa
    levelValue = math.floor(scoreValue/20) #Every 20 points, level changes
    speedGame = 75 - levelValue * 5 #Game gets faster every level


    pygame.display.update()



# Creates a message box showing the user's score, level and the amount of time survived

root = tkinter.Tk()
root.withdraw()

wordSecond = " seconds!"
if math.floor(timeValue/2000) == 1:
    wordSecond = " second!"

tkinter.messagebox.showinfo('GAME OVER!','You finished with ' + str(scoreValue) + ' points at level ' + str(levelValue) + ' and you played for ' + str(math.floor(timeValue/1000)) + wordSecond)