from typing import Tuple
from Entity import Entity

from Vehicle import Vehicle

class Helicopter(Entity):
    def __init__(self, spawn_point: Tuple[int, int]):
        super().__init__(spawn_point, './graphics/Helicopter.png', (60,40))
        self.stolen_ores = 0
    
    # chase player around with the help of x,y of the player position 
    def chase(self, player_pos, deltatime):
        dx = (player_pos[0] - self.rect.centerx) * deltatime
        dy = (player_pos[1] - self.rect.centery) * deltatime
        if (abs(dx) <= 50 ):
            dx *= 2 
        if (abs(dy) <= 50):
            dy *= 2
        self.update_position(dx, dy)
    
    # Steal from player and keep chasing him
    def collide(self, player: Vehicle, deltatime):
        self.steal(player)
        self.chase(player.rect.center, deltatime)
    
    # Steal 1 ore from player and do not go under 0
    def steal(self, player: Vehicle):
        if player.orecap > 0:
            player.orecap -= 1
            self.stolen_ores += 1
        if player.orecap <= 0:
            player.orecap = 0
            return 0
        
        return self.stolen_ores