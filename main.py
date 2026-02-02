import pygame
import nodes

pygame.init()
pygame.font.init()

# ----- Pygame setup ----- #

pygame.display.set_caption("School project")

main_text = pygame.font.SysFont('Arial', 50)
secondary_font = pygame.font.SysFont('Arial', 30)

screen_size = (720, 720)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# --- Menu config -- #

label = nodes.parentNode(screen, screen_size, x=100, y=100)
label_text = nodes.label(label, "This is a label", secondary_font, padding=20 ,position="center")
label_hitbox = nodes.hitBox(label, label_text.size[0], label_text.size[1], position="center")
label_flexible = nodes.mouseMove(label)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:
            label_flexible.event(event)

    screen.fill((20, 70, 40))

    label.draw()

   
    clock.tick(100)
    pygame.display.flip()

