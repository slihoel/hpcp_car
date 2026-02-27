import pygame
import math
import pyautogui
import collisiondetector as cd
import Car
import Obstacle as obs
import drawmap

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
        

car = Car.Car()


obstacles = drawmap.getMap(1)

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

    car.draw(window)
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