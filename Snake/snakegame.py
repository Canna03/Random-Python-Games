#########################################
# File Name: SnakeTemplate.py
# Description: This program is a template for Snake Game.
#              It demonstrates how to move and lengthen the snake.
# Author: ICS2O
# Date: 02/11/2018
#########################################
from random import randint
import pygame
import random

pygame.init()
WIDTH = 800
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

TOP = 0
BOTTOM = HEIGHT
MIDDLE = 390
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (126, 205, 128)
RED = (199, 55, 47)
outline = 0


# ---------------------------------------#
# functions                             #
# ---------------------------------------#
def redrawGameWindow():
    gameWindow.fill(GREEN)
    pygame.draw.rect(gameWindow, BLUE, (0, 0, 800, 100), 0)

    font = pygame.font.SysFont("Microsoft Sans Serif",
                                        25)  # Importing font "Microsoft Sans Serif" for Score and Time
    score = font.render("Score: " + str(scoreV), True, BLACK)
    gameWindow.blit(score, (40, 30))

    timer = font.render("Timer: " + str(time), True, BLACK)
    gameWindow.blit(timer, (640, 30))

    segR = 210
    segG = 180
    segB = 200
    for i in range(len(segX)):
        if i == 0:
            pygame.draw.rect(gameWindow, (106, 13, 173), (segX[i] - 10, segY[i] - 10, 20, 20), 0)
            continue
        else:
            if segR >= 3:
                segR -= 3
            if segG >= 3:
                segG -= 3
        pygame.draw.rect(gameWindow, (segR, segG, segB), (segX[i] - 10, segY[i] - 10, 20, 20), 0)


    for i in range(len(appleX)):
        pygame.draw.circle(gameWindow, RED, (appleX[i], appleY[i]), SEGMENT_R, outline)

    pygame.display.update()


def addApple(x, y, a, b):
    appX = random.randrange(10, 790, 20)
    appY = random.randrange(110, 590, 20)
    while True:
        if appX not in x and appY not in y and appX not in a and appY not in b:
            break
        appX = random.randrange(10, 790, 20)
        appY = random.randrange(110, 590, 20)

    return [appX, appY]

# ---------------------------------------#
# main program                          #
# ---------------------------------------#
print("Use the arrows and the space bar.")
print("Hit ESC to end the program.")

# snake's properties
scoreV = 0
SEGMENT_R = 10
HSTEP = 20
VSTEP = 20
stepX = 0
stepY = -VSTEP  # initially the snake moves upwards
segX = []
segY = []
speed = 60

appleX = []
appleY = []
for i in range(4):  # add coordinates for the head and 3 segments
    segX.append(MIDDLE)
    segY.append(590 + i * VSTEP - 20)


# ---------------------------------------#
lost = False
appleNotEaten = True
appleTimer = 60
inPlay = True
begin = pygame.time.get_ticks()
while inPlay:
    elapsed = pygame.time.get_ticks() - begin
    time = round((60 * 1000 - elapsed) / 1000)

    if speed > 20:
        speed = 60 - (scoreV // 5) * 5

    if appleTimer == time:
        appleTimer -= 10
        new = addApple(appleX, appleY, segX, segY)
        appleX.append(new[0])
        appleY.append(new[1])

    pygame.event.clear()
    redrawGameWindow()
    pygame.time.delay(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    if keys[pygame.K_LEFT]:
        if stepY != 0:
            stepX = -HSTEP
            stepY = 0
    if keys[pygame.K_RIGHT]:
        if stepY != 0:
            stepX = HSTEP
            stepY = 0
    if keys[pygame.K_UP]:
        if stepX != 0:
            stepX = 0
            stepY = -VSTEP
    if keys[pygame.K_DOWN]:
        if stepX != 0:
            stepX = 0
            stepY = VSTEP
    if keys[pygame.K_SPACE]:  # if space bar is pressed, add a segment:
        if appleNotEaten:
            segX.append(segX[-1])  # assign it the same x and y coordinates
            segY.append(segY[-1])  # as those of the last segment (at index -1)

    if segX[0] > 800 or segX[0] < 0 or segY[0] < 100 or segY[0] > 600:
        inPlay = False
        lost = True

    # move the segments
    lastIndex = len(segX) - 1
    for i in range(lastIndex, 0, -1):  # starting from the tail, and going backwards:
        segX[i] = segX[i - 1]  # every segment takes the coordinates
        segY[i] = segY[i - 1]  # of the previous one
    # move the head
    segX[0] = segX[0] + stepX
    segY[0] = segY[0] + stepY

    for i in range(len(appleX)):
        if appleX[i] == segX[0] and appleY[i] == segY[0]:
            segX.append(segX[-1])
            segY.append(segY[-1])
            appleX.pop(i)
            appleY.pop(i)
            appleNotEaten = False
            scoreV += 1

            new = addApple(appleX, appleY, segX, segY)
            appleX.append(new[0])
            appleY.append(new[1])

    for i in range(1, len(segX)):
        if segX[0] == segX[i] and segY[0] == segY[i]:
            inPlay = False
            lost = True
            break

if lost:
    gameWindow.fill(RED)
    font = pygame.font.SysFont("Microsoft Sans Serif",
                                        60)  # Importing font "Microsoft Sans Serif" for Score and Time
    lose = font.render("You Lost!", True, BLACK)
    gameWindow.blit(lose, (270, 260))
    pygame.display.update()

    pygame.time.delay(2000)

else:
    gameWindow.fill(GREEN)
    font = pygame.font.SysFont("Microsoft Sans Serif",
                                        60)  # Importing font "Microsoft Sans Serif" for Score and Time
    lose = font.render("Your score is " + str(scoreV) + "!", True, BLACK)
    gameWindow.blit(lose, (180, 260))
    pygame.display.update()

    pygame.time.delay(2000)




# ---------------------------------------#
pygame.quit()