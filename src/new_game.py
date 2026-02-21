import pygame
#import new_nodes
from pygame import Vector2
from ZaKgame import *


# ----- Pygame setup ----- #

screen_size = (1080, 1080)
my_game = nodes.Game(screen_size, name = "Test1", fps = 1000)

# --- Level-- #

scene1 = nodes.Scene("scene1", my_game, bg_color = (200, 100, 20))

parent = nodes.BaseNode(scene1)

block = nodes.ColorBlock(parent, (200, 60))

modifier = modifiers.AxisMove(parent, 880, axis = "x", speed = 300)
modifiery = modifiers.AxisMove(parent, 1020, axis = "y", speed = 300)

def test():
    print(parent.offset)

my_game.run(test)


pygame.quit()
exit()