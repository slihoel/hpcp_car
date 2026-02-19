import pygame
import math
import pyautogui
import collisiondetector as cd
import Car

pygame.init()
WINX, WINY = pyautogui.size()
window = pygame.display.set_mode((WINX, WINY))
window.fill((50, 50, 50))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
delta_time = 0
keystates = {'w': False, 's': False, 'a': False, 'd': False}


def draw_Corners(corners):
    for i, corner in enumerate(corners):
        pygame.draw.circle(window, (i * 63, i * 63, i * 63), corner, 5)

def sin_a_plus_b(a, b):
    return math.sin(a) * math.cos(b) + math.cos(a) * math.sin(b)

def cos_a_plus_b(a, b):
    return math.cos(a) * math.cos(b) - math.sin(a) * math.sin(b)




class Obstacle:
    def __init__(self, x, y, width, height, path, id=0, angle=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id
        self.theta = angle
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path).convert_alpha(), (width, height)), math.degrees(self.theta))
        self.isColliding = False
        

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
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect)
        

car = Car.Car()

obstacles = [
    Obstacle(250, 0, 50, 50, "assets/white_wall.png", 0), 
    Obstacle(250, 50, 50, 50, "assets/red_wall.png", 1),
    Obstacle(250, 100, 50, 50, "assets/white_wall.png", 2),
    Obstacle(250, 150, 50, 50, "assets/red_wall.png", 3),
    Obstacle(250, 200, 50, 50, "assets/white_wall.png", 4),
    Obstacle(250, 250, 50, 50, "assets/red_wall.png", 5),
    Obstacle(250, 300, 50, 50, "assets/white_wall.png", 6),
    Obstacle(250, 350, 50, 50, "assets/red_wall.png", 7),
    Obstacle(250, 400, 50, 50, "assets/white_wall.png", 8),
    Obstacle(254.8, 430.9, 50, 50, "assets/red_wall.png", 10, 0.31),
    Obstacle(269.1, 458.8, 50, 50, "assets/white_wall.png", 11, 0.63),
    Obstacle(291.2, 481.0, 50, 50, "assets/red_wall.png", 12, 0.94),
    Obstacle(319.1, 495.1, 50, 50, "assets/white_wall.png", 13, 1.26),
    Obstacle(350.0, 500.0, 50, 50, "assets/red_wall.png", 14, 1.57),
    Obstacle(400, 500, 50, 50, "assets/white_wall.png", 15),
    Obstacle(450, 500, 50, 50, "assets/red_wall.png", 16),
    Obstacle(500, 500, 50, 50, "assets/white_wall.png", 17),
    Obstacle(550, 500, 50, 50, "assets/red_wall.png", 18),
    Obstacle(600, 500, 50, 50, "assets/white_wall.png", 19),
]
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
                if not obstacle.isColliding:
                    obstacle.isColliding = True
                    print(f"Collision with obstacle id: {obstacle.id}")
            else:
                if obstacle.isColliding:
                    obstacle.isColliding = False
                    print(f"Collision with obstacle id: {obstacle.id} ended")
        else:
            if obstacle.isColliding:
                obstacle.isColliding = False
                print(f"Collision with obstacle id: {obstacle.id} ended")
        
                pass
    pygame.display.flip()






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
            if event.key == pygame.K_q:
                car.mode *= -1
    
    update()

    

    delta_time = clock.tick(120)

pygame.quit()