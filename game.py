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

# --- Menu config -- #

level_ground = nodes.parentNode(screen, screen_size)
level_blocks = []
level_colidors = []

for i in range(5):
    size = (screen_size[1] // 20, screen_size[1] // 20)
    offset = (i * size[0] * 2, 0)
    level_colidors.append(nodes.hitBox(level_ground, size, offset = offset))
    level_blocks.append(nodes.block(level_ground, size, color = [0, 0, 255], offset = offset))

level_modifier = nodes.moveMouse(level_ground)

player_node = nodes.parentNode(screen, screen_size, physics_layer = 1, position_str = "center")
player_block = nodes.block(player_node, (50, 50), color = [255, 0, 0])
player_movement = nodes.moveInput(player_node)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:
            level_ground.event(event)
            player_node.event(event)

    screen.fill((20, 70, 40))

    level_ground.draw()
    player_node.draw()

   
    clock.tick(120)
    pygame.display.flip()

