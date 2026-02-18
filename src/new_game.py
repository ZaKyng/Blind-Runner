import pygame
import nodes
from pygame import Vector2

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

parent = nodes.BaseNode(scene, offset_str="center")

image = nodes.SpriteBlock(parent, Vector2(200, 200), "src/img/bonsai.png")

image2 = nodes.TilemapBlock(parent, Vector2(200, 200), "src/img/bonsai.png", Vector2(32, 32), Vector2(0, 2), offset = Vector2(300, 0))

image3 = nodes.AnimatedSpriteBlock(parent, Vector2(200, 200), "src/img/bonsai.png", Vector2(32, 32), 0, 7, 40, offset = Vector2(0, 300))

"""colorBlock = nodes.ColorBlock(parent, [80, 200], color = [255, 0, 0], offset_str="center")
colorBlock2 = nodes.ColorBlock(colorBlock, [20, 100], color = [0, 255, 0, 80], offset_str="left", changable = False)
colorBlock3 = nodes.ColorBlock(colorBlock2, [10, 40], color = [0, 0, 255], offset_str="center")
colorBlock4 = nodes.ColorBlock(colorBlock3, [5, 5], color = [255, 0, 255], offset_str="top")


modifier2 = nodes.KeayboardMove(colorBlock2, speed = 8)"""
modifier = nodes.MouseClick(parent)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                colorBlock4.kill()
            if event.key == pygame.K_a:
                colorBlock2.size = pygame.Vector2(50, 200)
                colorBlock2.color = pygame.Color(255, 255, 0, 120)"""
        scene.event(event)

    screen.fill((20, 70, 40))

    scene.update()
    scene.draw()

    clock.tick(120)
    pygame.display.flip()

pygame.quit()
exit()