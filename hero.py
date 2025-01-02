import pygame as pg
from constants import *
from pygame.locals import *
import math


def load_images(sprite_sheet, steps=ANIMATION_STEPS):
    #extract images from spritesheet
    size = sprite_sheet.get_height()
    img_list = []
    for x in range(steps):
        temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
        img_list.append(temp_img)
    return img_list

class Hero(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_down = pg.image.load("Tiled/free-field-enemies-pixel-art-for-tower-defense/4/D_Walk.png")
        self.img_up = pg.image.load("Tiled/free-field-enemies-pixel-art-for-tower-defense/4/U_Walk.png")
        self.img_side = pg.image.load("Tiled/free-field-enemies-pixel-art-for-tower-defense/4/S_Walk.png")
        self.d_list = load_images(self.img_down)
        self.u_list = load_images(self.img_up)
        self.s_list = load_images(self.img_side)
        self.direction2rotate = {'U':(self.u_list, 0), 'D':(self.d_list, 0), 'L':(self.s_list, 0), 'R':(self.s_list, 0),
                            'UL':(self.u_list, 45), 'UR':(self.u_list, -45), 'DL':(self.d_list, -45), 'DR':(self.d_list, 45)}

        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.d_list[self.frame_index]
        self.direction = 'D'

        self.rect = self.image.get_rect()
        self.rect.center = (GAME_WIDTH //2, SCREEN_HEIGHT //2)

        # fire props
        self.range = 2* TILE_SIZE
        self.img_glow = pg.image.load("Tiled/2d-special-effects/light_glow_effect.png")
        self.glow_list = load_images(self.img_glow, steps=10)
        self.glow_index = 0
        self.glow_img = self.glow_list[self.glow_index]
        self.glow_rect = self.glow_img.get_rect()
        self.glow_time = pg.time.get_ticks()
        self.last_attack = pg.time.get_ticks()
        self.target = None
        self.damage = 20


    def update(self):
        self.move()
        self.play_animation()
        if self.glow_index != -1:
            self.play_glow()

    def move(self):
        pressed_keys = pg.key.get_pressed()
        direction = ''
        if any([pressed_keys[k] for k in [K_UP, K_DOWN, K_LEFT, K_RIGHT]]):
            #move + save direction
            if self.rect.top > 0 and pressed_keys[K_UP]:
                    self.rect.move_ip(0, -5)
                    direction += 'U'
            elif self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
                    self.rect.move_ip(0,5)
                    direction += 'D'
            if self.rect.left > 0 and pressed_keys[K_LEFT]:
                    self.rect.move_ip(-5, 0)
                    direction += 'L'
            elif self.rect.right < GAME_WIDTH and pressed_keys[K_RIGHT]:
                    self.rect.move_ip(5, 0)
                    direction += 'R'
        #update or keep old direction
        if direction == '':
            direction = self.direction
        self.direction = direction

        if self.direction == 'R':
            self.image = pg.transform.flip(self.s_list[self.frame_index], True, False)
        else:
            transform = self.direction2rotate[self.direction]
            self.image = pg.transform.rotate(transform[0][self.frame_index], transform[1])

    def play_animation(self, delay = ANIMATION_DELAY):
        #check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > delay:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #check if the animation has finished and reset to idle
            if self.frame_index >= ANIMATION_STEPS:
                self.frame_index = 0

    def play_glow(self):
        self.glow_img = self.glow_list[self.glow_index]
        if pg.time.get_ticks() - self.glow_time > 1:
            self.glow_time = pg.time.get_ticks()
            self.glow_index += 1
            if self.glow_index >= 10:
                self.glow_index = -1 #glow off


    def attack(self, enemy_group):
        self.target = None
        self.pick_target(enemy_group)
        if self.target is not None:
            if pg.time.get_ticks() - self.last_attack > 500: #TODO: firerate
                self.last_attack = pg.time.get_ticks()
                self.glow_rect.center = self.target.rect.center
                self.glow_index = 0
                self.target.health -= self.damage

    def pick_target(self, enemy_group):
        #find an enemy to target
        x_dist = 0
        y_dist = 0
        #check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.rect.x
                y_dist = enemy.pos[1] - self.rect.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    #damage enemy
                    # self.target.health -= DAMAGE
                    break

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.glow_index != -1:
            surface.blit(self.glow_img, self.glow_rect)