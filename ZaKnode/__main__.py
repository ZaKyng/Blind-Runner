import os
import pygame
from pygame import Vector2
from . import *

    



# ----- Pygame setup ----- #
def run():
    screen_size = (1980, 1080)
    my_game = nodes.Game(screen_size, fps = 120)

    bonsai = resources.LoadImage(resources.directory("img/bonsai.png"), alpha_channel = True)

    bonsai_grid = resources.LoadImageGrid(resources.directory("img/bonsai.png"), Vector2(32, 32))

    bonsai_grow_anim = resources.Animation(bonsai_grid.grid, 0, 5)
    bonsai_color_anim = resources.Animation(bonsai_grid.grid, 5, 7)

    box = resources.LoadImage(resources.directory("img/box.png"), True)

    # --- Level-- #

    default = nodes.Scene("default", my_game)
    scene1 = nodes.Scene("scene1", my_game, bg_color = (200, 100, 20))
    scene2 = nodes.Scene("scene2", my_game, bg_color = (20, 200, 100))
    scene3 = nodes.Scene("scene3", my_game, bg_color = (200, 20, 100))
    scene4 = nodes.Scene("scene4", my_game, bg_color = (100, 20, 200))
    scene5 = nodes.Scene("scene5", my_game, bg_color = (60, 50, 60)) 
    scene6 = nodes.Scene("scene6", my_game, bg_color = (200, 190, 20))
    scene7 = nodes.Scene("scene7", my_game, bg_color = (12, 5, 9))

    nodes.ShowAxis(default)

    desc1 = nodes.Label(default, "Use <- / -> to switch scenes", my_game.fonts["main"], offset_str="center")
    press_esc = nodes.Label(default, "Press ESC to leave", my_game.fonts["secondary"], offset_str="bottom-right")


    parent1 = nodes.BaseNode(scene1, offset=Vector2(150, 150))
    block1 = nodes.ColorBlock(parent1, (80, 80), (170, 200, 20, 90), alpha_channel = True)
    block1_2 = nodes.ColorBlock(parent1, (80, 80))
    modifier1_1 = modifiers.AxisMove(block1, 0, 700, speed = 100, mode = "linear", strength = 6, show_path = True)
    modifier1_2 = modifiers.AxisMove(block1_2, 0, 700, speed = 300, mode = "ease-both", strength = 20, looping = False)

    modifier1_2.change(axis = "y")

    nodes.ShowAxis(block1)

    collision = nodes.CollisionArea(block1, 8)
    collision.addCollisionBlock(Vector2(20, 200), offset = Vector2(100, 100))
    modifier1_3 = modifiers.MouseDragMove(block1, 8)

    desc = nodes.TextBlock(scene1, "Dragging the green hitbox moves the block and all it's children", my_game.fonts["secondary"], offset_str="bottom", offset = Vector2(0, -120))
    desc_1 = nodes.TextBlock(scene1, "Red line shows the path of AxisMove", my_game.fonts["secondary"], offset_str="bottom", offset = Vector2(0, -80))
    desc1 = nodes.Label(scene1, "Showcase of linear and gradual interpolation on block of color", my_game.fonts["main"], offset_str="top")
    

    parent2 = nodes.BaseNode(scene2, offset_str = "CenTer")
    block2 = nodes.SpriteBlock(parent2, (250, 250), bonsai.image, offset_str = "center")
    nodes.ShowAxis(parent2)
    nodes.ShowAxis(block2)
    modifier2 = modifiers.KeyboardWASDMove(parent2, 320)

    desc2 = nodes.TextBlock(scene2, "Image loading and move with WASD", my_game.fonts["main"], offset_str="top", txt_color = (0, 0, 0), bg_color = (255, 255, 255), padding = 25, zindex = 2)


    parent3 = nodes.BaseNode(scene3, offset_str = "center", offset = Vector2(250, 0), zindex = -1)
    block3 = nodes.AnimatedSpriteBlock(parent3, (250, 250), bonsai_grow_anim.frames, 1.5, offset_str = "center")
    modifier3 = modifiers.MouseClickMove(parent3)

    desc3 = nodes.TextBlock(scene3, "2 animations from once loaded tilemap image", my_game.fonts["secondary"], offset_str = "top", txt_color = (0, 0, 0), bg_color = (255, 255, 255), padding = 15)
    desc4 = nodes.TextBlock(scene3, "Sorted by z-index and 1 moves on mouse click", my_game.fonts["secondary"], offset_str = "top", offset = Vector2(0, 120), txt_color = (200, 200, 240), bg_color = (12, 12, 12), padding = 25, zindex = -1)

    parent4 = nodes.BaseNode(scene3, offset_str = "center", offset = Vector2(-250, 0))
    block4 = nodes.AnimatedSpriteBlock(parent4, (250, 250), bonsai_color_anim.frames, 3, offset_str = "center")

    parent5 = nodes.BaseNode(scene4)
    block5 = nodes.TileMapBlock(parent5, (250, 250), bonsai_grid, [1, 1])
    modifier5 = modifiers.LinearMove(parent5, Vector2(100, 130), Vector2(800, 540))

    explain_text = nodes.Label(scene4, "Explanation: ", my_game.fonts["secondary"], (200, 200, 200), 8, offset_str = "top-right", offset = Vector2(-20, 20))
    explain = nodes.SpriteBlock(scene4, Vector2(300, 300), bonsai.image, 5, offset_str = "top-right", offset = Vector2(-20, 20 + explain_text.size.y))
    explain_box = nodes.SpriteBlock(explain, explain.size // 3, box.image, 6)
    

    modifiers.ForeverDo(explain_box, lambda: explain_box.change(offset = Vector2(explain_box.size[0] * block5.coords[0], explain_box.size[1] * block5.coords[1])))

    press = modifiers.Press(scene4, pygame.K_a, lambda: block5.change(coords_change = [0, 1]))
    press = modifiers.Press(scene4, pygame.K_s, lambda: block5.change(coords_change = [1, 0]))
    press = modifiers.Press(scene4, pygame.K_d, lambda: block5.change(coords_change = 1))

    desc5_1 = nodes.TextBlock(scene4, "Press A, S or D to change", my_game.fonts["secondary"], (255, 200, 255), (25, 25, 25), padding = 18, offset = Vector2(130, 20))
    desc5 = nodes.Label(scene4, "Translation of one tile of a tilemap \nfrom 1 point to another", my_game.fonts["main"], (220, 240, 190), offset = Vector2(130, 900))


    tile5 = nodes.TileMapBlock(scene5, Vector2(400, 500), bonsai_grid, [0, 0], offset_str = "center")
    collision_tile5 = nodes.CollisionArea(tile5, 2, show_self = True)
    collision_tile5.change(show = True)
    collision_tile5.addCollisionBlock(tile5.size, offset = Vector2(100, 200))
    modifiers.ClickOn(tile5, 2, lambda: tile5.change(coords_change = 1))
    drag = modifiers.MouseDragMove(tile5, 2)
    desc6 = nodes.Label(scene5, "Click on green area (hitbox) to change image", my_game.fonts["main"], (110, 100, 255), offset_str = "bottom")

    parent6 = nodes.BaseNode(scene6)
    nodes.ShowAxis(parent6)
    nodes.ColorBlock(parent6, Vector2(100, 100), pygame.Color(0, 0, 240), offset_str = "center")
    circle = modifiers.CircularMove(parent6, Vector2(my_game.screen_size) // 2, radius = 350, speed = 50, clockwise = False, start_deg = 180, show_path = True)

    

    modifiers.Press(scene6, pygame.K_g, lambda: circle.change(speed = circle.speed + 10))
    modifiers.Press(scene6, pygame.K_h, lambda: circle.change(speed = circle.speed - 10))
    modifiers.Press(scene6, pygame.K_j, lambda: circle.change(clockwise = circle.direction == 1))

    nodes.TextBlock(scene6, "Move block with axis and move its modifiers with it", my_game.fonts["secondary"], txt_color = (210, 100, 255), padding = 20, offset_str = "Top")
    nodes.Label(scene6, "Press G, H or J to change ", my_game.fonts["main"], (10, 80, 55), offset_str = "bottom")


    block_size = 2
    for i in range(int(my_game.screen_size.x) // block_size):
        new_block = nodes.ColorBlock(scene7, Vector2(block_size, block_size), color = (255 / (my_game.screen_size.x // block_size) * i, 255 / (my_game.screen_size[0] // block_size) * i / 2, 255), offset = Vector2(i * block_size, 200))
        modifiers.AxisMove(new_block, my_game.screen_size.y - block_size - 200, axis = "y", mode = "ease-both", speed = 300 + i, strength = 1.5)

    nodes.Label(scene7, f"{my_game.screen_size.x // block_size} blocks with different speeds", my_game.fonts["main"], (10, 80, 55), offset_str = "bottom")

    press_global = []
    for scene in list(my_game.scenes.values()):
        press_global.append(modifiers.Press(scene, pygame.K_RIGHT, lambda: my_game.changeScene()))
        press_global.append(modifiers.Press(scene, pygame.K_LEFT, lambda: my_game.changeScene(-1)))
        if press_esc not in scene.children:
            scene.addChild(press_esc)

    def scene_changing(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_game.changeScene(-1)
            elif event.key == pygame.K_DOWN:
                my_game.changeScene()

    def test():
        pass

    my_game.run(test, global_input = scene_changing)


    pygame.quit()
    exit()

if __name__ == "__main__":
    run()