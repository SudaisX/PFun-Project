import pygame
from pygame import mixer
from random import randint
from math import sqrt, pow

#initializes pygame
pygame.init()

#screen size and background image
screen = pygame.display.set_mode((800, 600)) #creates the screen with the arguments passed as a tuple of (Width, Height)
background = background = pygame.image.load('images/zen.jpg')

#icon and title
icon = pygame.image.load('images/icon.png')
pygame.display.set_caption('depresso shooter scooter')
pygame.display.set_icon(icon)

#Background music
mixer.music.load('sounds/bg_music.mp3')
mixer.music.play(-1)

#Parent class
class Parent:
    def __init__(self, image, x, y, x_change, y_change):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

#Player
class Player(Parent):
    def __init__(self):
        Parent.__init__(self, 'images/player.png', 370, 520, 0, 0)

    def boundrycheck(self):
        if self.x < 0:
            self.x = 0
        elif self.x > 736:
            self.x = 736

#Enemy
class Enemy(Parent):
    def __init__(self, image):
        Parent.__init__(self, image, randint(64, 735), randint(50,150), 0.3, 40)

    def newX(self, score):
        if score >= 0 and score < 15:
            return 0.4
        elif score >= 15 and score < 30:
            return 0.6
        elif score >= 30 and score < 60:
            return 0.8
        elif score >= 60 and score < 90:
            return 1.2
        elif score >= 90 and score < 110:
            return 1.4

#Bullet
class Tears(Parent):
    def __init__(self):
        Parent.__init__(self, 'images/tear3.png', 0, player.y, 0, 4)
        self.state = 'ready'  #ready = you cant see, fire = tear currently moving
        self.sound = mixer.Sound('sounds/laser.wav')

    def draw(self):
        self.state = 'fire'
        screen.blit(self.image, (self.x + 16, self.y + 10)) #16 and 10 added to centralise the tear

#Score
class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.x = 10
        self.y = 10

    def show(self):
        showscore = self.font.render(f'Score: {str(self.value)}', True, (255, 255, 255))
        screen.blit(showscore, (self.x, self.y))

#Checks collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = sqrt(pow((enemyX - bulletX), 2) + pow((enemyY - bulletY), 2))
    if distance < 35:
        return True
    else:
        return False

#Player
player = Player()

#Enemies
sel = Enemy('images/sel2.jpg')
d_grade = Enemy('images/d_grade.png')
plagiarism = Enemy('images/plagiarism.png')
canvas = Enemy('images/canvas3.png')
zoom = Enemy('images/zoom.png')
hackerrank = Enemy('images/hackerrank.png')
enemy = [sel, d_grade, plagiarism, canvas, zoom, hackerrank]

#tears + score
tears = Tears()
score = Score()

#Game loop
running = True
while running:
    screen.fill((45, 48, 51)) #draw a background of color (r, g, b)
    screen.blit(background, (0,0)) #draw background image

    #Check keystrokes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  #check keystroke for Left or Right
            if event.key == pygame.K_LEFT:
                player.x_change = -1  
            if event.key == pygame.K_RIGHT:
                player.x_change = 1
            if event.key == pygame.K_SPACE:
                if tears.state == 'ready':
                    tears.x = player.x
                    tears.sound.play()
                    tears.draw()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0

    #Check student's boundries
    player.x += player.x_change
    player.boundrycheck()

    for i in range(len(enemy)):
        #enemy movement
        enemy[i].x += enemy[i].x_change
        if enemy[i].x < 0:
            enemy[i].x_change = enemy[i].newX(score.value)
            enemy[i].y += enemy[i].y_change
        elif enemy[i].x > 736:
            enemy[i].x_change = -enemy[i].newX(score.value)
            enemy[i].y += enemy[i].y_change

        #collision
        collision = isCollision(enemy[i].x, enemy[i].y, tears.x, tears.y)
        if collision == True:
            tears.y = player.y
            tears.state = 'ready'
            score.value += 1
            enemy[i].x = randint(64, 735)
            enemy[i].y = randint(50,150)

        enemy[i].draw()

    #tears movement
    if tears.y <= 0:
        tears.y = 480
        tears.state = 'ready'
 
    if tears.state == 'fire':
        tears.draw()
        tears.y -= tears.y_change

    player.draw() #draws player
    score.show()
    pygame.display.update() #updates display within the loop