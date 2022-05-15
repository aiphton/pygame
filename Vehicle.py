
from typing import Tuple

import pygame

from Entity import Entity


class Vehicle(Entity):
    def __init__(self, spawn_point: Tuple[int, int]):
        super().__init__(spawn_point, './graphics/LKW.png', (66,36))
        self.orecap = 0
        self.fuelcap = 150
        self.hasLost = False
        self.delivered_ores = 0

    # Increase to 150 and then stop
    def refuel(self):
        if self.fuelcap <= 150:
            self.fuelcap += 1
        if self.fuelcap > 150:
            self.fuelcap = 150
    
    # Load ores to 100 and then stop  
    def load_ores(self):
        if self.orecap <= 100:
            self.orecap += 1
        if self.orecap > 100:
            self.orecap = 100
    
    # Unload Ores and dont go under 0    
    def decrease_ores(self):
        if self.orecap > 0:
            self.orecap -= 1
            self.delivered_ores += 1
        if self.orecap <= 0:
            self.orecap = 0
        
        return self.delivered_ores
    
    # Process player input and move accordingly
    def drive(self, deltatime, direction:str, move_speed = 400):
        """Direction: WASD as string"""
        dxy = deltatime * move_speed
        
        self.fuelcap -= 0.1
        if self.fuelcap <= 0:
            self.fuelcap = 0
            self.hasLost = True
            
        if direction.lower() == "w":
            self.update_position(0, -dxy)
        elif direction.lower() == "a":
            self.update_position(-dxy, 0)
        elif direction.lower() == "s":
            self.update_position(0, +dxy)
        elif direction.lower() == "d":
            self.update_position(+dxy, 0)
            
        else:
            raise AttributeError(f'Wrong Direction Value: {direction}')

        