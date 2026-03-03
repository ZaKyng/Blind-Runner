import os
import pygame
#import new_nodes
from pygame import Vector2
from ZaKnode import *

def directory(src):
    return os.path.join(os.path.dirname(__file__), src)


# ----- Pygame setup ----- #
def run():
    screen_size = (1080, 1080)
    my_game = nodes.Game(screen_size, name = "Test1", fps = 120)

    bonsai = resources.LoadImage(directory("img/bonsai.png"))

    bonsai_grid = resources.LoadImageGrid(directory("img/bonsai.png"), Vector2(32, 32))

    bonsai_grow_anim = resources.Animation(bonsai_grid.grid, 0, 5)
    bonsai_color_anim = resources.Animation(bonsai_grid.grid, 5, 7)

    # --- Level-- #

    scene1 = nodes.Scene("scene1", my_game, bg_color = (200, 100, 20))
    scene2 = nodes.Scene("scene2", my_game, bg_color = (20, 200, 100))
    scene3 = nodes.Scene("scene3", my_game, bg_color = (100, 20, 200))
    scene4 = nodes.Scene("scene4", my_game, bg_color = (200, 20, 100))

    parent1 = nodes.BaseNode(scene1)
    block1 = nodes.ColorBlock(parent1, (80, 80))
    modifier1_1 = modifiers.AxisMove(parent1, 180, 900, speed = 57, mode = "linear", strength = 6)
    modifier1_2 = modifiers.AxisMove(parent1, 180, 900, speed = 300, mode = "ease-in", axis = "y", strength = 2)
    
    parent2 = nodes.BaseNode(scene2, offset_str = "CenTer")
    block2 = nodes.SpriteBlock(parent2, (250, 250), bonsai.image, offset_str = "center")
    modifier2 = modifiers.KeyboardArrowsMove(parent2, 320)

    parent3 = nodes.BaseNode(scene3, offset = Vector2(360, 540), zindex = -1)
    block3 = nodes.AnimatedSpriteBlock(parent3, (250, 250), bonsai_grow_anim.frames, 1.5, offset_str = "center")
    modifier3 = modifiers.MouseClickMove(parent3)
    parent4 = nodes.BaseNode(scene3, offset = Vector2(720, 540))
    block4 = nodes.AnimatedSpriteBlock(parent4, (250, 250), bonsai_color_anim.frames, 3, offset_str = "center")

    parent5 = nodes.BaseNode(scene4)
    block5 = nodes.TileMapBlock(parent5, (250, 250), bonsai_grid.grid, [1, 1], offset_str = "center")
    modifier5 = modifiers.LinearMove(parent5, Vector2(100, 100), Vector2(800, 540))



    def test():
        #print(parent.offset)
        return

    my_game.run(test)


    pygame.quit()
    exit()

if __name__ == "__main__":
    run()