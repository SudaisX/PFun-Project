import pygame
from random import randint
from math import sqrt, pow

#initializes pygame
pygame.init()

#creates the screen with the arguments passed as a tuple of (Width, Height)
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load('classroom.jpg')

#setting title and icon
pygame.display.set_caption("depresso shooter scooter")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Player
class Player:
    def __init__(self, image, x, y, x_change):
        self.image = pygame.image.load(f'{image}')
        self.x = x
        self.y = y
        self.x_change = x_change

player = Player('player.png', 370, 520, 0)

#Enemy
class EnemyL
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.x = randint(64, 735)
        self.y = randint(50,150)
        self.x_change = 0
        self.y_change = 40

enemies = 6
enemyImg = [pygame.image.load('book.png'), pygame.image.load('assignment.png'), pygame.image.load('brain.png'), pygame.image.load('list.png'), pygame.image.load('monster1.png'), pygame.image.load('monster2.png')]
#enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(enemies):
    #enemyImg.append(pygame.image.load('book.png'))
    enemyX.append(randint(64, 735))
    enemyY.append(randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('tear3.png')
bulletX = 0
bulletY = player.y
bulletY_change = 4
bulletState = 'ready' #ready = you cant see, fire = bullet currently moving

#score
scoreVal = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

def showscore(scoreX, scoreY):
    score = font.render(f'Score: {str(scoreVal)}', True, (0, 0, 0 ))
    screen.blit(score, (scoreX, scoreY))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def drawplayer(x, y):
    screen.blit(player.image, (x, y))

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
                player.x_change = -1  
            if event.key == pygame.K_RIGHT:
                player.x_change = 1
            if event.key == pygame.K_SPACE:
                if bulletState == 'ready':
                    bulletX = player.x
                    bullet(bulletX, bulletY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0

    #Check student's boundries
    player.x += player.x_change
    if player.x < 0:
        player.x = 0
    elif player.x > 736:
        player.x = 736

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
            bulletY = player.y
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

    drawplayer(player.x, player.y) #draws player
    showscore(scoreX, scoreY)
    pygame.display.update() #updates display within the loop