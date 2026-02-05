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

scene = nodes.scene()

def player(scene, screen, screen_size, size, color = [255, 0, 0]):
    player_node = nodes.parentNode(scene, screen, screen_size, physics_layer = 1, position_str = "center")
    player_block = nodes.block(player_node, size, color = color)
    player_colidor = nodes.hitBox(player_node, size)
    player_movement = nodes.moveInput(player_node)

level_ground = nodes.parentNode(scene, screen, screen_size, physics_layer = 2)
level_blocks = []
level_colidors = []

for i in range(5):
    size = (screen_size[1] // 20, screen_size[1] // 20)
    offset = (i * size[0] * 2, 0)
    level_colidors.append(nodes.hitBox(level_ground, size, offset = offset))
    level_blocks.append(nodes.block(level_ground, size, color = [0, 0, 255], offset = offset))

level_modifier = nodes.moveMouse(level_ground)

player(scene, screen, screen_size, (50, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:
            scene.event(event)

    screen.fill((20, 70, 40))

    scene.draw()

   
    clock.tick(120)
    pygame.display.flip()