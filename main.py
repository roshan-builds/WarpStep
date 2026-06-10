#imports
import pygame
import sys

#initialize pygame
pygame.init()

#constants
GAMELENGTH = 960
TILESIZE = 40
MAX_STABILITY = 150

#colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
DARK_CYAN = (0, 125, 125)
MAGENTA = (255, 0, 255)
DARK_MAGENTA = (125, 0, 125)
RED = (237, 33, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
STABILITY_COLOR = 0
DIM_COLOR_SWAPPABLE = 0
DIM_COLOR_STIFF = 0

#variables
player_x = 120
player_y = 480
last_move_time = 0
last_dim_change_time = 0
player_dim = 0
dim_val_1 = 0
stability_meter = 150
stability_decrease = 15

#screen setup
screen = pygame.display.set_mode((GAMELENGTH, GAMELENGTH))
font = pygame.font.SysFont(None, 28)

#dimension change function
def dim_change(keys, player_dim, current_time, last_dim_change_time, stability_level, decreasing, player_x, player_y):
    dim_change_delay = 250

    if current_time - last_dim_change_time < dim_change_delay: #waiting till enough delay
        return player_dim, last_dim_change_time, stability_level #updating values

    if keys[pygame.K_SPACE]:
        next_dim = (player_dim + 1) % 2 #nextdim is either 0 or 1, meaning two dimensions

        if next_dim % 2 == 0:
            next_dim_val_1 = 0 #first dimension
        else:
            next_dim_val_1 = 200 #second dimension

        next_swappable_wall_rects = [pygame.Rect(360 + next_dim_val_1, 400, TILESIZE, 4 * TILESIZE)] #possible location for dimension wall
        player_rect = pygame.Rect(player_x, player_y, TILESIZE, TILESIZE)

        can_swap = True #if we can swap or not
        for wall_rect in next_swappable_wall_rects:
            if player_rect.colliderect(wall_rect): #if we are in the place of the possible location
                can_swap = False #we can't swap

        if can_swap: #what decides if we can or can't swap
            player_dim = next_dim #swapping to the right dimension
            stability_level -= decreasing #stability level decreases
            last_dim_change_time = current_time #refreshing last time swapped
    
    return player_dim, last_dim_change_time, stability_level #updating global dim value
    

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

def stability_bar(stability_level, color):
    if stability_level > 100:
        color = GREEN
    elif stability_level > 50:
        color = YELLOW
    else:
        color = RED
    
    return stability_level, color

running = True #running = game loop
while running:
    current_time = pygame.time.get_ticks() #using pygame timer instead of time module

    for event in pygame.event.get(): #end game loop
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player_dim, last_dim_change_time, stability_meter = dim_change(keys, player_dim, current_time, last_dim_change_time, stability_meter, stability_decrease, player_x, player_y)

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
    
    #drawing dimensional walls
    for wall_rect in swappable_wall_rects:
        pygame.draw.rect(screen, DIM_COLOR_SWAPPABLE, wall_rect)
    for wall_rect in stiff_wall_rects:
        pygame.draw.rect(screen, DIM_COLOR_STIFF, wall_rect)
    
    meter = pygame.Rect(680, 40, stability_meter, TILESIZE)
    stability_meter, STABILITY_COLOR = stability_bar(stability_meter, STABILITY_COLOR)
    stability_percent = int((stability_meter / MAX_STABILITY) * 100)
    stability_text = font.render(f"Dimensional Stability: {stability_percent}%", True, STABILITY_COLOR)
    stability_text_rect = stability_text.get_rect(midbottom=meter.midtop)
    screen.blit(stability_text, stability_text_rect)
    pygame.draw.rect(screen, STABILITY_COLOR, meter)
    pygame.display.flip() #refreshing game

#what happens after loop finishes
pygame.quit()
sys.exit()
