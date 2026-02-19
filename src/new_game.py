import pygame
#import new_nodes
from pygame import Vector2
from ZaKgame import *

pygame.init()
pygame.font.init()

# ----- Pygame setup ----- #

running = True

pygame.display.set_caption("Level test")

main_font = pygame.font.SysFont('Arial', 50)
secondary_font = pygame.font.SysFont('Arial', 30)

screen_size = (1080, 1080)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# --- Level-- #

scene1 = nodes.Scene(screen, screen_size, bg_color = (200, 100, 20))

scene2 = nodes.Scene(screen, screen_size, bg_color = (120, 0, 120))

scene3 = nodes.Scene(screen, screen_size, bg_color = (0, 120, 120))


parent4 = nodes.BaseNode(scene1, zindex = 2, offset = Vector2(1, 0))

block = nodes.ColorBlock(parent4, Vector2(200, 200), color = pygame.Color(120, 0, 120))

parent = nodes.BaseNode(scene1, zindex = 3)

block = nodes.ColorBlock(parent, Vector2(200, 200))

imageGrid = resources.LoadImageGrid("src/img/bonsai.png", Vector2(32, 32))

animation = resources.Animation(imageGrid.grid, 0, 5)

sprite = nodes.AnimatedSpriteBlock(parent, Vector2(200, 200), animation.frames, 40, offset = Vector2(0, 200))

move = modifiers.MouseClick(parent)

parent5 = nodes.BaseNode(scene1, zindex = 4, offset = Vector2(1, 1))

image = resources.LoadImage("src/img/bonsai.png")

block555 = nodes.SpriteBlock(parent5, Vector2(200, 200), image.image)

inputMove = modifiers.KeayboardMove(parent5)




parent2 = nodes.BaseNode(scene2)

sprite2 = nodes.AnimatedSpriteBlock(parent2, Vector2(200, 200), animation.frames, 40)

move2 = modifiers.MouseClick(parent2)




parent3 = nodes.BaseNode(scene3)

animation2 = resources.Animation(imageGrid.grid, 5, 7)

sprite2 = nodes.AnimatedSpriteBlock(parent3, Vector2(200, 200), animation2.frames, 90)

move2 = modifiers.KeayboardMove(parent3)


index = 0

possible_scenes = [scene1, scene2, scene3]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                index += 1
                if index >= len(possible_scenes):
                    index = 0
        possible_scenes[index].event(event)

    screen.fill(possible_scenes[index].bg_color)

    possible_scenes[index].update()
    possible_scenes[index].draw()

    clock.tick(120)
    pygame.display.flip()

pygame.quit()
exit()