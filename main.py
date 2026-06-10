#imports
import pygame
import sys

#initialize pygame
pygame.init()

#constants
GAMELENGTH = 960
TILESIZE = 40

#colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
DARK_CYAN = (0, 125, 125)
MAGENTA = (255, 0, 255)
DARK_MAGENTA = (125, 0, 125)
RED = (237, 33, 0)
DIM_COLOR_SWAPPABLE = 0
DIM_COLOR_STIFF = 0

#variables
player_x = 120
player_y = 480
last_move_time = 0
last_dim_change_time = 0
player_dim = 0
dim_val_1 = 0

#screen setup
screen = pygame.display.set_mode((GAMELENGTH, GAMELENGTH))

#dimension change function
def dim_change(keys, player_dim, current_time, last_dim_change_time):
    dim_change_delay = 250

    if current_time - last_dim_change_time < dim_change_delay:
        return player_dim, last_dim_change_time

    if keys[pygame.K_SPACE]:
        player_dim = (player_dim + 1) % 2
        last_dim_change_time = current_time

    return player_dim, last_dim_change_time #updating global dim value

#movement function
def movement(x, y, keys, current_time, last_move_time, wall_rects):
    move_delay = 180 #time between movement to give blocky retro movement

    if current_time - last_move_time < move_delay: #if the move delay time has passed
        return x, y, last_move_time #updates these factors for the whole game loop
    
    #backup variables
    old_x = x
    old_y = y

    #key -> movement check
    if keys[pygame.K_RIGHT]: 
        x += TILESIZE #moving in tile chunk
        last_move_time = current_time
    elif keys[pygame.K_LEFT]: 
        x -= TILESIZE #moving in tile chunk
        last_move_time = current_time
    elif keys[pygame.K_DOWN]: 
        y += TILESIZE #moving in tile chunk
        last_move_time = current_time
    elif keys[pygame.K_UP]: 
        y -= TILESIZE #moving in tile chunk
        last_move_time = current_time
    
    player_rect = pygame.Rect(x, y, TILESIZE, TILESIZE)

    for wall_rect in wall_rects:
        if player_rect.colliderect(wall_rect):
            x = old_x
            y = old_y

    return x, y, last_move_time #updating factors for whole game loop


running = True #running = game loop
while running:
    current_time = pygame.time.get_ticks() #using pygame timer instead of time module

    for event in pygame.event.get(): #end game loop
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player_dim, last_dim_change_time = dim_change(keys, player_dim, current_time, last_dim_change_time)

    if player_dim % 2 == 0:
        DIM_COLOR_SWAPPABLE = CYAN
        DIM_COLOR_STIFF = DARK_CYAN
        dim_val_1 = 0
    else:
        DIM_COLOR_SWAPPABLE = MAGENTA
        DIM_COLOR_STIFF = DARK_MAGENTA
        dim_val_1 = 200

    #collection of dim-swapping walls
    swappable_wall_rects = [pygame.Rect(360 + dim_val_1, 400, TILESIZE, 4 * TILESIZE)]
    stiff_wall_rects = [pygame.Rect(0, 560, GAMELENGTH, TILESIZE), pygame.Rect(0, 360, GAMELENGTH, TILESIZE)]
    all_wall_rects = swappable_wall_rects + stiff_wall_rects

    #player value updating
    player_x, player_y, last_move_time = movement(player_x, player_y, keys, current_time, last_move_time, all_wall_rects)

    screen.fill((10, 10, 20)) #clears screen every frame
    pygame.draw.rect(screen, RED, (player_x, player_y, TILESIZE, TILESIZE)) #draws player
    
    #
    for wall_rect in swappable_wall_rects:
        pygame.draw.rect(screen, DIM_COLOR_SWAPPABLE, wall_rect)
    for wall_rect in stiff_wall_rects:
        pygame.draw.rect(screen, DIM_COLOR_STIFF, wall_rect)
    
    pygame.display.flip() #refreshing game

#what happens after loop finishes
pygame.quit()
sys.exit()
