import pygame


pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Consolas', 30)

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

player = pygame.Rect(200, 200, 50, 50) # pygame.Rect((200, 200), (50, 50))
platform = pygame.Rect(0, height-20, width, 20)
platform1 = pygame.Rect(200, 500, 200, 20)

colliders = [platform, platform1]

player_vel = [0, 0]

gravity = 0.2
acceleration = 0.3

last_time = pygame.time.get_ticks()
delta_time = 0

running = True
while running:
    delta_time = pygame.time.get_ticks() - last_time
    last_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)

    mouse_pos = pygame.mouse.get_pos()
    mouse_state = pygame.mouse.get_pressed()

    keys_pressed = pygame.key.get_pressed()
    # print(pygame.mouse.get_pos())
    # print(pygame.mouse.get_pressed())
    
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
        player_vel[0] = max(player_vel[0] - acceleration, -8)

    elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
        player_vel[0] = min(player_vel[0] + acceleration, 8)

    else:
        if (player_vel[0] != 0):
            player_vel[0] -= player_vel[0] * 0.01
    
    player.x += player_vel[0]

    for collider in colliders:
        if player.colliderect(collider):
            if player_vel[0] > 0:
                player.right = collider.left
            elif player_vel[0] < 0:
                player.left = collider.right
            player_vel[0] = 0


    # --- Gravity ---
    player_vel[1] += gravity

    # --- Vertical movement ---
    player.y += player_vel[1]

    on_ground = False

    for collider in colliders:
        if player.colliderect(collider):
            if player_vel[1] > 0:
                player.bottom = collider.top
                player_vel[1] = 0
                on_ground = True
            elif player_vel[1] < 0:
                player.top = collider.bottom
                player_vel[1] = 0


    if (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP]) and on_ground:
        player_vel[1] = -12


    if mouse_state[0]:
        player.x = mouse_pos[0]
        player.y = mouse_pos[1]

    player.x = max(0, min(width - player.width, player.x))
    player.y = max(0, min(height - player.height, player.y))

    text_surface = my_font.render(f'{mouse_pos}', True, (0, 255, 0))
    last_time_text = my_font.render(f'{last_time}', True, (0, 255, 0))
    delta_time_text = my_font.render(f'{delta_time}', True, (0, 255, 0))

    # screen.fill("purple")
    screen.fill((0, 0, 0))

    screen.blit(text_surface, (100, 100))
    screen.blit(last_time_text, (100, 150))
    screen.blit(delta_time_text, (100, 200))

    
    pygame.draw.rect(screen, (50, 50, 255), platform)
    pygame.draw.rect(screen, (255, 50, 50), platform1)
    pygame.draw.rect(screen, (255, 255, 255), player)
    
    pygame.display.flip() # pygame.display.update()
    clock.tick(125)

pygame.quit()