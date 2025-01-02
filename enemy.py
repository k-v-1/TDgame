import pygame as pg
from pygame.math import Vector2
from random import randint

from constants import *
from hero import load_images

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints: list, roadnr=None):
        super().__init__()
        if roadnr is None:
            roadnr = randint(1,4)
        self.waypoints = waypoints[f'road{roadnr}']
        self.target_waypoint = 1
        self.props = ENEMY_DATA[enemy_type]
        self.speed = self.props["speed"]
        self.health = self.props["health"]
        
        #animation variables
        self.sprite_sheetD = pg.image.load(self.props["imageD"]).convert_alpha()
        self.animation_listD = load_images(self.sprite_sheetD)
        self.sprite_sheetU = pg.image.load(self.props["imageU"]).convert_alpha()
        self.animation_listU = load_images(self.sprite_sheetU)
        self.sprite_sheetS = pg.image.load(self.props["imageS"]).convert_alpha()
        self.animation_listS = load_images(self.sprite_sheetS)
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        #setup image
        self.angle = 90
        self.original_image = self.animation_listD[self.frame_index]
        self.image = self.original_image #TODO change later when changing orientation??
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(self.waypoints[0])

    def update(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            self.kill()
        self.move(world)
        self.update_img()
        self.play_animation()
        self.rect.center = self.rect.center

    def move(self, world):
        #define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.rect.center
            self.angle = self.movement.as_polar()[1] #angle in degrees wrt positive x-axis (-180 -> 180)
        else:
            #enemy has reached the end of the path
            self.kill()
            # world.health -= 1
            world.missed_enemies += 1

        #calculate distance to target
        dist = self.movement.length()
        #check if remaining distance is greater than the enemy speed
        if dist >= (self.speed * world.game_speed):
            self.rect.center += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            #skip remaining distance to waypoint
            if dist != 0:
                self.rect.center += self.movement.normalize() * dist
            self.target_waypoint += 1

    def update_img(self):
        if -135 < self.angle <= -45: #TODO: change by else to avoid errors?
            self.original_image = self.animation_listU[self.frame_index]
            rotate_angle = 270-self.angle
        elif -45 < self.angle <= 45 :
            self.original_image = pg.transform.flip(self.animation_listS[self.frame_index], True, False)
            rotate_angle = 0 - self.angle
        elif 45 < self.angle <= 135:
            self.original_image = self.animation_listD[self.frame_index]
            rotate_angle = 90 - self.angle
        elif 135 < self.angle or self.angle <= -135:
            self.original_image = self.animation_listS[self.frame_index]
            rotate_angle = 180 - self.angle
        self.image = pg.transform.rotate(self.original_image, rotate_angle)
    
    def play_animation(self):
        #check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > ANIMATION_DELAY//self.speed:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #check if the animation has finished and reset to idle
            if self.frame_index >= len(self.animation_listD):
                self.frame_index = 0

