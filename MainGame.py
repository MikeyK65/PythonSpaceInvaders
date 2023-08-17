import pygame
import math
import random

from pygame import mixer


pygame.init()

GAME_AREA_WIDTH = 800
GAME_AREA_HEIGHT = 800

playerScore = 0
alienAmount = 100
ufoAmount = 500

font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

gameOverFont = pygame.font.Font('freesansbold.ttf',64)
gameOverTextX = 60
gameOverTextY = 100


screen = pygame.display.set_mode((GAME_AREA_WIDTH,GAME_AREA_HEIGHT))

background = pygame.image.load("background.jpg")

mixer.music.load("background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.1)

bulletSound = mixer.Sound("laser.wav")
bulletSound.set_volume (0.2)
explosionSound = mixer.Sound("explosion.wav")
explosionSound.set_volume (0.2)

pygame.display.set_caption("Space Invader")

spaceshipIcon = pygame.image.load("spaceship.png")
pygame.display.set_icon(spaceshipIcon)

playerImage = pygame.image.load ("spaceship.png")
playerX = 0
playerY = GAME_AREA_HEIGHT - playerImage.get_height()

playerBulletImage = pygame.image.load ("bullet.png")
playerBulletX = 0
playerBulletY = 800
playerBulletXChange = 0
playerBulletYChange = 1
playerBulletState = 0   # 0 = READY, 1 = FIRE/MOVING

numberOfEnemies = 10

enemyImage = []
enemyStartX = []
enemyStartY = []
enemyX = []
enemyY = []
enemyXMovement = []
enemyYMovement = []
enemyStatus = []        # 0 = alive, 1 = dead

speedMultiplier = 5

for i in range (numberOfEnemies):
    enemyImage.append(pygame.image.load ("ufo.png"))
    enemyStartX.append(0)
    enemyStartY.append(200)
    enemyX.append(0 + (i * 30))
    enemyY.append(200)
    enemyStatus.append(0)
    enemyXMovement.append(0.1)
    enemyYMovement.append(0)

def showScore(x,y):
    score = font.render("Score : " + str(playerScore), True, (255,255,255))
    screen.blit(score, (x,y))

def player(x, y):
    screen.blit(playerImage, (x, y))

def drawEnemies():
    for i in range(numberOfEnemies):
        if enemyStatus[i] == 0:
            drawEnemy (i)

def drawEnemy(i):
    screen.blit(enemyImage[i], (enemyX[i], enemyY[i]))

def fireBullet(x,y):
    global playerBulletState 
    playerBulletState = 1
    screen.blit(playerBulletImage, (x, y))

def isCcollision (enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    
    return False


def gameoverText(x, y):
    gameOver = font.render("Game Over!  Final Score : " + str(playerScore), True, (255,255,255))
    screen.blit(gameOver, (x,y))


##################################
#
# MAIN CODE
#
##################################

running = True
xMovement = 0

playerXSpeed = 0.5
playerYSpeed = 0.5


# Main loop
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_LEFT:
                xMovement -= playerXSpeed

            if event.key == pygame.K_RIGHT:
                xMovement += playerXSpeed

            if event.key == pygame.K_SPACE:
                if playerBulletState == 0:
                    bulletSound.play()
                    playerBulletY = playerY
                    playerBulletX = playerX 
                    fireBullet(playerBulletX, playerBulletY)
            
        if event.type == pygame.KEYUP:
            xMovement = 0

    playerX += xMovement

    if playerX <= 0:
        playerX = 0
    elif playerX >= GAME_AREA_WIDTH - playerImage.get_width():
        playerX = GAME_AREA_WIDTH - playerImage.get_width()

    # enemy movement
    for i in range(numberOfEnemies):
        if enemyStatus[i] == 0:
            enemyX[i] += enemyXMovement[i]
            if enemyX[i] <= 0:
                enemyX[i] = 0
                enemyXMovement[i] = 0.1 * speedMultiplier
                enemyY[i] += enemyImage[i].get_height() * speedMultiplier
            elif enemyX[i] >= GAME_AREA_WIDTH - enemyImage[i].get_width():
                enemyX[i] = GAME_AREA_WIDTH - enemyImage[i].get_width()
                enemyXMovement[i] = -0.1 * speedMultiplier
                enemyY[i] += enemyImage[i].get_height() * speedMultiplier
    
    if playerBulletState == 1:
        screen.blit(playerBulletImage, (playerBulletX, playerBulletY))
        playerBulletY -= playerBulletYChange
        print (playerBulletX, playerBulletY, playerBulletState)

        if playerBulletY < 0:
            playerBulletState = 0
        

    
    #screen.blit(background, (0,0))

    player(playerX, playerY)
    drawEnemies()
    showScore(textX, textY)

    for i in range(numberOfEnemies):
        if enemyStatus[i] == 0:
            if isCcollision (enemyX[i], enemyY[i], playerBulletX, playerBulletY):
                playerBulletState = 0  
                playerBulletX = 0
                playerBulletY = 0          
                playerScore += alienAmount
                enemyStatus[i] = 1
                explosionSound.play()

                # reset alien
                #enemyX = enemyStartX
                #enemyY = enemyStartY
    
    pygame.display.update()
    

    # Any aliens still alive
    aliensAlive = False
    for i in range(numberOfEnemies):
        if enemyStatus[i] == 0:
            aliensAlive = True

    if aliensAlive == False:
        gameoverText(gameOverTextX, gameOverTextY)
        
        running = False

    # Have the aliens won?
    for i in range(numberOfEnemies):
        if enemyStatus[i] == 0:
            if enemyY[i] > GAME_AREA_HEIGHT - playerImage.get_height():
                gameoverText(gameOverTextX, gameOverTextY)
                #running = False
                break
