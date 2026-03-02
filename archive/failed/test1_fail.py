import pygame
from . import nodes1 as nodes



"""
    The game works for now, but in the furure it would be almost imposible to add new modifiers and other nodes.
    I need to rethink the node file structure and need to add z-index.
    I want to be able to add anything to anything (any modifier to any node, any node to parentNode and even to any node,
        nodes (block, hitBox) need to work more like parentNode).
    Now that I think about it, parentNode shouldn't have velocity, just position and modifiers and other nodes should 
        have velocity and on update just should change position. IDK
    Just need to rewrite the whole nodes.py again.
"""



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


translate_test_parent = nodes.parentNode(scene, position = grid.gridCoordinates([5, 7]), physics_layer = 1)
translate_block = []
translate_hitBox = []

for i in range(4):
    output = translate_test_parent.collisionBlock(grid.cell_size, offset = [i * grid.cell_size[0], 0])
    translate_block.append(output[0])
    translate_hitBox.append(output[1])


#translate_test1 = nodes.translate(translate_test_parent, "x", grid.gridCoordinates([5, 1])[0], 2)
#translate_test2 = nodes.translateLinear(translate_test_parent, "y", grid.gridCoordinates([1, 1])[1], 2)

tranlsate_test3 = nodes.translateGlobal(translate_test_parent, grid.gridCoordinates([6, 8]), grid.gridCoordinates([2, 2]), 1)

win_area_parent = nodes.parentNode(scene, position = grid.gridCoordinates([17, 1]))
win_area_hitbox = nodes.hitBox(win_area_parent, [grid.cell_size[0], grid.cell_size[1]], show = True, can_leave_window = True)

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

win_area_modifier = nodes.enterCheck(win_area_parent, 5, win)
win_area_modifier2 = nodes.moveMouse(win_area_parent)


blind_part = nodes.parentNode(scene)
blind_box = nodes.block(blind_part, screen_size, color = [0, 0, 0])

player_defautl_pos = [1, 18]
player = grid.player(position = player_defautl_pos, physics_check = 1)

player.collisionBlock(grid.cell_size, offset = [grid.cell_size[0] * 2, 0])
nodes.moveMouse(player)


label_parent = nodes.parentNode(scene, position = grid.gridCoordinates([5, 2]))
label = nodes.label(label_parent, "", secondary_font, position_str = "center", changable = "true")

win_count = 0








while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene.event(event)

    screen.fill((20, 70, 40))

    if player.velocity == [0, 0]:
        blind_box.display = False
    else:
        blind_box.display = True

    label.text = "You won "+str(win_count)+" times"

    #translate_test.update()
    scene.update()
    scene.draw()
   

    clock.tick(120)
    pygame.display.flip()

pygame.quit()
exit()