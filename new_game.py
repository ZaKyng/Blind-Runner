import pygame
import nodes

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
colorBlock = nodes.ColorBlock(parent, [80, 200], color = [255, 0, 0], offset_str="center")
colorBlock2 = nodes.ColorBlock(colorBlock, [20, 100], color = [0, 255, 0], offset_str="left")
colorBlock3 = nodes.ColorBlock(colorBlock2, [10, 40], color = [0, 0, 255], offset_str="center")
colorBlock4 = nodes.ColorBlock(colorBlock3, [5, 5], color = [255, 0, 255], offset_str="top")

modifier = nodes.MouseClick(parent)
modifier2 = nodes.KeayboardMove(colorBlock2, speed = 8)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene.event(event)

    screen.fill((20, 70, 40))

    #translate_test.update()
    scene.update()
    scene.draw()
    

    clock.tick(120)
    pygame.display.flip()

pygame.quit()
exit()