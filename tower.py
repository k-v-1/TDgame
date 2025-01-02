import pygame as pg
from constants import *
import math


def range_border(range):
    #create transparent circle showing range
    range_image = pg.Surface((range * 2, range * 2))
    range_image.fill((0, 0, 0))
    range_image.set_colorkey((0, 0, 0))
    pg.draw.circle(range_image, "grey100", (range, range), range, width=RANGE_WIDTH)
    range_image.set_alpha(100)
    range_rect = range_image.get_rect()
    return range_image, range_rect


class Tower(pg.sprite.Sprite):
    def __init__(self, tile_x, tile_y, type=0):
        super().__init__()
        images = ['Tconc0', 'Tpunt1', 'Tpunt3', 'Tconc2'] #TODO: just change filenames
        self.image = pg.image.load(f"img/{images[type]}.png")
        self.image = pg.transform.scale(self.image,(32,32))

        #calculate center coordinates
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x + 0.5) * TILE_SIZE
        self.y = (self.tile_y + 0.5) * TILE_SIZE
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #get data from type
        self.properties = TOWER_DATA[type]
        self.health = 50

        #target and bullets
        self.bullet_group = pg.sprite.Group()
        self.last_bullet = pg.time.get_ticks()
        self.target = None

        #selection and range
        self.selected = True
        self.range = self.properties["range"] * TILE_SIZE
        self.range_image, self.range_rect = range_border(self.range)
        self.range_rect.center = self.rect.center
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    def update(self, enemy_group):
        if self.health <= 0:
            self.kill()
        self.target = None
        self.pick_target(enemy_group)
        self.fire()

    def pick_target(self, enemy_group):
        #find an enemy to target
        x_dist = 0
        y_dist = 0
        #check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.rect.center[0] - self.x
                y_dist = enemy.rect.center[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    break
        
    def fire(self):
        if self.target is not None:
            # Check if enough time past since last fire
            if pg.time.get_ticks() - self.last_bullet > self.properties["cooldown"]:  #firerate
                self.last_bullet = pg.time.get_ticks()
                self.bullet_group.add(Bullet(self.rect.center,
                                             self.target,
                                             self.properties["bullet_speed"],
                                             self.properties["damage"],
                                             follow=self.properties["follow"]))



class Bullet(pg.sprite.Sprite):

    def __init__(self, coords, target, speed, damage, follow=False):
        super().__init__()
        #properties
        self.speed = speed
        self.damage = damage
        self.follow = follow

        #image setup
        self.image = pg.image.load("img/Tcirc0.png")
        self.image = pg.transform.scale(self.image,(5,5))
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.pos = self.rect.center

        #target setup
        self.target = target
        x_dist = self.target.rect.center[0] - self.rect.center[0]
        y_dist = self.target.rect.center[1] - self.rect.center[1]
        self.direction = math.degrees(math.atan2(-y_dist, x_dist))
        self.move_vec = pg.math.Vector2()
        self.move_vec.from_polar((self.speed, -self.direction)) #speed, angle in degrees

    def move(self, enemy_group):
        if self.follow and self.target in enemy_group:
            x_dist = self.target.rect.center[0] - self.rect.center[0]
            y_dist = self.target.rect.center[1] - self.rect.center[1]
            self.direction = math.degrees(math.atan2(-y_dist, x_dist))
            self.move_vec.from_polar((self.speed, -self.direction)) #speed, angle in degrees

        self.pos = self.pos + self.move_vec
        self.rect.center = round(self.pos[0]), round(self.pos[1])
        #kill bullet once enemy is hit
        for enemy in enemy_group:
            if self.rect.colliderect(enemy):
                enemy.health -= self.damage
                self.kill()
        # kill bullet once out of game window
        if self.rect.x < 0 or self.rect.y < 0 or self.rect.x > GAME_WIDTH or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect) 