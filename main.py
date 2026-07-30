import sys
import math
import pygame


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.Clock()
run = True
dt = 0
mousePositionX, mousePositionY = pygame.mouse.get_pos()
physicsOn = False
g = 0.981

class Button:
    def __init__(self, posX, posY, height, width, colour):
        self.posX = posX
        self.posY = posY
        self.height = height
        self.width = width
        self.colour = colour

        self.rect = pygame.Rect(posX, posY, height, width)

    def touchingMouse(self):
        if mousePositionX >= self.posX and mousePositionX <= (self.posX+self.width) and mousePositionY >= self.posY and mousePositionY <= (self.posY + self.height):
            return True


playPause = Button(10, 10, 25, 25, 'red')

class Block:
    def __init__(self, posX, posY, height, width, startAngle):
        self.posX = posX
        self.posY = posY
        self.height = height
        self.width = width
        self.r = math.sqrt(pow(width, 2) + pow(height, 2)) / 2
        self.v = 0
        self.freeFall = True

        self.angle = startAngle

        self.baseAngA = math.radians(315)
        self.baseAngB = math.radians(45)
        self.baseAngC = math.radians(225)
        self.baseAngD = math.radians(135)

    def update_points(self):
        radAngle = math.radians(self.angle)
        
        angA = self.baseAngA + radAngle
        angB = self.baseAngB + radAngle
        angC = self.baseAngC + radAngle
        angD = self.baseAngD + radAngle

        self.pointA = (self.posX + self.r * math.cos(angA), self.posY + self.r * math.sin(angA))
        self.pointB = (self.posX + self.r * math.cos(angB), self.posY + self.r * math.sin(angB))
        self.pointC = (self.posX + self.r * math.cos(angC), self.posY + self.r * math.sin(angC))
        self.pointD = (self.posX + self.r * math.cos(angD), self.posY + self.r * math.sin(angD))

    def update_gravity(self):
        self.v = self.v + g
        self.posY =+ self.v


    def rotate(self, degreesDelta):
        self.angle += degreesDelta
        self.update_points()

    def draw(self):
        points = [self.pointA, self.pointB, self.pointD, self.pointC, self.pointA, self.pointD]
        pygame.draw.aalines(screen, 'white', False, points, 2)

size = 75
square = Block(250, 250, size, size, 0)
floor = Block(200, 950, 150, 150, 0)

rotationSpeed = 90

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((40, 40, 40))
    mousePositionX, mousePositionY = pygame.mouse.get_pos()


    pygame.draw.rect(screen, playPause.colour, playPause.rect)
    if playPause.touchingMouse() == True and pygame.mouse.get_just_released()[0] == True:
        if playPause.colour == 'red':
            playPause.colour = 'green'
            physicsOn = True
        elif playPause.colour == 'green':
            playPause.colour = 'red'
            physicsOn = False

    square.update_points()
    square.draw()
    square.rotate(rotationSpeed*dt)

    floor.update_points()
    floor.draw()
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()