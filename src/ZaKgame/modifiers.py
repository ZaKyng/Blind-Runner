import pygame
from pygame import Vector2

from .base import *

# ----- Modifiers ----- #

class MouseClick(Modifier):
    def __init__(self, parentNode):
        super().__init__(parentNode)
    

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.parentNode.offset = pygame.mouse.get_pos()
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()

class KeyboardMove(Modifier):
    def __init__(self, parentNode, speed = 20):
        super().__init__(parentNode)

        self.velocity = Vector2(0, 0)
        self.speed = speed
    

    def event(self, event):
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            i = 1 if event.type == pygame.KEYDOWN else -1
            speed = self.speed * i
            if event.key == pygame.K_LEFT:
                self.velocity.x += -speed
            elif event.key == pygame.K_RIGHT:
                self.velocity.x += speed
            elif event.key == pygame.K_UP:
                self.velocity.y += -speed
            elif event.key == pygame.K_DOWN:
                self.velocity.y += speed
        super().event(event)
    
    def update(self):
        self.parentNode.offset += self.velocity
        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()