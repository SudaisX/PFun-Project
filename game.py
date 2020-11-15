import pygame
from random import randint
from math import sqrt, pow
from pygame import mixer

#initializes pygame
pygame.init()

#creates the screen with the arguments passed as a tuple of (Width, Height)
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load('images/zen.jpg')

#setting title and icon
pygame.display.set_caption("depresso shooter scooter")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

#Background sound
mixer.music.load('sounds/bg_music.mp3')
mixer.music.play(-1)

#Player
class Player:
    def __init__(self, image, x, y, changeInX):
        self.image = pygame.image.load(f'{image}')
        self.x = x
        self.y = y
        self.changeInX = changeInX

player = Player('images/player.png', 370, 520, 0)

playerImg = pygame.image.load('images/player.png')
playerX = 370
playerY = 520
playerX_change = 0

#Enemy
enemies = 6
enemyImg = [pygame.image.load('images/sel2.jpg'), pygame.image.load('images/d_grade.png'), pygame.image.load('images/plagiarism.png'), pygame.image.load('images/zoom.png'), pygame.image.load('images/hackerrank.png'), pygame.image.load('images/canvas3.png')]
#enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(enemies):
    #enemyImg.append(pygame.image.load('jessica.jpg'))
    enemyX.append(randint(64, 735))
    enemyY.append(randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('images/tear3.png')
bulletX = 0
bulletY = playerY
bulletY_change = 4
bulletState = 'ready' #ready = you cant see, fire = bullet currently moving

#score
scoreVal = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

def showscore(scoreX, scoreY):
    score = font.render(f'Score: {str(scoreVal)}', True, (255, 255, 255 ))
    screen.blit(score, (scoreX, scoreY))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def bullet(x, y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10)) #16 and 10 added to centralise the bullet

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = sqrt(pow((enemyX - bulletX), 2) + pow((enemyY - bulletY), 2))
    if distance < 35:
        return True
    else:
        return False

#GamveOver
def isOver(enemyX, enemyY, playerX, playerY):
    distance = sqrt(pow((enemyX - playerX), 2) + pow((enemyY - playerY), 2))
    if distance < 35:
        return True
    else:
        return False

fontover = pygame.font.Font('freesansbold.ttf', 64)
def gameover():
    over = fontover.render(f'GAME OVER!', True, (0, 0, 0 ))
    screen.blit(over, (200,250))

#Game loop
running = True
while running:
    #background color (r, g, b)
    screen.fill((45, 48, 51))

    #background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  #check keystroke for Left or Right
            if event.key == pygame.K_LEFT:
                playerX_change = -1  
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bulletState == 'ready':
                    bullet_sound = mixer.Sound('sounds/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Check student's boundries
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    for i in range(enemies):
        #game over
        #if enemyY[i] > 200:
        #    for j in range(enemies):
        #        enemyY[j] = 2000
        #    gameover()
        #    break

        #enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == True:
            #explosion_sound = mixer.Sound('explosion.wav')
            #explosion_sound.play()
            bulletY = playerY
            bulletState = 'ready'
            scoreVal += 1
            print(scoreVal)
            enemyX[i] = randint(64, 735)
            enemyY[i] = randint(50,150)


        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = 'ready'
 
    if bulletState == 'fire':
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY) #draws player
    showscore(scoreX, scoreY)
    pygame.display.update() #updates display within the loop