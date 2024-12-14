import pygame
import random
import math
import time
from pygame import mixer

# Stopwatch Start
BEGIN = pygame.time.get_ticks()
# initializing pygame
pygame.init()

# creating screen)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# caption and icon
pygame.display.set_caption("Welcome to Space Invaders")


# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))


# player
playerImage = pygame.image.load('Random-Python-Games/Space Invaders/spaceship.png')
player_X = 380
player_Y = 520
player_Xchange = 0

# Invader
invaders_presetX = []
invaders_presetY = []
no_of_invaders = 16
invaderImage = []
invader_Xchange = []
invader_Ychange = []
invader_X = []
invader_Y = []
invader_change = 0.1

for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('Random-Python-Games/Space Invaders/alien.png'))
    invaders_presetX.append(100 + 80 * (num % 8))
    invaders_presetY.append(45 + (num // 8) * 45)
    invader_Xchange.append(invader_change)
    invader_Ychange.append(90)

for i in range(no_of_invaders):
    invader_X.append(invaders_presetX[i])
    invader_Y.append(invaders_presetY[i])

# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('Random-Python-Games/Space Invaders/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 2
bullet_state = "rest"


# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 40:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


def invader(x, y, a):
    screen.blit(invaderImage[a], (x, y))


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"


# game loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controlling the player movement
        # From the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -1
            if event.key == pygame.K_RIGHT:
                player_Xchange = 1
            if event.key == pygame.K_SPACE:
                # Fixing the change of direction of bullet
                if bullet_state == "rest":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
        if event.type == pygame.KEYUP:
            player_Xchange = 0

    if no_of_invaders < 1:
        no_of_invaders = 16
        invader_change += 0.1
        for i in range(no_of_invaders):
            invader_X.append(invaders_presetX[i])
            invader_Y.append(invaders_presetY[i])
        for num in range(no_of_invaders):
            invaderImage.append(pygame.image.load('alien.png'))
            invader_Xchange.append(invader_change)
            invader_Ychange.append(90)

    # adding the change in the player position
    player_X += player_Xchange
    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state == "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange

    # movement of the invader
    for i in range(no_of_invaders):
        if invader_Y[i] >= 480:
            if abs(player_X-invader_X[i]) < 80:
                for j in range(no_of_invaders):
                    invader_Y[j] = 2000
                game_over()
                break

        if invader_X[i] >= 725 or invader_X[i] <= 10:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]

        invader(invader_X[i], invader_Y[i], i)

    for i in range(no_of_invaders):
        # Collision
        if isCollision(bullet_X, invader_X[i] + 30, bullet_Y, invader_Y[i] + 20):
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
            no_of_invaders -= 1
            invader_X.pop(i)
            invader_Y.pop(i)
            invader_Xchange.pop(i)
            invader_Ychange.pop(i)
            break

    # restricting the spaceship so that
    # it doesn't go out of screen
    if player_X <= 20:
        player_X = 20
    elif player_X >= 760:
        player_X = 760



    player(player_X, player_Y)
    show_score(scoreX, scoreY)
    pygame.display.update()
