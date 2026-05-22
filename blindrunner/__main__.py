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

    my_game.fonts.addFont("main", my_game.directory("assets/starfish_font.ttf"), 4)

    settings_scene = settings.Settings(my_game)

    menu.Menu(my_game, settings_scene)
    
    one_story_level = ingame_level_play.Level(my_game, settings_scene)
    
    level_map.Levels(my_game, one_story_level)

    one_player_level = player_level_play.Level(my_game, settings_scene)

    editor = level_editor.LevelEditor(my_game)

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