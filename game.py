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

for i in range(300):
    size = (screen_size[1] // 20, screen_size[1] // 20)
    offset_x = i * (screen_size[1] // 20) % screen_size[1]
    offset_y = i // 20 * (screen_size[1] // 20)
    color = [i*8 % 256, (0 + i*15) % 256, (100 + i*5) % 256]
    level_ground.rect_list.append(nodes.addWorldBlock(level_ground, size, 
    color, offset_x=offset_x, offset_y=offset_y))

level_modifier = nodes.moveMouse(level_ground)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:
            level_ground.event(event)

    screen.fill((20, 70, 40))

    level_ground.draw()

   
    clock.tick(120)
    pygame.display.flip()

