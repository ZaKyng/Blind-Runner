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

print(5.9 // 3)

grid = nodes.levelGrid(scene, 8)

grid.ground(physics_layer = 1)

grid_modifier = nodes.moveMouse(grid.level)


player_node = nodes.parentNode(scene, physics_layer = 5, position = [grid.cell_size[0] // 2, grid.cell_size[1] // 2])
player_node.collisionBlock(grid.cell_size, color = [0, 255, 0])

nodes.playerMove(player_node, 1)

player_mouse = nodes.moveMouse(player_node)

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