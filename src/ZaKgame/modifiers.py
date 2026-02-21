import pygame
from pygame import Vector2

from .base import *


default_speed = 200



# ----------- Modifiers ------------ #

# -- Position changers -- #


# - Constant - #

class AxisMove(Modifier):
    def __init__(self, parentNode, start, end = None, axis = "x", speed = default_speed):
        super().__init__(parentNode)

        axis_arr = {
            "x" : 0,
            "y" : 1
        }

        self.axis = axis_arr.get(axis.lower(), 0)
        self.direction = 1

        if end is None:
            end = self.parentNode.offset[self.axis]
        
        if start > end:
            self.start = end
            self.end = start
        else:
            self.start = start
            self.end = end



        self.speed = speed


    def event(self, event):
        super().event(event)
    
    def update(self):
        self.parentNode.offset[self.axis] += self.speed * self.game.delta * self.direction
        if self.parentNode.offset[self.axis] >= self.end:
            self.parentNode.offset[self.axis] = self.end
            self.direction *= -1
        elif self.parentNode.offset[self.axis] <= self.start:
            self.parentNode.offset[self.axis] = self.start
            self.direction *= -1
        #print(self.direction)
        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()


# - Mouse - #

class MouseClickMove(Modifier):
    def __init__(self, parentNode):
        super().__init__(parentNode)
    

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            self.parentNode.offset = mouse_pos - self.parentNode.parentNode.position
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()


# - Keyboard - #

class KeyboardMove(Modifier):
    def __init__(self, parentNode, speed, leave_window):
        super().__init__(parentNode)

        self.speed = speed

        self.leave_window = leave_window


    def event(self, event):
        super().event(event)
    
    def update(self, direction):
        if direction.length_squared() > 0:
            direction = direction.normalize()

        velocity = direction * self.speed * self.game.delta
        self.parentNode.offset += velocity

        if not self.leave_window:
            max_x = self.game.screen_size[0] - self.parentNode.size.x
            max_y = self.game.screen_size[1] - self.parentNode.size.y

            self.parentNode.offset.x = max(0, min(max_x, self.parentNode.offset.x))
            self.parentNode.offset.y = max(0, min(max_y, self.parentNode.offset.y))

        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()

class KeyboardArrowsMove(KeyboardMove):
    def __init__(self, parentNode, speed = default_speed, leave_window = False):
        super().__init__(parentNode, speed = speed, leave_window = leave_window)


    def event(self, event):
        super().event(event)
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        direction = Vector2(0, 0)
        direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        super().update(direction)

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()

class KeyboardWASDMove(KeyboardMove):
    def __init__(self, parentNode, speed = default_speed, leave_window = False):
        super().__init__(parentNode, speed = speed, leave_window = leave_window)


    def event(self, event):
        super().event(event)
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        direction = Vector2(0, 0)
        direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        direction.y = keys[pygame.K_s] - keys[pygame.K_w]

        super().update(direction)

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()
    
        
