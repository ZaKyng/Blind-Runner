import os
import pygame
#import new_nodes
from pygame import Vector2
from ZaKnode import *
from .lib import lib
from .lib.scenes import menu
from .lib.scenes import level
from .lib.scenes import levels
from .lib.scenes import level_editor
from .lib.scenes import settings

# ----- Pygame setup ----- #
def run():
    screen_size = (1980, 1080)
    my_game = nodes.Game(screen_size, __file__, fps = 240, screen_ratio = 16/9, overflow_hidden = True)

    my_game.fonts.addFont("main", my_game.directory("assets/starfish_font.ttf"), 4)

    menu.Menu(my_game)
    
    one_level = level.Level(my_game)
    
    level_map = levels.Levels(my_game, one_level)

    level_editor.PlayerLevels(my_game)

    settings_scene = settings.Settings(my_game)

    settings_scene.addFPSToScenes()


    def global_input(event):
        pass

    def test():
        
        pass

    my_game.run(test, global_input = global_input)

if __name__ == "__main__":
    run()