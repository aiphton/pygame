from turtle import width
import pygame
from pytmx import load_pygame
import pytmx
from Helicopter import Helicopter

from Vehicle import Vehicle


pygame.init()
width = 900
height = 600
moveSpeed = 100
max_orecap = 100

# Init Player and Helicopter Objects
vehicle = Vehicle((0, 250))
helicopter = Helicopter((500, 1000))

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Transporter Spiel')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False


data = load_pygame("Map/map_v3.tmx")
map_dimensions = data.width*data.tilewidth, data.height*data.tileheight
map_screen = pygame.Surface(map_dimensions)

game_name = font.render('Transporter Spiel', False, (111, 196, 169))
game_message = font.render('Press Space to play the game', False, (111, 196, 169))

for layer in data.layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, image in layer.tiles():
            map_screen.blit(
                image, (x*data.tilewidth, y*data.tileheight,)
            )

map_screen = pygame.transform.scale(map_screen, (width, height))

scale_factor_x = width / (data.width*data.tilewidth)
scale_factor_y = height / (data.height*data.tileheight)

fuel_station_rect: pygame.Rect = None
ores_rect: pygame.Rect = None
target_rect: pygame.Rect = None

# Resize Areas to the size of the map
objectlayer: pytmx.pytmx.TiledObjectGroup = data.get_layer_by_name("Areas")
obj: pytmx.TiledObject
for obj in objectlayer:
    if obj.name == "Fuel_Station":
        fuel_station_rect = pygame.Rect(
            obj.x*scale_factor_x, obj.y*scale_factor_y, obj.width*scale_factor_x, obj.height*scale_factor_y)
    if obj.name == "Ores":
        ores_rect = pygame.Rect(obj.x*scale_factor_x, obj.y*scale_factor_y,
                                obj.width*scale_factor_x, obj.height*scale_factor_y)
    if obj.name == "Target":
        target_rect = pygame.Rect(obj.x*scale_factor_x, obj.y*scale_factor_y,
                                  obj.width*scale_factor_x, obj.height*scale_factor_y)

while True:
    deltatime = clock.get_time()/1000
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print('goodbye!')
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Restart Game
            max_orecap = 100
            helicopter.stolen_ores = 0
            vehicle.delivered_ores = 0
            vehicle.fuelcap = 150
            vehicle.orecap = 0
            vehicle.set_position(0, 250)
            helicopter.set_position(500, 1000)
            game_active = True
            vehicle.hasLost = False

    if game_active and not vehicle.hasLost:
        
        # Initialzie Screen Messages
        fuel_stat_message = font.render("Tank: " + str(round(vehicle.fuelcap, 1)) + " / 150", False, (111, 196, 169))
        ores_stat_message = font.render("Erze: " + str(round(vehicle.orecap, 1))+ " / 100" , False, (111, 196, 169))
        ores_delivered_info = font.render("Ores delivered:" + str(vehicle.delivered_ores) + " / 80", False, (111, 196, 169))
        ores_stolen_info = font.render("Ores stolen:" + str(helicopter.stolen_ores) + " / 20", False, (111, 196, 169))
        ores_position = font.render("Ores loading", False, (111, 196, 169))

        deltatime = clock.get_time()/1000
        screen.fill((0, 0, 0))  # reset screen to black

        # process key strokes and move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            vehicle.drive(deltatime, "w")
        if keys[pygame.K_a]:
            vehicle.drive(deltatime, "a")
        if keys[pygame.K_s]:
            vehicle.drive(deltatime, "s")
        if keys[pygame.K_d]:
            vehicle.drive(deltatime, "d")
        # Border
        if vehicle.rect.top < 0:
            vehicle.rect.top = 0
        if vehicle.rect.left < 0:
            vehicle.rect.left = 0
        if vehicle.rect.bottom >= screen.get_height():
            vehicle.rect.bottom = screen.get_height()
        if vehicle.rect.right >= screen.get_width():
            vehicle.rect.right = screen.get_width()

        # Collision with Fuel Station, Ore loading zone and Ore unloading zone
        if fuel_station_rect.collidepoint(vehicle.rect.center):
            vehicle.refuel()
        if ores_rect.collidepoint(vehicle.rect.center):
            vehicle.load_ores()
        if target_rect.collidepoint(vehicle.rect.center):
            # unload Ores if player is in designated area
            vehicle.decrease_ores()
            if vehicle.delivered_ores >= 80:
                game_active = False
            
        # Steal Ores from Vehicle if Ores > 0
        if vehicle.rect.colliderect(helicopter.rect):
            helicopter.collide(vehicle, deltatime)
            helicopter.steal(vehicle)
            if helicopter.stolen_ores >= 20:
                game_active = False
        
        # Chase after player
        helicopter.chase(vehicle.rect.center, deltatime)

        # Show Messages on screen
        screen.blit(map_screen, (0, 0))
        screen.blit(ores_stat_message, (5, 90))
        screen.blit(fuel_stat_message, (5, 60))
        screen.blit(ores_delivered_info, (5,30))
        screen.blit(ores_stolen_info, (5, 0))
        
        # Draw player and Helicopter on Screen
        screen.blit(vehicle.image, vehicle.rect)
        screen.blit(helicopter.image, helicopter.rect)
    else:
        # Show this message if game over or game got started
        screen.blit(game_name, (width/3, height/4))
        screen.blit(game_message, (230, 200))

    pygame.display.update()
    clock.tick(60)
