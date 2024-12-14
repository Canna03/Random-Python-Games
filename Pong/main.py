from random import randint
import pygame

pygame.init()
WIDTH = 800
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

TOP = 0
BOTTOM = HEIGHT
MIDDLE = WIDTH // 2
LEFT = 0
RIGHT = WIDTH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (75, 230, 255)
outline = 0

foodx = round(randint(2, 38) * 20)
foody = round(randint(2, 28) * 20)
end = False
inPlay = True
win = False
score = 0
speed = 60
speedLimit = 0
clock = 60


# ---------------------------------------#
# functions                             #
# ---------------------------------------#
def redrawGameWindow():
    gameWindow.fill(BLACK)

    pygame.draw.circle(gameWindow, BLUE, (segX[0], segY[0]), SEGMENT_R, outline)
    for i in range(len(segX)):
        segmentCLR = (GREEN)
        pygame.draw.circle(gameWindow, segmentCLR, (segX[i], segY[i]), SEGMENT_R, outline)
        pygame.draw.circle(gameWindow, RED, (foodx, foody), 10, outline)

        font = pygame.font.SysFont("Courier New", 30)
        graphics = font.render("Score: " + str(score), 1, WHITE)
        gameWindow.blit(graphics, (20, 20))
        font = pygame.font.SysFont("Courier New", 30)
        graphics = font.render("Timer: " + str(countdown), 1, WHITE)
        gameWindow.blit(graphics, (20, 60))
    pygame.display.update()


def text(fontSize, text, coords, textColour):
    smallfont = pygame.font.SysFont("Courier New", fontSize)
    script = smallfont.render(str(text), True, textColour)
    gameWindow.blit(script, coords)


def timer(elapsed, clock, begin):
    elapsed = pygame.time.get_ticks() - begin
    countdown = round((timer * 1000 - elapsed) / 1000)
    if countdown == 0:
        inPlay = False
        end = True


# ---------------------------------------#
# main program                          #
# ---------------------------------------#
print("Use the arrows and the space bar.")
print("Hit ESC to end the program.")

# snake's properties
SEGMENT_R = 10
HSTEP = 20
VSTEP = 20
stepX = 0
stepY = -VSTEP  # initially the snake moves upwards
segX = []
segY = []
for i in range(4):  # add coordinates for the head and 3 segments
    segX.append(MIDDLE)
    segY.append(BOTTOM + i * VSTEP)

# ---------------------------------------#

begin = pygame.time.get_ticks()
while inPlay == True:
    elapsed = pygame.time.get_ticks() - begin
    countdown = round((clock * 1000 - elapsed) / 1000)
    pygame.event.clear()
    redrawGameWindow()
    pygame.time.delay(speed)

    pygame.display.update

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    if keys[pygame.K_LEFT] and stepX <= 0:
        stepX = -HSTEP
        stepY = 0
    if keys[pygame.K_RIGHT] and stepX >= 0:
        stepX = HSTEP
        stepY = 0
    if keys[pygame.K_UP] and stepY >= 0:
        stepX = 0
        stepY = -VSTEP
    if keys[pygame.K_DOWN] and stepY >= 0:
        stepX = 0
        stepY = VSTEP

    # move the segments
    lastIndex = len(segX) - 1
    for i in range(lastIndex, 0, -1):  # starting from the tail, and going backwards:
        segX[i] = segX[i - 1]  # every segment takes the coordinates
        segY[i] = segY[i - 1]  # of the previous one

    # move the head
    segX[0] = segX[0] + stepX
    segY[0] = segY[0] + stepY

    # if snake hits the edge
    if segX[0] <= LEFT or segX[0] >= RIGHT or segY[0] <= TOP or segY[0] >= BOTTOM:
        end = True
        inPlay = False

    # if snake eats food
    if segX[0] == foodx and segY[0] == foody:
        foodx = round(randint(2, 38) * 20)
        foody = round(randint(2, 28) * 20)
        segX.append(segX[-1])
        segY.append(segY[-1])
        score = score + 1

    # self collision
    for i in range(1, len(segX)):
        if segX[0] == segX[i] and segY[0] == segY[i]:
            inPlay = False
            end = True

    # speed increase after certain apples
    speed = 60 - score // 5 * 5
    if score == 5:
        print(speed)

    # winning
    if score == 20:
        inPlay = False
        win = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

pygame.display.update
# ---------------------------------------#
while end == True:
    gameWindow.fill(RED)
    text(100, "YOU LOST", (160, 250), BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()

while win == True:
    gameWindow.fill(GREEN)
    text(100, "WINNER", (160, 250), BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()

pygame.quit()
