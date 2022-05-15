from typing import Tuple

import pygame


class Entity():
    def __init__(self, spawn_point: Tuple[int, int], image_path, scale: Tuple[int,int]):
        self.image = pygame.transform.scale(pygame.image.load(image_path), scale)
        self.rect = self.image.get_rect()
        self.set_position(spawn_point[0], spawn_point[1])
    
    def update_position(self, x, y):
        self.rect.centerx += x
        self.rect.centery += y
    
    def set_position(self, x, y):
        self.rect.center = (x, y)
        
    @property
    def y(self):
        return self.rect.centery

    @property
    def x(self):
        return self.rect.centerx