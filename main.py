import pygame
import custom_ui
import random

pygame.init()
pygame.font.init()

# ----- Pygame setup ----- #

main_text = pygame.font.SysFont('Arial', 50)
secondary_font = pygame.font.SysFont('Arial', 30)

screen_size = [720, 720]
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# --- Menu config -- #


def idk(event):
    print("Hello")
    print(event)

buttons = []

buttons.append(custom_ui.ButtonMove(screen, screen_size, "top", idk, secondary_font, padding = 12, position="top"))
buttons.append(custom_ui.ButtonMove(screen, screen_size, "bottom", idk, secondary_font, padding = 12, position="bottom"))
buttons.append(custom_ui.ButtonMove(screen, screen_size, "left side", idk, secondary_font, padding = 12, position="left"))
buttons.append(custom_ui.ButtonFix(screen, screen_size, "right side", idk, secondary_font, padding = 12, position="right"))
buttons.append(custom_ui.ButtonFix(screen, screen_size, "Im in center", idk, secondary_font, padding = 12, position="center"))
buttons.append(custom_ui.ButtonFix(screen, screen_size, "postition null", idk, secondary_font, padding = 12))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        for button in buttons:
            button.handle_event(event)

    screen.fill((20, 70, 40))
    for button in buttons:
        button.draw()
        if (button != buttons[0]):
            if (buttons[0].colideCheck(button)):
                print(button.rect)
    clock.tick(100)
    pygame.display.flip()

