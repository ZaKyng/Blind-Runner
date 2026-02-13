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

scene = nodes.scene(screen, screen_size)

parent = nodes.parentNode(scene, position_str="bottom-left")
print(parent.position)
label = nodes.label(parent, "Hello world", main_font, position_str="bottom-left")
print(label.offset)

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