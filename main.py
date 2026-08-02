import sys
import math
import pygame
import random

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

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)
        return Vector(self.x / mag, self.y / mag)

class Particle:

    def __init__(self, x,y, radius=10, mass=1.0, bounce = 0.8, colour='red'):
        self.position = Vector(x, y)
        self.v = Vector(0,0)
        self.a = Vector(0,0)
        self.radius = radius
        self.mass = mass
        self.inv_mass = 1 / mass if mass > 0 else 0.0
        self.bounce = bounce
        self.colour = colour
        self.touching_floor = False
    def force(self, force:Vector):
        self.a += force * self.inv_mass

    def update(self, dt = float, floor = float):

        self.v += self.a * dt
        self.position += self.v * dt
        self.a = Vector(0, 0)

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
            self.touching_floor = True
        elif self.position.y + self.radius < floor__height:
            self.touching_floor = False
        

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            self.colour,
            (int(self.position.x), int(self.position.y)),
            int(self.radius)
        )

def collision(a:Particle, b:Particle):
    delta  =  b.position - a.position
    s = delta.magnitude()
    min_s = a.radius + b.radius

    if s >= min_s:
        return
    dir = delta.normalize()
    pen  = min_s - s

    W = a.inv_mass + b.inv_mass
    if W == 0:
        return
    
    r_v = b.v - a.v
    v_d = r_v.dot(dir)

    if v_d > 0:
        return

    j = 0
    e = a.bounce * b.bounce
    e2 = min(a.bounce, b.bounce)

    # you can swap e and e2 for different "bounciness" calculations

    eff_e = e if abs(v_d) > 1.0 else 0.0
    j = -(1+eff_e) * v_d
    j /= W
    J = dir * j
    a.v -= J * a.inv_mass
    b.v += J * b.inv_mass

    
    corr = dir * (pen/W) 
    a.position -= corr * a.inv_mass
    b.position += corr * b.inv_mass
    
mousePositionX, mousePositionY = pygame.mouse.get_pos()

g = Vector(0, 981.0)
circles = []
all_bounce = 0.8
print(all_bounce)
floor__height = 1030

play_pause = Button(10, 10, 25, 25, 'red')

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and all_bounce < 1.0:
                all_bounce += 0.1
                print(all_bounce)
            elif event.key == pygame.K_DOWN and all_bounce > 0:
                all_bounce -= 0.1
                print(all_bounce)
            elif event.key  == pygame.K_SPACE:
                if play_pause.colour == 'red':
                    play_pause.colour = 'green'
                    physics_on = True
                elif play_pause.colour == 'green':
                    play_pause.colour = 'red'
                    physics_on = False
            elif event.key == pygame.K_r:
                play_pause.colour = 'red'
                physics_on = False
                circles.clear()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            mx, my = pygame.mouse.get_pos()
            r = random.randint(15, 35)
            colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            circles.append(Particle(mx, my, r, r * 0.5, colour = colour))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mx, my = pygame.mouse.get_pos()
                    r = 60
                    colour = 'black'
                    circles.append(Particle(mx, my, r, 3000, colour = colour))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    r = 35
                    colour = 'red'
                    circles.append(Particle(mx, my, r, 5 , colour = colour))


    keys = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000
    screen.fill((40, 40, 40))
    mousePositionX, mousePositionY = pygame.mouse.get_pos()


    pygame.draw.rect(screen, play_pause.colour, play_pause.rect)

    if physics_on == True:
        for c in circles:
            c.bounce = all_bounce
            c.force(g * c.mass)
            c.update(dt)
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                collision(circles[i], circles[j])

    for c in circles:
        c.draw(screen)

    if (play_pause.touching_mouse() == True and pygame.mouse.get_just_released()[0] == True) or ():
            if play_pause.colour == 'red':
                play_pause.colour = 'green'
                physics_on = True
            elif play_pause.colour == 'green':
                play_pause.colour = 'red'
                physics_on = False

    pygame.draw.line(screen, 'white', (0, floor__height), (1920, floor__height), width=1)

    pygame.display.flip()

pygame.quit()