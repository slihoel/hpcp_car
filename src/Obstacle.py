import pygame
import math

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