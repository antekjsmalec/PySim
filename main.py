import sys
import math
import pygame


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.Clock()
pygame.display.set_caption("PySim")
run = True
dt = 0
physics_on = False

class Button:
    def __init__(self, posX, posY, height, width, colour):
        self.posX = posX
        self.posY = posY
        self.height = height
        self.width = width
        self.colour = colour

        self.rect = pygame.Rect(posX, posY, height, width)

    def touching_mouse(self):
        if mousePositionX >= self.posX and mousePositionX <= (self.posX+self.width) and mousePositionY >= self.posY and mousePositionY <= (self.posY + self.height):
            return True

class Vector:

    def __init__(self, x = 0.0, y = 0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

class Particle:

    def __init__(self, x,y, radius=10, mass=1.0, bounce = 0.8):
        self.position = Vector(x, y)
        self.v = Vector(0,0)
        self.a = Vector(0,0)
        self.radius = radius
        self.mass = mass
        self.inv_mass = 1 / mass if mass > 0 else 0.0
        self.bounce = bounce

    def force(self, force:Vector):
        self.a += force * self.inv_mass

    def update(self, dt = float, floor = float):
        self.v += self.a * dt
        self.position += self.v * dt
        self.a = Vector(0,0)

        if self.position.x - self.radius <= 0:
            self.position.x = self.radius
            self.v.x = -self.v.x * self.bounce
        elif self.position.x + self.radius >= 1920:
            self.position.x = 1920 - self.radius
            self.v.x = -self.v.x * self.bounce
        if self.position.y - self.radius <=0:
            self.position.y = self.radius
            self.v.y = -self.v.y * self.bounce
        elif self.position.y + self.radius >= floor__height:
            self.position.y = floor__height - self.radius
            self.v.y = -self.v.y * self.bounce

mousePositionX, mousePositionY = pygame.mouse.get_pos()

g = Vector(0, 981.0)
floor__height = 1030
particle = Particle(600, 50, 10,1, 0.8)
a_force = Vector(-1000, 0)
d_force = Vector(1000, 0)
w_force = Vector(0, -670)

play_pause = Button(10, 10, 25, 25, 'red')



while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000
    screen.fill((40, 40, 40))
    mousePositionX, mousePositionY = pygame.mouse.get_pos()


    pygame.draw.rect(screen, play_pause.colour, play_pause.rect)
    if play_pause.touching_mouse() == True and pygame.mouse.get_just_released()[0] == True:
        if play_pause.colour == 'red':
            play_pause.colour = 'green'
            physics_on = True
        elif play_pause.colour == 'green':
            play_pause.colour = 'red'
            physics_on = False

    if physics_on == True:
        particle.force(g)
        particle.update(dt, floor__height)

    if keys[pygame.K_a]:
        particle.force(a_force)
    elif keys[pygame.K_d]:
        particle.force(d_force)
    elif keys[pygame.K_w]:
        particle.force(w_force)


    pygame.draw.circle(screen, 'red', (int(particle.position.x), int(particle.position.y)), particle.radius)
    pygame.draw.line(screen, 'white', (0, floor__height), (1920, floor__height), width=1)

    pygame.display.flip()

pygame.quit()