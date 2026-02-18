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

scene = nodes.Scene(screen, screen_size)

parent = nodes.BaseNode(scene)

block = nodes.ColorBlock(parent, Vector2(200, 200))

imageGrid = resources.LoadImageGrid("src/img/bonsai.png", Vector2(32, 32))

animation = resources.Animation(imageGrid.grid, 0, 5)

sprite = nodes.AnimatedSpriteBlock(parent, Vector2(200, 200), animation.frames, 40, offset = Vector2(0, 200))

move = modifiers.MouseClick(parent)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene.event(event)

    screen.fill((20, 70, 40))

    scene.update()
    scene.draw()

    clock.tick(120)
    pygame.display.flip()

pygame.quit()
exit()