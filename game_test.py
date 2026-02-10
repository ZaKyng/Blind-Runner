import pygame
import nodes

pygame.init()
pygame.font.init()

# ----- Pygame setup ----- #

running = True

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


label_parent = nodes.parentNode(scene, position = grid.gridCoordinates([5, 2]))
label = nodes.label(label_parent, "", secondary_font, position_str = "center", changable = "true")

win_count = 0
def win():
    global win_count, running
    win_count += 1
    print(win_count)
    label.text = "You won "+str(win_count)+" times"
    if win_count > 2:
        running = False

win_area_parent = nodes.parentNode(scene, position = grid.gridCoordinates([18, 18]))
win_area_hitbox = nodes.hitBox(win_area_parent, grid.cell_size, show = True)

win_area_modifier = nodes.enterCheck(win_area_parent, 5, win)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene.event(event)

    screen.fill((20, 70, 40))

    scene.update()
    scene.draw()

   

    clock.tick(120)
    pygame.display.flip()

pygame.quit()
exit()