import os
import pygame
from pygame import Vector2
from . import *

    

def directory(src):
    return os.path.join(os.path.dirname(__file__), src)


# ----- Pygame setup ----- #
def run():
    screen_size = (1480, 1080)
    my_game = nodes.Game(screen_size, name = "Test1", fps = 120)

    bonsai = resources.LoadImage(directory("img/bonsai.png"), alpha_chanel = True)

    bonsai_grid = resources.LoadImageGrid(directory("img/bonsai.png"), Vector2(32, 32))

    bonsai_grow_anim = resources.Animation(bonsai_grid.grid, 0, 5)
    bonsai_color_anim = resources.Animation(bonsai_grid.grid, 5, 7)

    # --- Level-- #

    default = nodes.Scene("default", my_game)
    scene1 = nodes.Scene("scene1", my_game, bg_color = (200, 100, 20))
    scene2 = nodes.Scene("scene2", my_game, bg_color = (20, 200, 100))
    scene3 = nodes.Scene("scene3", my_game, bg_color = (100, 20, 200))
    scene4 = nodes.Scene("scene4", my_game, bg_color = (200, 20, 100))
    scene5 = nodes.Scene("scene5", my_game, bg_color = (60, 50, 60))

    desc1 = nodes.Label(default, "Use <- / -> to switch scenes", my_game.fonts["main"], offset_str="center")

    

    parent1 = nodes.BaseNode(scene1, offset=Vector2(150, 150))
    block1 = nodes.ColorBlock(parent1, (80, 80))
    block1_2 = nodes.ColorBlock(parent1, (80, 80))
    modifier1_1 = modifiers.AxisMove(block1, 0, 700, speed = 100, mode = "linear", strength = 6, show_path = True)
    modifier1_2 = modifiers.AxisMove(block1_2, 0, 700, speed = 300, mode = "ease-in", axis = "y", strength = 2)

    collision = nodes.CollisionArea(block1, 8, True)
    collision.addRect(Vector2(20, 200), offset = Vector2(100, 100))
    modifier1_3 = modifiers.MouseDragMove(block1, 8)

    desc = nodes.TextBlock(scene1, "Dragging the green hitbox moves the block and all it's children", my_game.fonts["secondary"], offset_str="bottom", offset = Vector2(0, -120))
    desc_1 = nodes.TextBlock(scene1, "Red line shows the path of AxisMove", my_game.fonts["secondary"], offset_str="bottom", offset = Vector2(0, -80))
    desc1 = nodes.Label(scene1, "Showcase of linear and gradual interpolation on block of color", my_game.fonts["main"], offset_str="top")
    

    parent2 = nodes.BaseNode(scene2, offset_str = "CenTer")
    block2 = nodes.SpriteBlock(parent2, (250, 250), bonsai.image, offset_str = "center")
    modifier2 = modifiers.KeyboardWASDMove(parent2, 320)

    desc2 = nodes.TextBlock(scene2, "Image loading and move with WASD", my_game.fonts["main"], offset_str="top", txt_color = (0, 0, 0), bg_color = (255, 255, 255), padding = 25, zindex = 2)


    parent3 = nodes.BaseNode(scene3, offset_str = "center", offset = Vector2(250, 0), zindex = -1)
    block3 = nodes.AnimatedSpriteBlock(parent3, (250, 250), bonsai_grow_anim.frames, 1.5, offset_str = "center")
    modifier3 = modifiers.MouseClickMove(parent3)

    desc3 = nodes.TextBlock(scene3, "2 animations from once loaded tilemap image", my_game.fonts["secondary"], offset_str = "top", txt_color = (0, 0, 0), bg_color = (255, 255, 255), padding = 15)
    desc4 = nodes.TextBlock(scene3, "Sorted by z-index and 1 moves on mouse click", my_game.fonts["secondary"], offset_str = "top", offset = Vector2(0, 120), txt_color = (200, 200, 240), bg_color = (12, 12, 12), padding = 25)

    parent4 = nodes.BaseNode(scene3, offset_str = "center", offset = Vector2(-250, 0))
    block4 = nodes.AnimatedSpriteBlock(parent4, (250, 250), bonsai_color_anim.frames, 3, offset_str = "center")

    parent5 = nodes.BaseNode(scene4)
    block5 = nodes.TileMapBlock(parent5, (250, 250), bonsai_grid, [1, 1])
    modifier5 = modifiers.LinearMove(parent5, Vector2(100, 130), Vector2(800, 540))

    press = modifiers.Press(scene4, pygame.K_a, lambda: block5.change(changer = [0, 1]))
    press = modifiers.Press(scene4, pygame.K_s, lambda: block5.change(changer = [1, 0]))
    press = modifiers.Press(scene4, pygame.K_d, lambda: block5.change(changer = 1))

    desc5_1 = nodes.TextBlock(scene4, "Press A, S or D to change", my_game.fonts["secondary"], (255, 200, 255), (25, 25, 25), padding = 18, offset = Vector2(130, 20))
    desc5 = nodes.Label(scene4, "Translation of one tile of a tilemap \nfrom 1 point to another", my_game.fonts["main"], (220, 240, 190), offset = Vector2(130, 900))


    tile5 = nodes.TileMapBlock(scene5, Vector2(220, 280), bonsai_grid, [0, 0], offset_str = "center")
    collision_tile5 = nodes.CollisionArea(tile5, 2, show = True)
    collision_tile5.addRect(tile5.size, offset_str = "left")
    modifiers.ClickOn(tile5, 2, lambda: tile5.change(changer = 1))
    desc6 = nodes.Label(scene5, "Click on picture to change", my_game.fonts["main"], (110, 100, 255), offset_str = "bottom")


    press_global = []
    for scene in list(my_game.scenes.values()):
        press_global.append(modifiers.Press(scene, pygame.K_RIGHT, lambda: my_game.changeScene()))
        press_global.append(modifiers.Press(scene, pygame.K_LEFT, lambda: my_game.changeScene(-1)))

    def scene_changing(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_game.changeScene(-1)
            elif event.key == pygame.K_DOWN:
                my_game.changeScene()

    def test():
        #print(parent.offset)
        return

    my_game.run(test, global_input = scene_changing)


    pygame.quit()
    exit()

if __name__ == "__main__":
    run()