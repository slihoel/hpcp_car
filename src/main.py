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
gamestate = "playing"
timer = 0
collide = 0
level = 1

def draw_Corners(corners):
    for i, corner in enumerate(corners):
        pygame.draw.circle(window, (i * 63, i * 63, i * 63), corner, 5)

def sin_a_plus_b(a, b):
    return math.sin(a) * math.cos(b) + math.cos(a) * math.sin(b)

def cos_a_plus_b(a, b):
    return math.cos(a) * math.cos(b) - math.sin(a) * math.sin(b)
        

car = Car.Car()
pos = None

obstacles = drawmap.getMap(level)

def update(gamestate=gamestate, timer=timer, collide=collide, pos=None, obstacles=obstacles):
    window.fill((50, 50, 50))

    if gamestate == "playing":
        font = pygame.font.Font(None, 50)
        if timer < 60000:
            timer_text = font.render(f"Time:  {timer / 1000:.3f}s", True, (255, 255, 255))
        else:
            timer_text = font.render(f"Time:  {timer // 60000}:{(timer % 60000) / 1000:.2f}s", True, (255, 255, 255))
        window.blit(timer_text, (10, 10))
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
                        if obstacle.id == -1:
                            gamestate = "win"
                        else:
                            gamestate = "lose"
                else:
                    if obstacle.isColliding:
                        obstacle.isColliding = False
                        print(f"Collision with obstacle id: {obstacle.id} ended")
            else:
                if obstacle.isColliding:
                    obstacle.isColliding = False
                    print(f"Collision with obstacle id: {obstacle.id} ended")
        car.draw(window)

    elif gamestate == "win":
        font = pygame.font.Font(None, 100)
        btnfont = pygame.font.Font(None, 50)
        if timer < 60000:
            text = font.render(f"Good!, Time:  {timer / 1000:.3f}s", True, (255, 255, 255))
        else:
            text = font.render(f"Good!, Time:  {timer // 60000}:{(timer % 60000) / 1000:.2f}s", True, (255, 255, 255))
        window.blit(text, (500, 500))
        restartbtn = pygame.Rect(500, 600, 160, 50)
        nextbtn = pygame.Rect(800, 600, 200, 50)
        restert_text = btnfont.render("Restart", True, (255, 255, 255)) 
        next_text = btnfont.render("Next Level", True, (255, 255, 255))
        pygame.draw.rect(window, (0, 255, 0), restartbtn)
        pygame.draw.rect(window, (0, 255, 0), nextbtn)
        window.blit(restert_text, (restartbtn.x + 20, restartbtn.y + 10))
        window.blit(next_text, (nextbtn.x + 20, nextbtn.y + 10))
        if pos is not None and restartbtn.collidepoint(pos):  
            timer = 0
            car.__init__()
            gamestate = "playing"
            pos = None
        elif pos is not None and nextbtn.collidepoint(pos):
            timer = 0
            car.__init__()
            gamestate = "playing"
            level += 1
            obstacles = drawmap.getMap(level)
            pos = None
        
    
    elif gamestate == "lose":
        btnfont = pygame.font.Font(None, 50)
        restartbtn = pygame.Rect(500, 600, 160, 50)
        restert_text = btnfont.render("Restart", True, (255, 255, 255)) 
        pygame.draw.rect(window, (255, 0, 0), restartbtn)
        font = pygame.font.Font(None, 100)
        text = font.render("Game Over!", True, (255, 255, 255))
        window.blit(text, (500, 500))
        window.blit(restert_text, (restartbtn.x + 20, restartbtn.y + 10)) 
        if pos is not None and restartbtn.collidepoint(pos):  
            timer = 0
            car.__init__()
            gamestate = "playing"
            pos = None


    pygame.display.flip()

    return gamestate, timer, collide, pos, obstacles






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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
    gamestate, timer, collide, pos, obstacles = update(gamestate, timer, collide, pos, obstacles)

    

    delta_time = clock.tick(120)
    if gamestate == "playing":
        timer += delta_time
pygame.quit()