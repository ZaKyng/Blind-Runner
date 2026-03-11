import os
import pygame
from pygame import Vector2
from . import *

    



# ----- Pygame setup ----- #
def run():
    screen_size = (1980, 1080)
    my_game = nodes.Game(screen_size, fps = 120)

    bonsai = resources.LoadImage(resources.directory("img/bonsai.png"), alpha_chanel = True)

    bonsai_grid = resources.LoadImageGrid(resources.directory("img/bonsai.png"), Vector2(32, 32))

    bonsai_grow_anim = resources.Animation(bonsai_grid.grid, 0, 5)
    bonsai_color_anim = resources.Animation(bonsai_grid.grid, 5, 7)

    # --- Level-- #

    scene1 = nodes.Scene("scene1", my_game, bg_color = (200, 100, 20))
    scene2 = nodes.Scene("scene2", my_game, bg_color = (220, 0, 50))

    


    parent1 = nodes.BaseNode(scene1, offset=Vector2(150, 150))
    nodes.ShowAxis(parent1)
    block1 = nodes.ColorBlock(parent1, (80, 80), angle = 15, alpha_channel = True, offset = Vector2(10, 50))
    block1_2 = nodes.ColorBlock(parent1, (80, 80))
    #modifier1_1 = modifiers.AxisMove(block1, 0, 700, speed = 100, mode = "linear", strength = 6, show_path = True)
    modifier1_2 = modifiers.AxisMove(block1_2, 0, 700, speed = 300, mode = "ease-both", axis = "y", strength = 2)
    modifiers.MouseClickMove(block1)

    nodes.ShowAxis(block1)

    collision = nodes.CollisionArea(block1, 8)
    collision.addCollisionBlock(Vector2(20, 200), offset = Vector2(100, 100))
    modifier1_3 = modifiers.MouseDragMove(block1, 8)

    desc = nodes.TextBlock(scene1, "Dragging the green hitbox moves the block and all it's children", my_game.fonts["secondary"], offset_str="bottom", offset = Vector2(0, -120))
    desc_1 = nodes.TextBlock(scene1, "Red line shows the path of AxisMove", my_game.fonts["secondary"], offset_str="bottom", offset = Vector2(0, -80))
    desc1 = nodes.Label(scene1, "Showcase of linear and gradual interpolation on block of color", my_game.fonts["main"], offset_str="top")
    

    def scene_changing(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_game.changeScene(-1)
            elif event.key == pygame.K_DOWN:
                my_game.changeScene()

    def test():
        block1.change(angle = block1.angle + 0.2)
        return

    my_game.run(test, global_input = scene_changing)


    pygame.quit()
    exit()

if __name__ == "__main__":
    run()