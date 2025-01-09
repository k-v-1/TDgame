import pygame as pg
from pygame.locals import *
import sys
import json

from world import World
from enemy import Enemy
from tower import Tower, range_border
from hero import Hero
from button import Button
from constants import *

# https://github.com/russs123/tower_defence_tut


pg.init()

FramePerSec = pg.time.Clock()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0,0,0))
pg.display.set_caption("Test1245")

#load images
map_image = pg.image.load('Tiled/map.png').convert_alpha()
buy_tower0_img = pg.transform.scale(pg.image.load('img/Tconc0.png').convert_alpha(), (32,32))
buy_tower1_img = pg.transform.scale(pg.image.load('img/Tpunt1.png').convert_alpha(), (32,32))
buy_tower2_img = pg.transform.scale(pg.image.load('img/Tpunt3.png').convert_alpha(), (32,32))
buy_tower3_img = pg.transform.scale(pg.image.load('img/Tconc2.png').convert_alpha(), (32,32))
cursor_tower0 = pg.transform.scale(pg.image.load('img/Tconc0.png').convert_alpha(), (32,32))
cursor_tower1 = pg.transform.scale(pg.image.load('img/Tpunt1.png').convert_alpha(), (32,32))
cursor_tower2 = pg.transform.scale(pg.image.load('img/Tpunt3.png').convert_alpha(), (32,32))
cursor_tower3 = pg.transform.scale(pg.image.load('img/Tconc2.png').convert_alpha(), (32,32))

tower_list = [cursor_tower0, cursor_tower1, cursor_tower2, cursor_tower3]
cancel_btn_img = pg.transform.scale(pg.image.load('img/buttonNormal.png').convert_alpha(), (159,47))
cancel_btnHigh_img = pg.transform.scale(pg.image.load('img/buttonHighlight.png').convert_alpha(), (159,47))
cancel_btnPres_img = pg.transform.scale(pg.image.load('img/buttonPressed.png').convert_alpha(), (159,47))
spawn_button_img = pg.transform.scale(pg.image.load('img/Tcirc2.png').convert_alpha(), (32,32))
#create images
red_tile = pg.Surface((TILE_SIZE, TILE_SIZE))
red_tile.fill((255,0,0))
red_tile_rect = red_tile.get_rect()

#create buttons
tower_button0 = Button(GAME_WIDTH + 10, 30, buy_tower0_img)
tower_button1 = Button(GAME_WIDTH + 50, 30, buy_tower1_img)
tower_button2 = Button(GAME_WIDTH + 90, 30, buy_tower2_img)
tower_button3 = Button(GAME_WIDTH + 130, 30, buy_tower3_img)
cancel_button = Button(GAME_WIDTH + 10, 80, cancel_btn_img, cancel_btnPres_img, cancel_btnHigh_img)
start_button = Button(GAME_WIDTH + 10, 500, cancel_btn_img, cancel_btnPres_img, cancel_btnHigh_img)
spawn_btns = [Button(864, 0, spawn_button_img),
              Button(928, 864, spawn_button_img),
              Button(32, 928, spawn_button_img),
              Button(0, 32, spawn_button_img)]


#load json data (polyline etc.)
with open('Tiled/map.tmj') as file:
    world_data = json.load(file)


def closest_tile(coords: tuple, tilenr=False):
    mouse_x, mouse_y = coords
    tile_x = mouse_x // TILE_SIZE
    tile_y = mouse_y // TILE_SIZE
    if tilenr:
        #returns x and y in tilenumbers
        return tile_x, tile_y
    else:
        # returns center of tile
        return (tile_x+0.5) * TILE_SIZE, (tile_y+0.5) * TILE_SIZE

def reset_selection(new_select=None):
    if world.selected_tower is not None:
        world.selected_tower.selected = False
        world.selected_tower = None
    if new_select is not None:
        world.selected_tower = new_select
        new_select.selected = True

def create_tower(mouse_pos: tuple):
    mouse_tile_x, mouse_tile_y = closest_tile(mouse_pos, tilenr=True)
    #calculate the sequential number of the tile
    tile_number = (mouse_tile_y * COLS) + mouse_tile_x
    #check if that tile is free
    if world.bg_map[tile_number] == 131 and mouse_pos[0] < GAME_WIDTH:
        #check that there isn't already a tower there
        space_is_free = True
        for tower in tower_group:
            if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
                space_is_free = False
        #if it is a free space then create tower
        if space_is_free == True:
            new_tower = Tower(mouse_tile_x, mouse_tile_y, towertype)
            tower_group.add(new_tower)
            reset_selection(new_select=new_tower)
            #deduct cost of tower
            #   world.money -= c.BUY_COST
        else:
            red_tile_rect.center = closest_tile(mouse_pos, tilenr=False)
            screen.blit(red_tile, red_tile_rect)
    elif mouse_pos[0] < GAME_WIDTH:
        red_tile_rect.center = closest_tile(mouse_pos, tilenr=False)
        screen.blit(red_tile, red_tile_rect)
    else:
        world.placing_towers = False


world = World(world_data, map_image)
world.process_data()
world.reset_level()
hero = Hero()
occupied_tiles = []
tower_group = pg.sprite.Group()
enemy_group = pg.sprite.Group()
last_enemy_spawn = pg.time.get_ticks()

#game loop
while True:
    screen.fill((0,0,0))
    world.draw(screen)
    
    if world.start_wave:
        #Spawning enemies
        if pg.time.get_ticks() - last_enemy_spawn > SPAWN_COOLDOWN:
            if world.spawned_enemies < len(world.enemy_list):
                enemy_type = world.enemy_list[world.spawned_enemies]
                enemy = Enemy(enemy_type, world.waypoints)
                enemy_group.add(enemy)
                world.spawned_enemies += 1
                last_enemy_spawn = pg.time.get_ticks()
        if world.killed_enemies + world.missed_enemies == len(world.enemy_list):
            world.reset_level()
            world.start_inverse = True

    elif world.start_inverse:
        enemy_group.add(hero)
        if pg.time.get_ticks() - last_enemy_spawn > SPAWN_COOLDOWN:
            if world.spawned_enemies < len(world.enemy_list):
                for roadnr, spawn_button in enumerate(spawn_btns):
                    if spawn_button.draw(screen):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, roadnr=roadnr+1)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        last_enemy_spawn = pg.time.get_ticks()
        if world.killed_enemies + world.missed_enemies == len(world.enemy_list):
            enemy_group.remove(hero)
            world.level += 1
            world.reset_level()
            world.start_inverse = False

    else:
        if start_button.draw(screen):
            world.start_wave = True
        for i, btn in enumerate([tower_button0, tower_button1, tower_button2, tower_button3]):
            if btn.draw(screen):
                world.placing_towers = True
                towertype = i
        #if placing towers then show the cancel button as well
        if world.placing_towers == True:
            #show cursor tower
            cursor_rect = tower_list[towertype].get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = closest_tile(cursor_pos, tilenr=False)
            if cursor_pos[0] <= GAME_WIDTH:
                screen.blit(tower_list[towertype], cursor_rect)
                #draw range
                range_image, range_rect = range_border(TOWER_DATA[towertype]["range"]*TILE_SIZE) #TODO: range
                range_rect.center = closest_tile(cursor_pos, tilenr=False)
                screen.blit(range_image, range_rect)
            if cancel_button.draw(screen):
                world.placing_towers = False

    #update and draw Hero, enemies and towers
    if not world.start_inverse:
        hero.update()
        hero.draw(screen)
    enemy_group.update(world)
    enemy_group.draw(screen)
    for tower in tower_group:
        tower.update(enemy_group)
        tower.draw(screen)
        for b in tower.bullet_group:
            b.move(enemy_group)
        tower.bullet_group.draw(screen)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        # on left click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos = pg.mouse.get_pos()
            if world.placing_towers:
                create_tower(pos)
            else:
                reset_selection()
                for t in tower_group:
                    if t.rect.collidepoint(pos):
                        reset_selection(new_select=t)
                        break
        #on space
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if world.start_wave:
                hero.attack(enemy_group)
            elif world.start_inverse:
                hero.attack(tower_group)

        # Cancel everything
        if (
            (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or  #ESC
            (event.type == pg.MOUSEBUTTONDOWN and event.button == 3)    #RightMouseBtn
        ): 
            world.placing_towers = False
            reset_selection()


    pg.display.update()
    FramePerSec.tick(FPS)
