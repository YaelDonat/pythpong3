import pygame
import random

class Ball():
    def __init__(self, x, y, rayon, direction):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, self.rayon, self.rayon)
        self.random_speed_y = random.randint(1, 4)

    def move(self, speed_x, speed_y):
        self.rect.x =(self.rect.x + self.direction * speed_x)
        self.rect.y +=(self.random_speed_y * speed_y)

    def show(self, surface):
        pygame.draw.rect(surface,(230, 230, 230), self.rect)