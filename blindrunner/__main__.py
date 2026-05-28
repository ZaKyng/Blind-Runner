import os
import pygame
#import new_nodes
from pygame import Vector2
from ZaKnode import *
from .lib import lib
from .lib.scenes import *


# ----- Pygame setup ----- #
def run():
    screen_size = (1920, 1080)
    my_game = nodes.Game(screen_size, __file__, fps = 240, screen_ratio = 16/9, overflow_hidden = True)

    my_game.fonts.addFont("main", my_game.directory("assets/font_utendo_a.ttf"), 3)

    global_assets = {
        "tile_placement" : {
            "ground" : [4, 0],
            "player_spawn" : [0, 3],
            "finish" : [4, 3],
            "spikes" : [4, 4],
            "g_enemy" : [5, 1],
            "f_enemy" : [4, 5],

            "ground_BR" : [0, 0],
            "ground_BLR" : [1, 0],
            "ground_BL" : [2, 0],
            "ground_TBR" : [0, 1],
            "ground_TBLR" : [1, 1],
            "ground_TBL" : [2, 1],
            "ground_TR" : [0, 2],
            "ground_TLR" : [1, 2],
            "ground_TL" : [2, 2],
            "ground_LR" : [3, 0],
            "ground_L" : [3, 1],
            "ground_R" : [3, 2],
            "ground_T" : [4, 1],
            "ground_B" : [4, 2],
            "ground_TB" : [5, 0],
        },
        "tile_maps" : [],
        "backgrounds" : [],
    
        "animations" : {
            "player" : {
            
            },
            "g_enemy" : {
            
            },
            "f_enemy" : {
            
            }
        }
    }
    

    
    global_assets["tile_maps"].append(resources.SpriteSheet(my_game.directory("assets/final_tiles-1-test.png"), (8, 8), alpha_channel = True))
    global_assets["tile_maps"].append(resources.SpriteSheet(my_game.directory("assets/final_tiles-2-test.png"), (8, 8), alpha_channel = True))
    global_assets["tile_maps"].append(resources.SpriteSheet(my_game.directory("assets/final_tiles-3-test.png"), (8, 8), alpha_channel = True))
    global_assets["tile_maps"].append(resources.SpriteSheet(my_game.directory("assets/final_tiles-4-test.png"), (8, 8), alpha_channel = True))

    global_assets["backgrounds"].append(resources.Image(my_game.directory("assets/backgrounds-1-test.png")))
    global_assets["backgrounds"].append(resources.Image(my_game.directory("assets/backgrounds-2-test.png")))
    global_assets["backgrounds"].append(resources.Image(my_game.directory("assets/backgrounds-3-test.png")))
    global_assets["backgrounds"].append(resources.Image(my_game.directory("assets/backgrounds-4-test.png")))

    player_idle_animation_r = [[global_assets["tile_maps"][0].grid[0][3], global_assets["tile_maps"][0].grid[0][4]]]
    global_assets["animations"]["player"]["idle_r"] = resources.Animation(player_idle_animation_r, 0, 1)

    player_idle_animation_l = [[global_assets["tile_maps"][0].grid[0][5], global_assets["tile_maps"][0].grid[0][6]]]
    global_assets["animations"]["player"]["idle_l"] = resources.Animation(player_idle_animation_l, 0, 1)

    player_run_animation_r = [[global_assets["tile_maps"][0].grid[1][3], global_assets["tile_maps"][0].grid[1][4]]]
    global_assets["animations"]["player"]["run_r"] = resources.Animation(player_run_animation_r, 0, 1)

    player_run_animation_l = [[global_assets["tile_maps"][0].grid[1][5], global_assets["tile_maps"][0].grid[1][6]]]
    global_assets["animations"]["player"]["run_l"] = resources.Animation(player_run_animation_l, 0, 1)

    player_idle_animation = [[global_assets["tile_maps"][0].grid[0][3], global_assets["tile_maps"][0].grid[1][3]]]
    global_assets["animations"]["player"]["none"] = resources.Animation(player_idle_animation, 0, 1)

    settings_scene = settings.Settings(my_game)

    menu.Menu(my_game, settings_scene)
    
    one_story_level = ingame_level_play.Level(my_game, settings_scene, global_assets)
    
    level_map.Levels(my_game, one_story_level)

    one_player_level = player_level_play.Level(my_game, settings_scene, global_assets)

    editor = level_editor.LevelEditor(my_game, global_assets)

    editor_menu.PlayerLevels(my_game, one_player_level, editor)

    settings_scene.addFPSToScenes()


    my_game.scenes.current_scene = "menu"


    def global_input(event):
        pass

    def test():
        
        pass

    my_game.run(test, global_input = global_input)

if __name__ == "__main__":
    run()