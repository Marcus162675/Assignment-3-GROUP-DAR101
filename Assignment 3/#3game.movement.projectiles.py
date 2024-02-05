#projectiles
import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('game for assignemnt 3')

# Load initial background image
bg = pygame.image.load(os.path.join('images','bg3.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,17)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1,8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images','0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    throwing = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(27, 36)]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False
        self.health = 250  # Add health attribute and initialize it to 3
        self.is_throwing = False
        self.throwCount = 0  # Initialize throw animation count
    
    def reset_health(self):
        self.health = 250  # Reset health to its initial value

    def draw(self, win):
        if self.falling:
            win.blit(self.fall,(self.x, self.y + 30))
        elif self.jumping:
            if self.jumpCount < len(self.jumpList):  # Check if jumpCount is within the range of jumpList
                self.y -= self.jumpList[self.jumpCount] * 1.2
                win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
                self.hitbox = (self.x+4,self.y,self.width-24,self.height-10)  # Move hitbox update here
                self.jumpCount += 1
            else:
                self.jumpCount = 0  # Reset jumpCount
                self.jumping = False
                self.runCount = 0
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x,self.y+3,self.width-25,self.height-35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x+4,self.y, self.width-24,self.height-10)
            win.blit(self.slide[self.slideCount//10], (self.x,self.y))
            self.slideCount += 1
        elif self.is_throwing:  # Update variable name here
            if self.throwCount + 1 >= 27:
                self.is_throwing = False  # Update variable name here
                self.throwCount = 0
            win.blit(self.throwing[self.throwCount // 3], (self.x, self.y))  # Use self.throw instead of self.throwing
            self.throwCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x,self.y,self.width-10,self.height)
        
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def reduce_health(self):
        self.health -= 1

    def is_alive(self):
        return self.health > 0

class zombie:
    rotate = [pygame.image.load(os.path.join('images', 'Idle (1).PNG')),pygame.image.load(os.path.join('images', 'Idle (2).PNG')),pygame.image.load(os.path.join('images', 'Idle (3).PNG')),pygame.image.load(os.path.join('images', 'Idle (4).PNG')),pygame.image.load(os.path.join('images', 'Idle (5).PNG')),pygame.image.load(os.path.join('images', 'Idle (6).PNG')),pygame.image.load(os.path.join('images', 'Idle (7).PNG')),pygame.image.load(os.path.join('images', 'Idle (8).PNG')),pygame.image.load(os.path.join('images', 'Idle (9).PNG')),pygame.image.load(os.path.join('images', 'Idle (10).PNG')),pygame.image.load(os.path.join('images', 'Idle (11).PNG')),pygame.image.load(os.path.join('images', 'Idle (12).PNG')),pygame.image.load(os.path.join('images', 'Idle (13).PNG')),pygame.image.load(os.path.join('images', 'Idle (14).PNG')),pygame.image.load(os.path.join('images', 'Idle (15).PNG'))]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self,win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 24:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y))
        self.rotateCount += 1
    
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
        
class saw(object):
    rotate = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),pygame.image.load(os.path.join('images', 'SAW1.PNG')),pygame.image.load(os.path.join('images', 'SAW2.PNG')),pygame.image.load(os.path.join('images', 'SAW3.PNG'))]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4
        self.health = 2  # Initialize zombie health
       
    
    def draw(self,win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y))
        self.rotateCount += 1
    
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
    
    def reduce_health(self):
        # Reduce zombie's health when hit by a kunai
        self.health -= 1
        self.collisions += 1
    
    def is_alive(self):
        # Check if the zombie is alive
        return self.health > 0
    
    def should_remove(self):
        # Check if the zombie should be removed from the game
        return self.collisions >= 2

class spike(saw):
    img = pygame.image.load(os.path.join('images', 'spike.png'))
    def draw(self,win):
        self.hitbox = (self.x + 10, self.y, 28,315)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False
    
class Crystal(object):
    img = pygame.image.load(os.path.join('images', 'Violet_crystal3.png'))
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collected = False

    def draw(self, win):
        if not self.collected:
            win.blit(self.img, (self.x, self.y))

    def collect(self, runner):
        if not self.collected and self.collision(runner):
            self.collected = True
            return True
        return False

    def collision(self, runner):
        return (self.x < runner.x + runner.width and
                self.x + self.width > runner.x and
                self.y < runner.y + runner.height and
                self.y + self.height > runner.y)

class Projectile1(object):
    img = pygame.image.load(os.path.join('images', 'kunai.png'))

    def __init__(self, x, y, width, height, facing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = facing  # Direction of the projectile (left or right)
        self.vel = 2 * facing  # Velocity (speed and direction) of the projectile

    def draw(self, win):
        self.x += self.vel  # Update the x-coordinate based on velocity and direction
        win.blit(self.img, (self.x, self.y))
    
    def collide(self, obj):
        
        projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        return projectile_rect.colliderect(obj_rect)

def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    runner.draw(win)
    for obstacle in objects:
        obstacle.draw(win)
    
    for crystals in collectibles:  # Draw each crystal in the collectibles list
        crystals.draw(win)
    
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Score: ' + str(score), 1, (255,255,255))
    win.blit(text, (600, 20))
    
    # Display health
    health_text = font.render('Health: ' + str(runner.health), 1, (255, 255, 255))
    win.blit(health_text, (10, 20))
    
    for Projectile in kunai:
        Projectile.draw(win)
    
    pygame.display.update()

def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score
               
    return last

def endscreen():
    global pause, objects, speed, score
    pause = 0 
    objects = []
    speed = 60
        
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        smallfont = pygame.font.SysFont('comicsans', 30)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        smallfont.render('Press Mousebutton to continue', 1, (200, 200, 200))
        pygame.display.update()
    score = 0
    runner.falling = False
    runner.reset_health() # Reset player's health
    runner.x = original_x  # Reset player's x position
    runner.y = original_y  # Reset player's y position
    
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, random.randrange(2000, 3000)) # Will trigger every 2 - 3 seconds)
pygame.time.set_timer(USEREVENT+3, random.randrange(5000, 5500))
original_x = 200
original_y = 313
runner = player(200, 313, 64, 64)
run = True
speed = 60 # NEW
pause = 0
fallspeed = 0 
objects = []
collectibles = []
score = 0
kunai = []

while run:    
    if pause > 0:
        pause += 1
        if pause > fallspeed * 2:
            endscreen()

    for objectt in objects:
        if objectt.collide(runner.hitbox):
            runner.reduce_health()  # Reduce player health

            if runner.health <= 0:  # Check if player health reaches 0
                runner.falling = True  # Set player falling when health reaches 0
                if pause == 0:
                    fallspeed = speed
                    pause = 1
        
        objectt.x -= 1.4
        if objectt.x + objectt.width < 0:
            objects.pop(objects.index(objectt))
        
    for crystals in collectibles[:]:  
        crystals.x -= 1.4
        if crystals.x + crystals.width < 0:
            collectibles.pop(collectibles.index(crystals))
        
        if crystals.collect(runner):
            score += 10  # Increase the score when a crystal is collected
            collectibles.remove(crystals)
                   
    if runner.health <= 0:  # Check if player health reaches 0
        runner.falling = True  # Set player falling when health reaches 0

    for crystals in collectibles[:]:  # Iterate over a copy of the list to avoid modifying it while iterating
        if crystals.collect(runner):
            score += 10  # Increase the score when a crystal is collected
            collectibles.remove(crystals)  # Remove the collected crystal from the list
    for projectile in kunai[:]:
        projectile.x += projectile.vel
        if projectile.x + projectile.width < W and projectile.x > 0:
            for zombie_obj in objects[:]:
                if isinstance(zombie_obj, zombie) and projectile.collide(zombie_obj):  # Check if the collided object is a zombie
                    objects.remove(zombie_obj)
                    kunai.remove(projectile)
                    score += 10
                    break
        else:
            kunai.remove(projectile)

  
    bgX -= 1.4  
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:  
        bgX = bg.get_width()
    
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            run = False    
            pygame.quit() 
            quit()
    
        if event.type == USEREVENT+1: # Checks if timer goes off
            speed += 1 # Increases speed
        if event.type == USEREVENT+2:
            r = random.randrange(0,3)
            if r == 0:
                zombie_object = zombie(810,310,64,64)
                objects.append(zombie_object)
            elif r == 1:
                saw_object = saw(810,310,64,64)
                objects.append(saw_object)          
            else:
                spike_object = spike(810,0,48,320)
                objects.append(spike_object)

        
        if event.type == USEREVENT + 3:  # Add a new event type for creating crystals
                    crystal_y = random.randint(150, 313)
        # Generate x-coordinate within the visible area of the window
                    crystal_x = 800
                    new_crystal = Crystal(crystal_x, crystal_y, 32, 32)
                    collectibles.append(new_crystal)        
                            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not runner.jumping:
            runner.jumping = True
    elif keys[pygame.K_DOWN]:
        if not runner.sliding:
            runner.sliding = True
    if keys[pygame.K_z]:
        if not runner.is_throwing:  # Check if player is not already throwing
            runner.is_throwing = True
            facing = 1 if runner.runCount > 0 else 1  # Set facing direction for projectile based on player direction
            kunai.append(Projectile1(round(runner.x + runner.width // 2),
                                round(runner.y + runner.height // 2),
                                64, 64, facing))

    if keys[pygame.K_LEFT]:
        if runner.x > 0:  # Check if the character is within the left boundary
            runner.x -= 2  # Move the player to the left

    if keys[pygame.K_RIGHT]:
        if runner.x < W - runner.width:  # Check if the character is within the right boundary
            runner.x += 2  # Move the player to the right
    
    
    clock.tick(speed)
    redrawWindow()
