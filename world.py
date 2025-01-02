import pygame as pg
from constants import *

class World():
    def __init__(self, data, map_image):
        self.image = map_image
        self.level_data = data
        self.waypoints = []
        self.game_speed = 1
        self.level = 1

        #enemy variables
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

        #general tower variables
        self.placing_towers = False
        self.selected_tower = None

    def draw(self,surface):
        surface.blit(self.image, (0,0))
    
    def process_data(self):
        #look through json/list-data to extract relevant info
        for layer in self.level_data["layers"]:
            if layer["name"] == "fg":
                self.fg_map = layer["data"]
            elif layer["name"] == "bg":
                self.bg_map = layer["data"]
            elif layer["name"] in ["road1", "road2", "road3", "road4"]:
                waypoint_data = layer["objects"][0]["polyline"]
                self.waypoints.append([(point.get("x"), point.get("y")) for point in waypoint_data])
        print(self.waypoints)

    # def process_waypoints(self, data):
    #     #iterate through waypoints to extract individual sets of x and y coordinates
    #     for point in data:
    #         temp_x = point.get("x")
    #         temp_y = point.get("y")
    #         self.waypoints.append((temp_x, temp_y))
    
    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type, enemies2spawn in enumerate(enemies):
            for _ in range(enemies2spawn):
                self.enemy_list.append(enemy_type)
        # for enemy_type in range(enemies):
        #     enemies_to_spawn = enemies[enemy_type]
        #     for _ in range(enemies_to_spawn):
        #         self.enemy_list.append(enemy_type)
            #now randomize the list to shuffle the enemies
            # random.shuffle(self.enemy_list)