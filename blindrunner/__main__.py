import os
import pygame
#import new_nodes
from pygame import Vector2
from ZaKnode import *
from .lib import menu
from .lib import level
from .lib import levels

# ----- Pygame setup ----- #
def run():
    screen_size = (1980, 1080)
    my_game = nodes.Game(screen_size, __file__, fps = 256, screen_ratio = 16/9, over_flow_hidden = True)

    my_game.fonts.addFont("main", my_game.directory("assets/starfish_font.ttf"), 4)

    menu.Menu(my_game)
    one_level = level.Level(my_game)
    levels.Levels(my_game, one_level)

    for scene in list(my_game.scenes.scenes.values()):
        nodes.TextBlock(scene, "back", "main", "m", padding = 8, zindex = 1, offset_str = "bottom-right")

    def global_input(event):
        pass

    def test():
        pass

    my_game.run(test, global_input = global_input)

if __name__ == "__main__":
    run()