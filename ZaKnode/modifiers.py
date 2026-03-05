import math
import pygame
from pygame import Vector2

from .base import *


default_speed = 200



# ----------- Modifiers ------------ #

## -- Position changers -- ##


### - Constant - ###

class AxisMove(Modifier):
    def __init__(self, parentNode, start, end = None, axis = "x", mode = "linear", speed = default_speed, strength = 3, show_path = False):
        super().__init__(parentNode)
        self.show = show_path

        axis_arr = {"x" : 0, "y" : 1}

        self.axis = axis_arr.get(axis.lower(), 0)
        

        if end is None:
            end = self.parentNode.offset[self.axis]
        
        if start > end:
            self.start = end
            self.end = start
        else:
            self.start = start
            self.end = end
        
        self.speed = speed
        self.strength = abs(strength)

        self.path_len = self.end - self.start
        self.duration = self.path_len / self.speed

        self.elapsed = 0.0
        
        self.direction = 1

        self.last_offset = self.parentNode.offset[self.axis]

        modes = {
            "linear" : self.linear,
            "ease-in" : self.easeIn,
            "ease-out" : self.easeOut,
            "ease-both" : self.easeBoth,
            "ease-in-out" : self.easeBoth
        }

        self.mode = modes.get(mode, self.linear)


    def event(self, event):
        super().event(event)
    
    def update(self):
        self.elapsed += self.direction * self.game.delta

        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.direction = -1
        elif self.elapsed <= 0:
            self.elapsed = 0
            self.direction = 1
        
        percents = self.elapsed / self.duration

        self.partition = self.mode(percents, self.strength)

        new_offset = self.start + self.path_len * self.partition

        #print([self.new_offset, self.last_offset, percents, partition])

        step = new_offset - self.last_offset
        
        self.parentNode.offset[self.axis] += step
        self.last_offset = new_offset

        super().update()

    def draw(self):
        if self.show:
            center_x = self.parentNode.position.x + self.parentNode.size.x // 2
            center_y = self.parentNode.position.y + self.parentNode.size.y // 2

            if self.axis == 0:
                start = (center_x - self.path_len * (self.partition), center_y)
                end = (center_x + self.path_len * (1 - self.partition), center_y)
            else:
                start = (center_x, center_y - self.path_len * (self.partition))
                end = (center_x, center_y + self.path_len * (1 - self.partition))

            pygame.draw.line(self.game.screen, (255, 0, 0), start, end, width = 4)
        super().draw()

    def kill(self):
        super().kill()
    
    
    def linear(self, p, s):
        return p

    def easeIn(self, p, s):
        return pow(p, s)
    
    def easeOut(self, p, s):
        return 1 - pow(1 - p, s)
    
    def easeBoth(self, p, s):
        if p < 0.5:
            return pow(2, s - 1) * pow(p, s)
        else:
            return 1 - pow(-2 * p + 2, s) / 2

class LinearMove(Modifier):
    def __init__(self, parentNode, start : Vector2, end = None, mode = "linear", speed = default_speed, strength = 3, show_path = False):
        super().__init__(parentNode)
        self.show = show_path

        self.direction = 1

        if end is None:
            end = self.parentNode.offset
        
        self.start = Vector2(start)
        self.parentNode.offset = self.start
        self.end = Vector2(end)

        self.speed = abs(speed)
        self.strength = abs(strength)
        
        self.difference = self.end - self.start
        self.path_len = math.sqrt(self.difference.x ** 2 + self.difference.y ** 2)

        self.duration = self.path_len / self.speed
        self.elapsed = 0.0
        
        self.direction = 1

        self.last_offset = Vector2(0, 0)

        modes = {
            "linear" : self.linear,
            "ease-in" : self.easeIn,
            "ease-out" : self.easeOut,
            "ease-both" : self.easeBoth
        }

        self.mode = modes.get(mode, self.linear)

    
    def event(self, event):
        super().event(event)
    
    def update(self):
        self.elapsed += self.direction * self.game.delta

        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.direction = -1
        elif self.elapsed <= 0:
            self.elapsed = 0
            self.direction = 1
        
        percents = self.elapsed / self.duration

        self.partition = self.mode(percents, self.strength)

        self.new_offset = self.difference * self.partition

        step = self.new_offset - self.last_offset
        
        self.parentNode.offset += step
        self.last_offset = self.new_offset

        super().update()

    def draw(self):
        if self.show:
            center_x = self.parentNode.position.x + self.parentNode.size.x // 2
            center_y = self.parentNode.position.y + self.parentNode.size.y // 2

            start = (center_x - self.difference.x * self.partition, center_y - self.difference.y * self.partition)
            end = (center_x + self.difference.x * (1 - self.partition), center_y + self.difference.y * (1 - self.partition))
                
            pygame.draw.line(self.game.screen, (255, 0, 0), start, end, width = 4)
        super().draw()

    def kill(self):
        super().kill()
    
    
    def linear(self, p, s):
        return p

    def easeIn(self, p, s):
        return pow(p, s)
    
    def easeOut(self, p, s):
        return 1 - pow(1 - p, s)
    
    def easeBoth(self, p, s):
        if p < 0.5:
            return pow(2, s - 1) * pow(p, s)
        else:
            return 1 - pow(-2 * p + 2, s) / 2

class CircularMove(Modifier):
    def __init__(self, parentNode, relative_center, radius = None, clockwise = True, speed = default_speed, show_path = False):
        super().__init__(parentNode)

        self.show = show_path

        self.speed = speed

        if clockwise:
            self.clockwise = 0
        else:
            self.clockwise = 1

        self.center = self.parentNode.offset + Vector2(relative_center)
        if radius is None:
            difference = self.parentNode.offset - self.center
            self.radius = math.sqrt(abs(difference.x ** 2 + difference.y ** 2))
        else:
            self.radius = radius

        self.path_len = 2 * math.pi * self.radius
        self.duration = max(self.path_len / self.speed, 0.1)

        self.elapsed = 0.0

        self.last_offset = self.parentNode.offset
        

    
    def event(self, event):
        super().event(event)
    
    def update(self):
        self.elapsed += self.game.delta

        if self.elapsed >= self.duration:
            self.elapsed = self.elapsed % self.duration
        
        percents = self.elapsed / self.duration

        self.angle = 2 * math.pi * (abs(self.clockwise - percents))

        self.new_offset = Vector2(self.center.x + math.cos(self.angle) * self.radius, self.center.y + math.sin(self.angle) * self.radius)


        step = self.new_offset - self.last_offset
        
        self.parentNode.offset += step

        self.last_offset = self.new_offset

        super().update()

    def draw(self):
        if self.show:
            center = self.parentNode.offset + Vector2(math.cos(self.angle) * self.radius, math.sin(self.angle) * self.radius) * -1
            pygame.draw.circle(self.game.screen, (255, 0, 0), center, abs(self.radius), width = 4)
        super().draw()

    def kill(self):
        super().kill()


### - Mouse - ###

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

class MouseDragMove(Modifier):
    def __init__(self, parentNode, physics_layer = 1, axis = None):
        super().__init__(parentNode)

        axis_arr = {"x" : [0], "y" : [1]}

        if axis is None:
            self.axis = [0, 1]
        else:
            self.axis = axis_arr[axis]

        self.physics_check = physics_layer

        self.mouse_offset = Vector2(0, 0)
        self.mouse_clicked = False

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = Vector2(event.pos)
            for collision_area in self.parentNode.collision:
                if collision_area.physics_layer == self.physics_check:
                    for rect in collision_area.collision_blocks:
                        if rect.rect.collidepoint(mouse):
                            self.mouse_offset = self.parentNode.position - mouse
                            self.mouse_clicked = True
                            return
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouse_clicked = False
        super().event(event)
    
    def update(self):
        if self.mouse_clicked:
            mouse = Vector2(pygame.mouse.get_pos())
            global_pos = mouse + self.mouse_offset
            for i in self.axis:
                self.parentNode.offset[i] = global_pos[i] - self.parentNode.parentNode.position[i]

        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()


### - Keyboard - ###

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
    

## -- User func -- ##

class ClickOn(Modifier):
    def __init__(self, parentNode : Node, physics_check, function : callable, buttondown : bool = True, button : int = None):
        super().__init__(parentNode)
        
        self.func = function
        self.button = button
        
        self.physics_check = physics_check

        if buttondown:
            self.event_type = pygame.MOUSEBUTTONDOWN
        else:
            self.event_type = pygame.MOUSEBUTTONUP

    def event(self, event):
        if event.type == self.event_type and self.pressed(event):
            mouse = pygame.mouse.get_pos()
            for collision_area in self.parentNode.collision:
                if collision_area.physics_layer == self.physics_check:
                    for rect in collision_area.collision_blocks:
                        if rect.rect.collidepoint(mouse):
                            self.func()
                            return

        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()
    

    def pressed(self, event):
        if self.button is None:
            return True
        return event.button == self.button

class Press(Modifier):
    def __init__(self, parentNode, key, function, keydown = True, mouse = False):
        super().__init__(parentNode)
        self.key = key
        self.func = function

        if mouse:
            self.input_type = self.mouse
            if keydown:
                self.event_type = pygame.MOUSEBUTTONDOWN
            else:
                self.event_type = pygame.MOUSEBUTTONUP
        else:
            self.input_type = self.keyboard
            if keydown:
                self.event_type = pygame.KEYDOWN
            else:
                self.event_type = pygame.KEYUP

    def event(self, event):
        if event.type == self.event_type and self.input_type(event):
            self.func()

        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()
    

    def mouse(self, event):
        return event.button == self.key
    
    def keyboard(self, event):
        return event.key == self.key