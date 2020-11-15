import pygame
from pygame import mixer
from random import randint
from math import sqrt, pow

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
    def __init__(self):
        self.image = pygame.image.load('images/player.png')
        self.x = 370
        self.y = 520
        self.x_change = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

#Enemy
class Enemy:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.x = randint(64, 735)
        self.y = randint(50,150)
        self.x_change = 0.3
        self.y_change = 40

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


#Bullet
class Bullet:
    def __init__(self):
        self.image = pygame.image.load('images/tear3.png')
        self.x = 0
        self.y = player.y
        self.y_change = 4
        self.state = 'ready'  #ready = you cant see, fire = tear currently moving
        self.sound = mixer.Sound('sounds/laser.wav')

    def draw(self):
        self.state = 'fire'
        screen.blit(self.image, (self.x + 16, self.y + 10)) #16 and 10 added to centralise the tear

    def sound(self):
        self.sound = mixer.Sound('sounds/laser.wav')
        return bullet_sound.play()

#score
class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.x = 10
        self.y = 10

    def show(self):
        showscore = self.font.render(f'Score: {str(self.value)}', True, (0, 0, 0 ))
        screen.blit(showscore, (self.x, self.y))


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


player = Player()
enemy = [Enemy('images/sel2.jpg'), Enemy('images/d_grade.png'), Enemy('images/plagiarism.png'), Enemy('images/canvas3.png'), Enemy('images/zoom.png'), Enemy('images/hackerrank.png')]
tear = Bullet()
score = Score()

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
                if tear.state == 'ready':
                    tear.x = player.x
                    tear.sound.play()
                    tear.draw()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0

    #Check student's boundries
    player.x += player.x_change
    if player.x < 0:
        player.x = 0
    elif player.x > 736:
        player.x = 736

    for i in range(len(enemy)):
        #enemy movement
        enemy[i].x += enemy[i].x_change
        if enemy[i].x < 0:
            enemy[i].x_change = 0.5
            enemy[i].y += enemy[i].y_change
        elif enemy[i].x > 736:
            enemy[i].x_change = -0.5
            enemy[i].y += enemy[i].y_change

        #collision
        collision = isCollision(enemy[i].x, enemy[i].y, tear.x, tear.y)
        if collision == True:
            tear.y = player.y
            tear.state = 'ready'
            score.value += 1
            print(score.value)
            enemy[i].x = randint(64, 735)
            enemy[i].y = randint(50,150)

        enemy[i].draw()

    #bullet movement
    if tear.y <= 0:
        tear.y = 480
        tear.state = 'ready'
 
    if tear.state == 'fire':
        tear.draw()
        tear.y -= tear.y_change

    player.draw() #draws player
    score.show()
    pygame.display.update() #updates display within the loop