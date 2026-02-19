

import math
import pygame

class Car:
    def __init__(self):
        self.x = 100
        self.y = 100        
        self.width = 120
        self.height = 60
        self.theta = math.pi * 1.5
        self.speed = 0
        self.accelerate_rate = 0.001
        self.speed_limit = 0.5
        self.speed = 0
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        self.head = pygame.Surface((10, 30))
        self.omega = 0
        self.image = pygame.transform.scale(pygame.image.load("assets/car_image.png").convert_alpha(), (self.width * 1.8, self.height * 3))
        self.mode = 1
        
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
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.theta))
        rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, rect)

    def accelerate(self, delta_time, direction):
        if self.speed < 0:
            if self.mode == 1:
                if direction == 1:
                    self.speed += self.accelerate_rate * delta_time * direction * self.mode
                else:
                    return
            elif self.speed < -self.speed_limit:
                self.speed = -self.speed_limit
            else:
                self.speed += self.accelerate_rate * delta_time * direction * self.mode
        else:
            if self.mode == -1:
                if direction == 1:
                    self.speed += self.accelerate_rate * delta_time * direction * self.mode
                else:
                    return
            elif self.speed > self.speed_limit:
                self.speed = self.speed_limit
            else:
                self.speed += self.accelerate_rate * delta_time * direction * self.mode
    
    def run(self, delta_time):
        if abs(self.speed) < 0.01:
            self.speed = 0
            return
        self.x += self.speed * math.cos(self.theta) * delta_time
        self.y -= self.speed * math.sin(self.theta) * delta_time

    def turn(self, delta_time, direction):
        self.omega = 0.003 * direction * self.speed
        self.theta += self.omega * delta_time
        if self.theta > 2 * math.pi:
            self.theta -= 2 * math.pi

