import pygame
import nodes

pygame.init()
pygame.font.init()

# ----- Pygame setup ----- #

pygame.display.set_caption("Level test")

main_text = pygame.font.SysFont('Arial', 50)
secondary_font = pygame.font.SysFont('Arial', 30)

screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# --- Level-- #

scene = nodes.scene(screen, screen_size)

print(5.9 // 3)

grid = nodes.levelGrid(scene, 50)

grid.ground(physics_layer = 1)


level_ground = nodes.parentNode(scene, physics_layer = 1, position=(4, 4))
level_blocks = []
level_colidors = []

for i in range(36):
    size = (screen_size[1] // 20, screen_size[1] // 20)
    offset = (i * size[0], 18 * size[1])
    level_colidors.append(nodes.hitBox(level_ground, size, offset = offset, can_leave_window = True))
    level_blocks.append(nodes.block(level_ground, size, color = [0, 0, 255], offset = offset))


for i in range(13):
    size = (screen_size[1] // 20, screen_size[1] // 20)
    offset = (2 * (i + 2) * size[0], (15 - i) * size[1])
    level_colidors.append(nodes.hitBox(level_ground, size, offset = offset, can_leave_window = True))
    level_blocks.append(nodes.block(level_ground, size, color = [0, 0, 255], offset = offset))

level_modifier = nodes.moveMouse(level_ground)


player_node = nodes.parentNode(scene, physics_layer = 5)
player_node.collisionBlock((50, 50), color = [0, 255, 0])

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