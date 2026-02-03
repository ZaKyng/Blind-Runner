import pygame
import random


pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Consolas', 30)

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

player = pygame.Rect(200, 200, 50, 50) # pygame.Rect((200, 200), (50, 50))
platforms = []
platforms.append(pygame.Rect(0, height-20, width, 20))
platforms.append(pygame.Rect(200, 500, 200, 20))
platforms.append(pygame.Rect(600, 350, 250, 20))


stars = []
star_size = 5


for i in range(10):
    star_x = random.randint(0, width - star_size)
    star_y = random.randint(0, height - 100 - star_size)
    new_star = pygame.Rect(star_x, star_y, star_size, star_size)
    while pygame.Rect.collidelist(new_star, platforms) != -1:
        star_x = random.randint(0, width - star_size)
        star_y = random.randint(0, height - 100 - star_size)
        new_star = pygame.Rect(star_x, star_y, star_size, star_size)
    stars.append([new_star, True])

score_count = 0

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

    for star in stars:
        if star[1] and player.colliderect(star[0]):
            star[1] = False
            score_count += 1

    for collider in platforms:
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

    for collider in platforms:
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

    score = my_font.render(f'score: {score_count}', True, (0, 0, 255))
    text_surface = my_font.render(f'{mouse_pos}', True, (0, 255, 0))
    last_time_text = my_font.render(f'{last_time}', True, (0, 255, 0))
    delta_time_text = my_font.render(f'{delta_time}', True, (0, 255, 0))

    # screen.fill("purple")
    screen.fill((0, 0, 0))

    screen.blit(score, (100, 100))
    screen.blit(text_surface, (100, 150))
    screen.blit(last_time_text, (100, 200))
    screen.blit(delta_time_text, (100, 250))


    for i in range(len(platforms)):
        pygame.draw.rect(screen, (i * 20, 100 + i * 10, 255 - i * 10), platforms[i])

    pygame.draw.rect(screen, (255, 255, 255), player)
    for star in stars:
        if star[1]:
            pygame.draw.rect(screen, (255, 255, 0), star[0])
    
    pygame.display.flip() # pygame.display.update()
    clock.tick(120)

pygame.quit()