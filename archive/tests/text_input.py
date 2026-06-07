import pygame

pygame.init()

screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Text Input Example")

font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

text = ""

# Start text input mode
pygame.key.start_text_input()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.TEXTINPUT:
            text += event.text  # add typed character
        

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Entered:", text)
                text = ""

    screen.fill((30, 30, 30))

    # Render text
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (20, 80))

    pygame.display.flip()
    clock.tick(60)

pygame.key.stop_text_input()
pygame.quit()