import pygame
#import new_nodes
from pygame import Vector2
from ZaKgame import *

pygame.init()
pygame.font.init()

# ----- Pygame setup ----- #

screen_size = (1080, 1080)
my_game = nodes.Game(screen_size)

# --- Level-- #

scene1 = nodes.Scene("scene1", my_game, bg_color = (200, 100, 20))

scene2 = nodes.Scene("scene2", my_game, bg_color = (120, 0, 120))

scene3 = nodes.Scene("scene3", my_game, bg_color = (0, 120, 120))


parent4 = nodes.BaseNode(scene1, zindex = 2, offset = Vector2(1, 0))

block = nodes.ColorBlock(parent4, Vector2(200, 200), color = pygame.Color(120, 0, 120))

parent = nodes.BaseNode(scene1, zindex = 3)

block = nodes.ColorBlock(parent, Vector2(200, 200))

imageGrid = resources.LoadImageGrid("src/img/bonsai.png", Vector2(32, 32))

animation = resources.Animation(imageGrid.grid, 0, 5)

sprite = nodes.AnimatedSpriteBlock(parent, Vector2(200, 200), animation.frames, 2, offset = Vector2(0, 200))

move = modifiers.MouseClick(parent)

parent5 = nodes.BaseNode(scene1, zindex = 4, offset = Vector2(1, 1))

image = resources.LoadImage("src/img/bonsai.png")

block555 = nodes.SpriteBlock(parent5, Vector2(200, 200), image.image)

inputMove = modifiers.KeyboardMove(parent5)




parent2 = nodes.BaseNode(scene2)

sprite2 = nodes.AnimatedSpriteBlock(parent2, Vector2(200, 200), animation.frames, 4)

move2 = modifiers.MouseClick(parent2)




parent3 = nodes.BaseNode(scene3)

animation2 = resources.Animation(imageGrid.grid, 5, 7)

sprite3 = nodes.AnimatedSpriteBlock(parent3, Vector2(200, 200), animation2.frames, 1)

move2 = modifiers.KeyboardMove(parent3)



my_game.run()