import pygame
import math
import pyautogui
import collisiondetector as cd

pygame.init()

clock = pygame.time.Clock()
delta_time = 0
keystates = {'w': False, 's': False, 'a': False, 'd': False}
WINX, WINY = pyautogui.size()


def draw_Corners(corners):
    for i, corner in enumerate(corners):
        pygame.draw.circle(window, (i * 63, i * 63, i * 63), corner, 5)

def sin_a_plus_b(a, b):
    return math.sin(a) * math.cos(b) + math.cos(a) * math.sin(b)

def cos_a_plus_b(a, b):
    return math.cos(a) * math.cos(b) - math.sin(a) * math.sin(b)


class Car:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.width = 50
        self.height = 30
        self.theta = 0
        self.speed = 0
        self.accelerate_rate = 0.001
        self.speed_limit = 0.5
        self.speed = 0
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        self.head = pygame.Surface((10, 30))
        self.omega = 0
        self.image.fill((255, 0, 0))
        self.head.fill((0, 0, 255))
        
    def getCorners(self):
        hypotenuse = (math.sqrt(self.width**2 + self.height**2) / 2) * 0.95
        sin_theta = math.sin(self.theta)
        cos_theta = math.cos(self.theta)
        sin_alpha = self.height / (2 * hypotenuse)
        cos_alpha = self.width / (2 * hypotenuse)
        corners = [
            (self.x + (cos_alpha * cos_theta - sin_alpha * sin_theta) * hypotenuse, self.y - (sin_alpha * cos_theta + cos_alpha * sin_theta) * hypotenuse), #A=((cosa cos(angle)-sina sin(angle)) R,(sina cos(angle)+cosa sin(angle)) R)
            (self.x + (cos_theta * cos_alpha + sin_theta * sin_alpha) * hypotenuse, self.y - (sin_theta * cos_alpha - cos_theta * sin_alpha) * hypotenuse), #B=((cos(angle) cosa+sin(angle) sina) R,(sin(angle) cosa-cos(angle) sina) R)
            (self.x - (cos_theta * cos_alpha - sin_theta * sin_alpha) * hypotenuse, self.y + (sin_theta * cos_alpha + sin_alpha * cos_theta) * hypotenuse), #C=(-(cos(angle) cosa-sin(angle) sina) R,-(sin(angle) cosa+sina cos(angle)) R)
            (self.x - (cos_theta * cos_alpha + sin_theta * sin_alpha) * hypotenuse, self.y + (sin_theta * cos_alpha - sin_alpha * cos_theta) * hypotenuse)  #D=(-(cos(angle) cosa+sin(angle) sina) R,-(sin(angle) cosa-sina cos(angle)) R)
        ]
        return corners

    def draw(self, surface):
        self.image.blit(self.head, (40, 0))
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.theta))
        rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, rect)

    def accelerate(self, delta_time, direction):
        self.speed += self.accelerate_rate * delta_time * direction
        if self.speed > self.speed_limit:
            self.speed = self.speed_limit
        if self.speed < 0:
            self.speed = 0
    
    def run(self, delta_time):
        self.x += self.speed * math.cos(self.theta) * delta_time
        self.y -= self.speed * math.sin(self.theta) * delta_time

    def turn(self, delta_time, direction):
        self.omega = 0.005 * direction * (self.speed / self.speed_limit)
        self.theta += self.omega * delta_time
        if self.theta > 2 * math.pi:
            self.theta -= 2 * math.pi


class Obstacle:
    def __init__(self, x, y, width, height, id=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((200, 0, 100))

    def getCorners(self):
        return [
            (self.x - self.width / 2, self.y - self.height / 2),
            (self.x + self.width / 2, self.y - self.height / 2),
            (self.x + self.width / 2, self.y + self.height / 2),
            (self.x - self.width / 2, self.y + self.height / 2)
        ]
    
    def draw(self, surface):
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect)
    
    

car = Car()
obstacles = [Obstacle(300, 300, 100, 50, 0), Obstacle(500, 200, 50, 100, 1), Obstacle(400, 500, 150, 30, 2)]

def update():
    window.fill((50, 50, 50))
    if keystates['w']:
        car.accelerate(delta_time, 1)
    if keystates['s']:
        car.accelerate(delta_time, -1)
    if keystates['a']:
        car.turn(delta_time, 1)
    if keystates['d']:
        car.turn(delta_time, -1)
    car.run(delta_time)
    car.draw(window)
    for obstacle in obstacles:
        obstacle.draw(window)
        draw_Corners(car.getCorners())
        draw_Corners(obstacle.getCorners())
        if cd.isColided(car.getCorners(), obstacle.getCorners()):
            if cd.isColided(obstacle.getCorners(), car.getCorners()):
                print("Collided with obstacle", obstacle.id)
                pass
    pygame.display.flip()




window = pygame.display.set_mode((WINX, WINY - 500))
window.fill((50, 50, 50))
pygame.display.set_caption("My Game")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keystates['w'] = True
                #print("W key pressed")
            if event.key == pygame.K_s:
                keystates['s'] = True
                #print("s key pressed")
            if event.key == pygame.K_a:
                keystates['a'] = True
                #print("a key pressed")
            if event.key == pygame.K_d:
                keystates['d'] = True
                #print("d key pressed")
            if event.key == pygame.K_r:
                car.x = 100
                car.y = 100
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keystates['w'] = False
                #print("w key released")
            if event.key == pygame.K_s:
                keystates['s'] = False
                #print("s key released")
            if event.key == pygame.K_a:
                keystates['a'] = False
                #print("a key released")
            if event.key == pygame.K_d:
                keystates['d'] = False
                #print("d key released")
    
    update()

    

    delta_time = clock.tick(60)

pygame.quit()