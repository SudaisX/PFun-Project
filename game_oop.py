import pygame
from random import randint
from math import sqrt, pow


pygame.init() #initializes pygame
screen = pygame.display.set_mode((800, 600)) #creates the screen with the arguments passed as a tuple of (Width, Height)
background = pygame.image.load('classroom.jpg')

#setting title and icon
pygame.display.set_caption("depresso shooter scooter")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

class Player:
    def __init__(self, image, x, y, changeX):
        self.image = pygame.image.load(f'{image}')
        self.x = x
        self.y = y
        self.changeX = changeX

    def drawPlayer(self, x, y):
        screen.blit(self.image, (self.x, self.y))


class Enemy():
    def __init__(self, image):
        self.image = pygame.image.load(f'{image}')
        self.x = randint(64, 735)
        self.y = randint(50,150)
        self.changeX = 0.3
        self.changeY = 40

    def drawEnemy(self, x, y):
        screen.blit(self.image, (self.x, self.y))


class Bullet():
    def __init__(self, y, state):
        self.image = pygame.image.load('tear3.png')
        self.x = 0
        self.y = y
        self.changeY = 4
        self.state = state #ready = you cant see, fire = bullet currently moving

    def drawBullet(self):
        global bulletState
        self.state = 'fire'
        screen.blit(self.image, (self.x + 16, self.y + 10)) #16 and 10 added to centralise the bullet

player = Player('player.png', 370, 520, 0)
enemies = [Enemy('book.png'), Enemy('assignment.png'), Enemy('brain.png'), Enemy('list.png'), Enemy('monster1.png'), Enemy('monster2.png') ]
bullet = Bullet(player.y, 'ready')

#score
scoreVal = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

def showscore(scoreX, scoreY):
    score = font.render(f'Score: {str(scoreVal)}', True, (0, 0, 0 ))
    screen.blit(score, (scoreX, scoreY))

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
                player.changeX = -1
            if event.key == pygame.K_RIGHT:
                player.changeX = 1
            if event.key == pygame.K_SPACE:
                if bullet.state == 'ready':
                    bullet.x = player.x
                    bullet.drawBullet()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.changeX = 0

    #Check student's boundries

    player.x += player.changeX
    if player.x < 0:
        player.x = 0
    elif player.x > 736:
        player.x = 736

    for enemy in enemies:

        #enemy movement
        enemy.x += enemy.changeX
        if enemy.x < 0:
            enemy.changeX = 0.5
            enemy.y += enemy.changeX
        elif enemy.x > 736:
            enemy.changeX = -0.5
            enemy.y += enemy.changeY

        #collision
        collision = isCollision(enemy.x, enemy.y, bullet.x, bullet.y)
        if collision == True:
            bullet.y = player.y
            bullet.state = 'ready'
            scoreVal += 1
            print(scoreVal)
            enemy.x = randint(64, 735)
            enemy.y = randint(50,150)
        enemy.drawEnemy(enemy.x, enemy.y)

    #bullet movement
    if bullet.y <= 0:
        bullet.y = 480
        bullet.state = 'ready'
 
    if bullet.state == 'fire':
        bullet.drawBullet()
        bullet.y -+ bullet.changeY

    player.drawPlayer(player.x, player.y) #draws player
    showscore(scoreX, scoreY)
    pygame.display.update() #updates display within the loop