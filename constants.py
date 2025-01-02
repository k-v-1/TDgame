
FPS=60
SCREEN_WIDTH = 1200
GAME_WIDTH = 960
SCREEN_HEIGHT = 960

#world constants
TILE_SIZE = 32
COLS = 30

#Enemy constants
ANIMATION_STEPS = 6
ANIMATION_DELAY = 100
SPAWN_COOLDOWN = 750
ENEMY_SPAWN_DATA = [
    [2,2,0,0], #lvl 1 [type0, type1, ...]
    [0,5,0,0],
    [0,1,15,0]
]
ENEMY_DATA = {
    0:{"speed": 1,
       "health": 20,
       "damage":1,
       "imageD":"Tiled/free-field-enemies-pixel-art-for-tower-defense/2/D_Walk.png",
       "imageU":"Tiled/free-field-enemies-pixel-art-for-tower-defense/2/U_Walk.png",
       "imageS":"Tiled/free-field-enemies-pixel-art-for-tower-defense/2/S_Walk.png"},
    1:{"speed": 4,
       "health": 15,
       "damage":1,
       "imageD":"Tiled/free-field-enemies-pixel-art-for-tower-defense/3/D_Walk.png",
       "imageU":"Tiled/free-field-enemies-pixel-art-for-tower-defense/3/U_Walk.png",
       "imageS":"Tiled/free-field-enemies-pixel-art-for-tower-defense/3/S_Walk.png"},
    2:{"speed": 0.5,
       "health": 50,
       "damage":1,
       "imageD":"Tiled/free-field-enemies-pixel-art-for-tower-defense/1/D_Walk.png",
       "imageU":"Tiled/free-field-enemies-pixel-art-for-tower-defense/1/U_Walk.png",
       "imageS":"Tiled/free-field-enemies-pixel-art-for-tower-defense/1/S_Walk.png"},
    3:{"speed": 1,
       "health": 20,
       "damage":1,
       "imageD":"Tiled/free-field-enemies-pixel-art-for-tower-defense/2/D_Walk.png",
       "imageU":"Tiled/free-field-enemies-pixel-art-for-tower-defense/2/U_Walk.png",
       "imageS":"Tiled/free-field-enemies-pixel-art-for-tower-defense/2/S_Walk.png"}
}

#Tower constants
# DAMAGE = 10
RANGE_WIDTH = 3

TOWER_DATA = {
    0:{
        "name": "basic",
        "damage": 5,
        "range": 5,
        "follow": False,
        "cooldown": 500,
        "bullet_speed": 3
    }, 
    1:{
        "name": "sniper",
        "damage": 10,
        "range": 10,
        "follow": False,
        "cooldown": 1500,
        "bullet_speed": 10
    }, 
    2:{
        "name": "shotgun",
        "damage": 20,
        "range": 2,
        "follow": False,
        "cooldown": 1000,
        "bullet_speed": 1
    }, 
    3:{
        "name": "follow",
        "damage": 1,
        "range": 15,
        "follow": True,
        "cooldown": 200,
        "bullet_speed": 1
    }, 
}