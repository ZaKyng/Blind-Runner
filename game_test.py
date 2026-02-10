import pygame
import nodes

pygame.init()
pygame.font.init()

# ----- Pygame setup ----- #

pygame.display.set_caption("Level test")

main_text = pygame.font.SysFont('Arial', 50)
secondary_font = pygame.font.SysFont('Arial', 30)

screen_size = (720, 720)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# --- Level-- #

scene = nodes.scene(screen, screen_size)

grid = nodes.levelGrid(scene, 20)

ground = grid.groundInit(physics_layer = 1)

player = grid.player(position = [3, 2], physics_check = 1)
nodes.moveMouse(player)


label_parent = nodes.parentNode(scene, position = [5 * grid.cell_size[0], 2 * grid.cell_size[1]])
label = nodes.label(label_parent, "Score: 0", secondary_font, position_str = "center")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        scene.event(event)

    screen.fill((20, 70, 40))

    scene.update()
    scene.draw()

   
    clock.tick(120)
    pygame.display.flip()