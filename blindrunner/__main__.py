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

        "levels" : {

        },

        "slider" : {

        },
    
        "animations" : [
            {
                "player" : {
                },
                "g_enemy" : {
                
                },
                "f_enemy" : {
                
                }
            },
            {
                "player" : {
                },
                "g_enemy" : {
                
                },
                "f_enemy" : {
                
                }
            },
            {
                "player" : {
                },
                "g_enemy" : {
                
                },
                "f_enemy" : {
                
                }
            },
            {
                "player" : {
                },
                "g_enemy" : {
                
                },
                "f_enemy" : {
                
                }
            }
        ],

        "music" : []
    }
    

    
    global_assets["tile_maps"].append(resources.SpriteSheet(my_game.directory("assets/final-tiles-1-test.png"), (8, 8), alpha_channel = True))
    global_assets["tile_maps"].append(resources.SpriteSheet(my_game.directory("assets/final-tiles-2-test.png"), (8, 8), alpha_channel = True))
    global_assets["tile_maps"].append(resources.SpriteSheet(my_game.directory("assets/final-tiles-3-test.png"), (8, 8), alpha_channel = True))
    global_assets["tile_maps"].append(resources.SpriteSheet(my_game.directory("assets/final-tiles-4-test.png"), (8, 8), alpha_channel = True))

    global_assets["backgrounds"].append(resources.Image(my_game.directory("assets/backgrounds-1-test.png")))
    global_assets["backgrounds"].append(resources.Image(my_game.directory("assets/backgrounds-2-test.png")))
    global_assets["backgrounds"].append(resources.Image(my_game.directory("assets/backgrounds-3-test.png")))
    global_assets["backgrounds"].append(resources.Image(my_game.directory("assets/backgrounds-4-test.png")))

    global_assets["buttons"] = resources.SpriteSheet(my_game.directory("assets/buttons2.png"), (64, 32), alpha_channel = True)

    global_assets["level_card"] = resources.Image(my_game.directory("assets/player-level-card.png"), alpha_channel = True)

    global_assets["add_button"] = resources.Image(my_game.directory("assets/add-button.png"), alpha_channel = True)

    global_assets["test_button"] = resources.Image(my_game.directory("assets/test-button.png"), alpha_channel = True)

    global_assets["arrows"] = resources.SpriteSheet(my_game.directory("assets/arrows.png"), (16, 16), alpha_channel = True)

    global_assets["fps_buttons"] = resources.SpriteSheet(my_game.directory("assets/fps-buttons.png"), (16, 8), alpha_channel = True)

    global_assets["slider"]["bg"] = resources.Image(my_game.directory("assets/slider-bg.png"), alpha_channel = True)
    global_assets["slider"]["fg"] = resources.Image(my_game.directory("assets/slider-fg.png"), alpha_channel = True)

    global_assets["levels"]["unlocked"] = resources.SpriteSheet(my_game.directory("assets/level-icons.png"), (32, 32), alpha_channel = True)
    global_assets["levels"]["locked"] = resources.SpriteSheet(my_game.directory("assets/locked-icons.png"), (32, 32), alpha_channel = True)
    global_assets["levels"]["check"] = resources.Image(my_game.directory("assets/level-check.png"), alpha_channel = True)
    global_assets["levels"]["lock"] = resources.Image(my_game.directory("assets/lock.png"), alpha_channel = True)

    for tile_set in range(4):
        global_assets["animations"][tile_set]["player"]["idle"] = {}

        player_idle_animation_r = [[global_assets["tile_maps"][tile_set].grid[0][3], global_assets["tile_maps"][tile_set].grid[0][4]]]
        global_assets["animations"][tile_set]["player"]["idle"]["right"] = resources.Animation(player_idle_animation_r, 0, 1)

        player_idle_animation_l = [[global_assets["tile_maps"][tile_set].grid[0][5], global_assets["tile_maps"][tile_set].grid[0][6]]]
        global_assets["animations"][tile_set]["player"]["idle"]["left"] = resources.Animation(player_idle_animation_l, 0, 1)

        global_assets["animations"][tile_set]["player"]["run"] = {}

        player_run_animation_r = [[global_assets["tile_maps"][tile_set].grid[1][3], global_assets["tile_maps"][tile_set].grid[1][4]]]
        global_assets["animations"][tile_set]["player"]["run"]["right"] = resources.Animation(player_run_animation_r, 0, 1)

        player_run_animation_l = [[global_assets["tile_maps"][tile_set].grid[1][5], global_assets["tile_maps"][tile_set].grid[1][6]]]
        global_assets["animations"][tile_set]["player"]["run"]["left"] = resources.Animation(player_run_animation_l, 0, 1)

        global_assets["animations"][tile_set]["player"]["jump"] = {}

        player_jump_animation_r = [[global_assets["tile_maps"][tile_set].grid[2][3]], [global_assets["tile_maps"][tile_set].grid[2][3]]]
        global_assets["animations"][tile_set]["player"]["jump"]["right"] = resources.Animation(player_jump_animation_r, 0, 1)

        player_jump_animation_l = [[global_assets["tile_maps"][tile_set].grid[2][5]], [global_assets["tile_maps"][tile_set].grid[2][5]]]
        global_assets["animations"][tile_set]["player"]["jump"]["left"] = resources.Animation(player_jump_animation_l, 0, 1)

        global_assets["animations"][tile_set]["player"]["fall"] = {}

        player_fall_animation_r = [[global_assets["tile_maps"][tile_set].grid[2][3], global_assets["tile_maps"][tile_set].grid[2][4]]]
        global_assets["animations"][tile_set]["player"]["fall"]["right"] = resources.Animation(player_fall_animation_r, 0, 1)

        player_fall_animation_l = [[global_assets["tile_maps"][tile_set].grid[2][5], global_assets["tile_maps"][tile_set].grid[2][6]]]
        global_assets["animations"][tile_set]["player"]["fall"]["left"] = resources.Animation(player_fall_animation_l, 0, 1)

        global_assets["animations"][tile_set]["player"]["finish"] = {}

        player_finish_animation_r = [[global_assets["tile_maps"][tile_set].grid[3][3], global_assets["tile_maps"][tile_set].grid[3][4], global_assets["tile_maps"][tile_set].grid[3][5], global_assets["tile_maps"][tile_set].grid[3][6]]]
        global_assets["animations"][tile_set]["player"]["finish"] = resources.Animation(player_finish_animation_r, 0, 3)



        global_assets["animations"][tile_set]["g_enemy"]["idle"] = {}

        g_enemy_idle_animation_r = [[global_assets["tile_maps"][tile_set].grid[5][1], global_assets["tile_maps"][tile_set].grid[5][1]]]
        global_assets["animations"][tile_set]["g_enemy"]["idle"]["right"] = resources.Animation(g_enemy_idle_animation_r, 0, 1)

        g_enemy_idle_animation_l = [[global_assets["tile_maps"][tile_set].grid[5][3], global_assets["tile_maps"][tile_set].grid[5][3]]]
        global_assets["animations"][tile_set]["g_enemy"]["idle"]["left"] = resources.Animation(g_enemy_idle_animation_l, 0, 1)

        global_assets["animations"][tile_set]["g_enemy"]["run"] = {}

        g_enemy_run_animation_r = [[global_assets["tile_maps"][tile_set].grid[5][1], global_assets["tile_maps"][tile_set].grid[5][2]]]
        global_assets["animations"][tile_set]["g_enemy"]["run"]["right"] = resources.Animation(g_enemy_run_animation_r, 0, 1)

        g_enemy_run_animation_l = [[global_assets["tile_maps"][tile_set].grid[5][3], global_assets["tile_maps"][tile_set].grid[5][4]]]
        global_assets["animations"][tile_set]["g_enemy"]["run"]["left"] = resources.Animation(g_enemy_run_animation_l, 0, 1)


        global_assets["animations"][tile_set]["f_enemy"]["idle"] = {}

        f_enemy_idle_animation_r = [[global_assets["tile_maps"][tile_set].grid[4][5], global_assets["tile_maps"][tile_set].grid[4][6]]]
        global_assets["animations"][tile_set]["f_enemy"]["idle"]["right"] = resources.Animation(f_enemy_idle_animation_r, 0, 1)

        f_enemy_idle_animation_l = [[global_assets["tile_maps"][tile_set].grid[5][5], global_assets["tile_maps"][tile_set].grid[5][6]]]
        global_assets["animations"][tile_set]["f_enemy"]["idle"]["left"] = resources.Animation(f_enemy_idle_animation_l, 0, 1)


    global_assets["music"].append(resources.Sound(my_game.directory("assets/test-music-1.mp3")))
    global_assets["music"].append(resources.Sound(my_game.directory("assets/test-music-2.mp3")))
    global_assets["music"].append(resources.Sound(my_game.directory("assets/test-music-3.mp3")))


    editor = level_editor.LevelEditor(my_game, global_assets)


    my_game.audio_player = lib.AudioManager(editor.scene)


    settings_scene = settings.Settings(my_game, global_assets)

    menu_node = menu.Menu(my_game, settings_scene, global_assets)
    
    one_story_level = ingame_level_play.Level(my_game, settings_scene, global_assets)
    
    level_map.Levels(my_game, one_story_level, global_assets)

    one_player_level = player_level_play.Level(my_game, settings_scene, global_assets)

    editor_menu.PlayerLevels(my_game, one_player_level, editor, global_assets)

    settings_scene.addFPSToScenes()
    
    
    

    my_game.audio_player.addMusic("music", "menu-music", global_assets["music"][0])
    my_game.audio_player.addMusic("music", "level-music", global_assets["music"][1])
    my_game.audio_player.addMusic("music", "running-music", global_assets["music"][2])

    my_game.audio_player.addMusic("sfx", "win", resources.Sound(my_game.directory("assets/victory.mp3")))
    for i in range(5):
        my_game.audio_player.addMusic("sfx", f"death{i + 1}", resources.Sound(my_game.directory(f"assets/death{i + 1}.mp3")))
        my_game.audio_player.sfx_channel.sounds[f"death{i + 1}"].changeVolume(0.7)


    my_game.scenes.current_scene = "menu"


    def global_input(event):
        pass

    not_menu = [one_story_level.name, one_player_level.name, editor.name]
    my_game.last_scene = "none"

    my_game.music_playing = "none"

    def always(my_game, global_assets=global_assets):
        current_scene = my_game.scenes.current_scene

        # 1. Handle Scene Transitions (only runs when scene changes)
        if my_game.last_scene != current_scene:
            if current_scene in not_menu:
                my_game.audio_player.stopMusic("music", "menu-music")
                my_game.audio_player.playMusic("music", "level-music")
                my_game.audio_player.playMusic("music", "running-music")
            else:
                if my_game.music_playing != "menu-music":
                    my_game.audio_player.stopMusic("music", "level-music")
                    my_game.audio_player.stopMusic("music", "running-music")
                    my_game.audio_player.playMusic("music", "menu-music")
                    my_game.music_playing = "menu-music"
            
            my_game.last_scene = current_scene

        # 2. Handle In-Game Music Toggling (runs every frame while in a level)
        if current_scene == one_story_level.name:
            target_level = one_story_level
        elif current_scene == one_player_level.name:
            target_level = one_player_level
        else:
            return # Not in a playable level, nothing more to do

        # Check cover status on every frame
        if not target_level.level.cover.active:
            if my_game.music_playing != "level-music":
                my_game.audio_player.music_channel.tracks["running-music"].changeVolume(0)
                my_game.audio_player.music_channel.tracks["level-music"].changeVolume(0.35)
                my_game.music_playing = "level-music"
        else:
            if my_game.music_playing != "running-music":
                my_game.audio_player.music_channel.tracks["running-music"].changeVolume(0.35)
                my_game.audio_player.music_channel.tracks["level-music"].changeVolume(0)
                my_game.music_playing = "running-music"



    my_game.run(lambda : always(my_game), global_input = global_input)

if __name__ == "__main__":
    run()