try: 
    from pyfirmata import ArduinoNano, util, STRING_DATA
except:
    import pip
    pip.main(['install', 'pyfirmata'])
    from pyfirmata import ArduinoNano, util, STRING_DATA

import pygame
import random
import math
import sys
from time import sleep

pygame.init()  # SHOULD ALWAYS BE IN YOUR CODE

port = 'COM3' #change to whatever this is - connect to computer and check through Arduino IDE
board = ArduinoNano(port)
pin_9 = board.get_pin('d:9:o')
pin_10 = board.get_pin('d:10:o')

iterator = util.Iterator(board)
iterator.start()

# creates screen with pixel size
screen = pygame.display.set_mode((800, 600))

#backrground
background = icon = pygame.image.load('background.jpg')
# Title and Icons:
pygame.display.set_caption("Danny's First Game! - Pygame tutorial")

# Spaceship icon
icon = pygame.image.load('window_icon.png')  # imports image
pygame.display.set_icon(icon)

# user / character
playerImg = pygame.image.load('soldier.png')   # imports image
playerX = 370  # starting pos
playerY = 480
playerX_change = 0
playerY_change = 0
playerSpeed = .5
# enemy
enemyImg = pygame.image.load('enemy_1.png')   # imports image
enemyX = random.randint(0, 736)  # starting pos
enemyY = random.randint(50, 150)
enemyY_change = 0.2

# bullet
bulletImg = pygame.image.load('bullet.png')   # imports image
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.8
bullet_state = "ready"

# score variable:
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 550


# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# FUNCTIONS:
# player location


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means to draw
# enemy location


def enemy(x, y):
    screen.blit(enemyImg, (x, y))  # blit means to draw
# fire bullet


def fire_bullet(x, y):
    global bullet_state  # makes varriable able to be accsessed at any time
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
# bullet collition


def bulletCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))  # distance formula
    if distance < 27:
        return True
    else:
        return False
# enemy collision


def isEnemyCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))  # distance formula
    if distance < 60:
        return True
    else:
        return False
# Score


def show_score(x, y):
    # remeber to convert to string   (typecasting)
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter('Score:' + str(score)))
# game over


def game_over_text():

    while true:
        board.pin_9.write(1)
        board.pin_10.write(0)
    #check which of these methods work
        board.digital[pin_9].write(1)
        board.digital[pin_9].write(0)

        sleep(5)
        break
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter('You lost'))
    
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# GAME LOOP:
while True:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # makes the window stay open until the x has been pressed.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# if keystroke is pressed check whether its wasd
        if event.type == pygame.KEYDOWN:
            # WASD ---->   UP, DOWN, Left, right
            if event.key == pygame.K_w:
                playerY_change = -1 * playerSpeed
            if event.key == pygame.K_a:
                playerX_change = -1 * playerSpeed
            if event.key == pygame.K_s:
                playerY_change = playerSpeed
            if event.key == pygame.K_d:
                playerX_change = playerSpeed
            # space: check if the bullet is ready, if so shoot it
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":  # so you can only fire another bullet when it is "ready"
                    bulletX = playerX
                    bulletY = playerY    # this makes the bullet start moving form the pos of the user
                    fire_bullet(bulletX, bulletY)
            # the following code stops the action when you stop pressing the key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                playerX_change = 0
                playerY_change = 0
    playerX += playerX_change
    playerY += playerY_change

    # enemy movement (only down)
    enemyY += enemyY_change
    if score_value > 5:
        enemyY_change = .3
        playerSpeed = .6
    elif score_value > 10:
        enemyY_change = .5
        playerSpeed = 1
    elif score_value > 15:
        enemyY_change = .6
        playerSpeed = 1.2
    elif score_value > 20:
        enemyY_change = .8
        playerSpeed = 1.6

# checking for boundaries:
    if playerX < 0:
        # these 4 lines make it so the player cannot go off screen.
        playerX = 0
    elif playerX >= 736:
        # 736 because the player is a 64 bit image (coordinates messure the bottom left corner of the picture)
        playerX = 736
    elif playerY > 560:
        playerY = 560
    elif playerY < 300:
        playerY = 300
    # Collision
    collision = bulletCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        # once bullet collistion is true based on the function, it resets the enemy to a rnd pos
        enemyX = random.randint(0, 736)  # starting pos
        enemyY = random.randint(50, 150)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        # if bullet state is fire it will reload the bullet
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # GAME OVER TEXT
    if enemyY > 550:
        enemyY = 2000
        game_over_text()

    enemyCollision = isEnemyCollision(enemyX, enemyY, playerX, playerY)
    if enemyCollision:
        enemyY = 2000
        game_over_text()

    # PLAYER FUNCTION goes here because it must be on screen at all times (remember loop)
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, textY)
    # everyhting must be before the background so it appears above it
    pygame.display.update()