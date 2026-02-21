import pygame
#import new_nodes
from pygame import Vector2
from ZaKgame import *


# ----- Pygame setup ----- #

screen_size = (1080, 1080)
my_game = nodes.Game(screen_size, name = "Test1", fps = 1000)

# --- Level-- #

scene1 = nodes.Scene("scene1", my_game, bg_color = (200, 100, 20))

parent = nodes.BaseNode(scene1, offset = Vector2(200, 540))

block = nodes.ColorBlock(parent, (120, 400), offset_str = "center")

modifier = modifiers.AxisMove(block, -100, 100, axis = "x")

my_game.run()


pygame.quit()
exit()