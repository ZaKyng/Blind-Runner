import pygame
import nodes

pygame.init()
pygame.font.init()

# ----- Pygame setup ----- #

running = True

pygame.display.set_caption("Level test")

main_text = pygame.font.SysFont('Arial', 50)
secondary_font = pygame.font.SysFont('Arial', 30)

screen_size = (1080, 1080)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# --- Level-- #

scene = nodes.scene(screen, screen_size)

grid_num = 20

grid = nodes.levelGrid(scene, grid_num)

ground = grid.groundInit(physics_layer = 1)

nodes.moveMouse(ground)


coords1 = [
    [5, 18],
    [6, 17],
    [7, 16],
    [8, 16],
    [9, 15],
    [10, 15],
    [11, 15],
    [12, 15],
    [13, 15],
    [14, 15],
    [15, 15],
    [16, 15],
    [17, 15],
    [18, 15],
    [16, 12],
    [17, 12],
    [18, 12],
    [14, 9],
    [13, 9],
    [12, 6],
    [15, 3],
    [16, 3]
]

coords2 = [
    [0, 15],
    [3, 11],
    [0, 8],
    [5, 7],
    [6, 7],
    [7, 7],
    [8, 7],
    [12, 6],
    [15, 3],
    [16, 3]
]


grid.addGround(ground, coords1)

player_defautl_pos = [1, 18]
player = grid.player(position = player_defautl_pos, physics_check = 1)

player.collisionBlock(grid.cell_size, offset = [grid.cell_size[0] * 2, 0])
nodes.moveMouse(player)


label_parent = nodes.parentNode(scene, position = grid.gridCoordinates([5, 2]))
label = nodes.label(label_parent, "", secondary_font, position_str = "center", changable = "true")

win_count = 0
def win():
    global win_count, running
    win_count += 1
    if win_count % 2 == 1:
        grid.removeGround(ground, coords1)
        grid.addGround(ground, coords2)
        player.removeCollisionBlock([grid.cell_size[0] * 2, 0])
    else:
        player.collisionBlock(grid.cell_size, offset = [grid.cell_size[0] * 2, 0])
        grid.removeGround(ground, coords2)
        grid.addGround(ground, coords1)
    player.position = grid.gridCoordinates(player_defautl_pos)
    
    player.velocity = [0, 0]

win_area_parent = nodes.parentNode(scene, position = grid.gridCoordinates([17, 1]))
win_area_hitbox = nodes.hitBox(win_area_parent, [grid.cell_size[0], grid.cell_size[1]], show = True, can_leave_window = True)

win_area_modifier = nodes.enterCheck(win_area_parent, 5, win)


translate_test_parent = nodes.parentNode(scene, position = grid.gridCoordinates([1, 8]), physics_layer = 1)
translate_block, translate_hitBox = translate_test_parent.collisionBlock(grid.cell_size)

translate_test = nodes.translate(translate_block, "x", grid.gridCoordinates([8, 1])[0], 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene.event(event)

    screen.fill((20, 70, 40))

    label.text = "You won "+str(win_count)+" times"

    #translate_test.update()
    scene.update()
    scene.draw()
   

    clock.tick(120)
    pygame.display.flip()

pygame.quit()
exit()