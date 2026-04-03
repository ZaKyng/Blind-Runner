import os
import pygame
#import new_nodes
from pygame import Vector2
from ZaKnode import *
from .lib import lib
from .lib.scenes import menu
from .lib.scenes import level
from .lib.scenes import levels
from .lib.scenes import settings

# ----- Pygame setup ----- #
def run():
    screen_size = (1980, 1080)
    my_game = nodes.Game(screen_size, __file__, fps = 240, screen_ratio = 16/9, over_flow_hidden = True)

    my_game.fonts.addFont("main", my_game.directory("assets/starfish_font.ttf"), 4)

    menu.Menu(my_game)
    
    one_level = level.Level(my_game)
    lib.ButtonText(my_game.scenes.scenes["level"], "Back", "main", lambda: my_game.scenes.changeScene("levels"), offset_str = "bottom-left")
    
    level_map = levels.Levels(my_game, one_level)
    lib.ButtonText(my_game.scenes.scenes["levels"], "Back", "main", lambda: my_game.scenes.changeScene("menu"), offset_str = "bottom-left")

    settings_scene = settings.Settings(my_game)
    lib.ButtonText(my_game.scenes.scenes["settings"], "Back", "main", lambda: my_game.scenes.changeScene("menu"), offset_str = "bottom-left")

    settings_scene.addFPSToScenes()


    def global_input(event):
        pass

    def test():
        
        pass

    my_game.run(test, global_input = global_input)

if __name__ == "__main__":
    run()