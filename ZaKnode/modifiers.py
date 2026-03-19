import math
import pygame
from pygame import Vector2

from .base import Modifier, Node


default_speed = 200


"""
class default(Modifier):
    def __init__(self, parentNode : Node):
        super().__init__(parentNode)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()
"""


# ----------- Modifiers ------------ #

#   # -- Position changers -- ##

#       ## - Constant - ###

class AxisMove(Modifier):
    def __init__(self, parentNode : Node, start : int, end : int = None, axis : str = "x", mode : str = "linear", speed : float = default_speed, strength : float = 3, looping : bool = True, show_path : bool = False):
        super().__init__(parentNode)

        if end is None:
            axis_arr = {"x" : 0, "y" : 1}
            end = self.parentNode.offset[axis_arr[axis]]
        
        self.elapsed = 0.0
        
        self.direction = 1

        self.change(start = start, end = end, axis = axis, mode = mode, speed = speed, strength = strength, looping = looping, show_path = show_path)

        self.last_offset = self.parentNode.offset[self.axis]


    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.duration == 0:
            return
        
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

        changer = self.parentNode.offset

        changer[self.axis] += new_offset - self.last_offset
        
        self.parentNode.change(offset = changer)
        self.last_offset = new_offset

        if self.direction == -1 and not self.looping:
            self.kill()

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
    
    def change(self, start = None, end = None, axis = None, mode = None, speed = None, strength = None, looping = None, show_path = None):
        if show_path is not None:
            self.show = show_path
        
        if looping is not None:
            self.looping = looping

        if axis is not None:
            axis_arr = {"x" : 0, "y" : 1}
            self.axis = axis_arr.get(axis.lower(), 0)
        
        if end is not None:
            self.end = end
        
        if start is not None:
            self.start = start
        
        if self.start > self.end:
            self.start, self.end = self.end, self.start
        
        if speed is not None:
            self.speed = speed

        if strength is not None:
            self.strength = abs(strength)

        if start is not None or end is not None:
            if self.parentNode.offset[self.axis] < self.start:
                self.parentNode.change(offset = self.start)
            elif self.parentNode.offset[self.axis] > self.end:
                self.parentNode.change(offset = self.end)

            self.path_len = self.end - self.start
            self.duration = self.path_len / self.speed if self.speed != 0 else 0

        if mode is not None:
            modes = {
                "linear" : self.linear,
                "ease-in" : self.easeIn,
                "ease-out" : self.easeOut,
                "ease-both" : self.easeBoth,
                "ease-in-out" : self.easeBoth
            }

            self.mode = modes.get(mode, self.linear)

        super().modifierChange()

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
    def __init__(self, parentNode : Node, end : Vector2, start : Vector2 = None, mode : str = "linear", speed : float = default_speed, strength : float = 3, looping : bool = True, show_path : bool = False):
        super().__init__(parentNode)

        if start is None:
            start = self.parentNode.offset

        self.elapsed = 0.0

        self.direction = 1

        self.change(end = end, start = start, mode = mode, speed = speed, strength = strength, looping = looping, show_path = show_path)

        self.last_offset = Vector2(0, 0)


    
    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.duration == 0:
            return
        
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
        
        self.parentNode.change(offset = self.parentNode.offset + step)
        self.last_offset = self.new_offset

        if self.direction == -1 and not self.looping:
            self.kill()

        super().update()

    def draw(self):
        if self.show:
            center_x = self.parentNode.position.x + self.parentNode.size.x // 2
            center_y = self.parentNode.position.y + self.parentNode.size.y // 2

            start = (center_x - self.difference.x * self.partition, center_y - self.difference.y * self.partition)
            end = (center_x + self.difference.x * (1 - self.partition), center_y + self.difference.y * (1 - self.partition))
                
            pygame.draw.line(self.game.screen, (255, 0, 0), start, end, width = 4)
        super().draw()
    
    def change(self, end = None, start = None, mode : str = None, speed : int = None, strength = None, looping = None, show_path = None):
        
        if looping is not None:
            self.looping = looping
        
        if show_path is not None:
            self.show = show_path
        
        if speed is not None:
            self.speed = abs(speed)
        
        if strength is not None:
            self.strength = abs(strength)

        if end is not None:
            self.end = Vector2(end)
        
        if start is not None:
            self.start = Vector2(start)

        if start is not None or end is not None:
            self.difference = self.end - self.start
            self.path_len = self.difference.length()

        self.duration = self.path_len / self.speed if self.speed != 0 else 0
        
        if mode is not None:
            modes = {
                "linear" : self.linear,
                "ease-in" : self.easeIn,
                "ease-out" : self.easeOut,
                "ease-both" : self.easeBoth,
                "ease-in-out" : self.easeBoth
            }

            self.mode = modes.get(mode, self.linear)
        
        if start is not None:
            self.parentNode.change(offset = self.start)
        
        super().modifierChange()

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
    def __init__(self, parentNode : Node, relative_center : Vector2, radius : float = None, clockwise : bool = True, start_deg : float = 0, speed : float = default_speed, show_path : bool = False):
        super().__init__(parentNode)

        self.change(relative_center = relative_center, radius = radius, clockwise = clockwise, start_deg = start_deg, speed = speed, show_path = show_path)
        
        self.last_offset = self.parentNode.offset
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.duration == 0:
            return

        self.elapsed += self.game.delta * self.direction

        if self.elapsed >= self.duration or self.elapsed <= 0:
            self.elapsed = self.elapsed % self.duration
        
        percents = self.elapsed / self.duration

        self.angle = 2 * math.pi * percents

        self.new_offset = Vector2(self.center.x + math.cos(self.angle) * self.radius, self.center.y + math.sin(self.angle) * self.radius)


        step = self.new_offset - self.last_offset
        
        self.parentNode.change(offset = self.parentNode.offset + step)

        self.last_offset = self.new_offset

        super().update()

    def draw(self):
        if self.show:
            center = self.parentNode.offset + Vector2(math.cos(self.angle) * self.radius, math.sin(self.angle) * self.radius) * -1
            pygame.draw.circle(self.game.screen, (255, 0, 0), center, abs(self.radius), width = 4)
        super().draw()

    def kill(self):
        super().kill()
    

    def change(self, relative_center : Vector2 = None, radius : float = None, clockwise : bool = None, start_deg : float = None, speed : float = None, show_path : bool = None):

        if relative_center is not None:
            self.center = self.parentNode.offset + Vector2(relative_center)
            if radius is None:
                difference = self.parentNode.offset - self.center
                self.radius = difference.length()
            else:
                self.radius = radius
            self.path_len = 2 * math.pi * self.radius
        else:
            if radius is not None:
                self.radius = radius
                self.path_len = 2 * math.pi * self.radius
        
        if show_path is not None:
            self.show = show_path

        if speed is not None:
            self.speed = max(speed, 0)

        if clockwise is not None:
            self.direction = 1 if clockwise else -1

        if start_deg is None:
            start_deg = (self.angle / (2 * math.pi)) * 360
        self.angle = math.radians(start_deg)

        
        self.duration = self.path_len / self.speed if self.speed != 0 else 0

        self.elapsed = (start_deg / 360) * self.duration

        super().modifierChange()

class Follow(Modifier):
    def __init__(self, parentNode : Node, follow_node : Node, axis = "both", speed = default_speed):
        super().__init__(parentNode)
        self.change(follow_node = follow_node, speed = speed, axis = axis)

    def event(self, event):
        super().event(event)
    
    def update(self):
        direction = self.follow_node.position - self.parentNode.position 
        if direction != Vector2(0, 0):
            changer = self.parentNode.offset
            step = self.speed * self.game.delta * direction.normalize()
            for i in self.axis:
                changer[i] += step[i]
            if step.length() > direction.length():
                for i in self.axis:
                    changer[i] = (self.follow_node.position - self.parentNode.parentNode.position)[i]
            self.parentNode.change(offset = changer)
        super().update()

    def draw(self):
        super().draw()

    def change(self, follow_node : Node = None, speed : int = None, axis : str = None):
        if follow_node is  not None:
            self.follow_node = follow_node
        if speed is not None:
            self.speed = speed
        if axis is not None:
            axis_arr = {"x" : [0], "y" : [1], "both" : [0, 1], "all" : [0, 1]}
            self.axis = axis_arr.get(axis.lower(), [0, 1])
        super().modifierChange()

    def kill(self):
        super().kill()

class Centralize(Modifier):
    def __init__(self, parentNode : Node, scene : Node):
        super().__init__(parentNode)
        self.scene = scene

    def event(self, event):
        super().event(event)
    
    def update(self):
        self.scene.change(offset = self.game.screen_size / 2 - (self.parentNode.position - self.scene.position))
        super().update()

    def draw(self):
        super().draw()

    def change(self):
        super().modifierChange()

    def kill(self):
        self.scene.change(offset = Vector2(0, 0))
        super().kill()


#       ## - Mouse - ###

class MouseClickMove(Modifier):
    def __init__(self, parentNode : Node):
        super().__init__(parentNode)
    

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            self.parentNode.change(offset = mouse_pos - self.parentNode.parentNode.position)
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()
    
    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()

class MouseDragMove(Modifier):
    def __init__(self, parentNode : Node, physics_check : int = 1, axis : str = None):
        super().__init__(parentNode)

        self.axis = [0, 1]
        
        self.mouse_offset = Vector2(0, 0)

        self.change(physics_check = physics_check, axis = axis)

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
            new_offset = self.parentNode.offset
            for i in self.axis:
                new_offset[i] = global_pos[i] - self.parentNode.parentNode.position[i]
            self.parentNode.change(offset = new_offset)

        super().update()

    def draw(self):
        super().draw()
    
    def change(self, physics_check = None, axis = None):
        axis_arr = {"x" : [0], "y" : [1], "all" : [0, 1], "both" : [0, 1], "xy" : [0, 1]}

        if axis is not None:
            self.axis = axis_arr.get(axis.lower(), [0, 1])

        if physics_check is not None:
            self.physics_check = physics_check
            self.mouse_clicked = False

        super().modifierChange()

    def kill(self):
        super().kill()


#       ## - Keyboard - ###

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

        step = self.parentNode.offset + direction * self.speed * self.game.delta
        self.parentNode.change(offset = step)

        if not self.leave_window:
            max_x = self.game.screen_size[0] - self.parentNode.size.x
            max_y = self.game.screen_size[1] - self.parentNode.size.y

            self.parentNode.change(offset = Vector2(max(0, min(max_x, self.parentNode.offset.x)), max(0, min(max_y, self.parentNode.offset.y))))

        super().update()

    def draw(self):
        super().draw()

    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()

class KeyboardArrowsMove(KeyboardMove):
    def __init__(self, parentNode : Node, speed : float = default_speed, leave_window : bool = False):
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
    
    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()

class KeyboardWASDMove(KeyboardMove):
    def __init__(self, parentNode : Node, speed : float = default_speed, leave_window : bool = False):
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
    
    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()
    

#   # -- User func -- ##

class ClickOn(Modifier):
    def __init__(self, parentNode : Node, physics_check : int, function : callable, buttondown : bool = True, button : int = None):
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
    
    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()
    

    def pressed(self, event):
        if self.button is None:
            return True
        return event.button == self.button

class Hover(Modifier):
    def __init__(self, parentNode : Node, physics_check : int, func : callable, else_func : callable = None):
        super().__init__(parentNode)
        self.hover = False
        self.else_func = None
        self.change(physics_check = physics_check, func = func, else_func = else_func)

    def event(self, event):     
        super().event(event)
    
    def update(self):
        did = False
        mouse = pygame.mouse.get_pos()
        for collision_area in self.parentNode.collision:
            if collision_area.physics_layer == self.physics_check:
                for rect in collision_area.collision_blocks:
                    if rect.rect.collidepoint(mouse):
                        self.func()
                        did = True
        
        if not did and self.else_func is not None:
            self.else_func()
        super().update()

    def draw(self):
        super().draw()

    def change(self, physics_check = None, func = None, else_func = None):
        if physics_check is not None:
            self.physics_check = physics_check
        
        if func is not None:
            self.func = func
        
        if else_func is not None:
            self.else_func = else_func

        super().modifierChange()

    def kill(self):
        super().kill()


class Hold(Modifier):
    def __init__(self, parentNode : Node, physics_check : int, function : callable, button : int = None):
        super().__init__(parentNode)
        
        self.func = function
        self.button = button
        
        self.physics_check = physics_check

        self.holding = False

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.pressed(event):
            mouse = pygame.mouse.get_pos()
            for collision_area in self.parentNode.collision:
                if collision_area.physics_layer == self.physics_check:
                    for rect in collision_area.collision_blocks:
                        if rect.rect.collidepoint(mouse):
                            self.holding = True
                            return
        
        elif event.type == pygame.MOUSEBUTTONUP and self.pressed(event):
            self.holding = False
            return

        super().event(event)
    
    def update(self):
        if self.holding:
            self.func()
        super().update()

    def draw(self):
        super().draw()
    
    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()
    

    def pressed(self, event):
        if self.button is None:
            return True
        return event.button == self.button
    
class Press(Modifier):
    def __init__(self, parentNode : Node, key, function : callable, keydown : bool = True, mouse : bool = False):
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
    
    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()
    

    def mouse(self, event):
        return event.button == self.key
    
    def keyboard(self, event):
        return event.key == self.key

class ForeverDo(Modifier):
    def __init__(self, parentNode : Node, func : callable):
        super().__init__(parentNode)
        self.change(func = func)

    def event(self, event):
        super().event(event)
    
    def update(self):
        self.func()
        super().update()

    def draw(self):
        super().draw()

    def change(self, func = None):
        if func is not None:
            self.func = func
        super().modifierChange()

    def kill(self):
        super().kill()

class SignalTrigger(Modifier):
    def __init__(self, parentNode : Node, signal_name : str, func : callable):
        super().__init__(parentNode)

        self.change(name = signal_name, func = func)

    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.game.signals[self.signal_name]:
            self.game.signals[self.signal_name] = False
            self.func()
        super().update()

    def draw(self):
        super().draw()

    def change(self, name = None, func = None):
        if name is not None:
            self.signal_name = name
        if func is not None:
            self.func = func
        super().modifierChange()

    def kill(self):
        super().kill()

class OnCollideDo(Modifier):
    def __init__(self, parentNode : Node, func : callable, physics_check : int, parent_physics_layer : int = None):
        super().__init__(parentNode)
        if parent_physics_layer is None:
            parent_physics_layer = "all"

        self.change(func = func, physics_check = physics_check, parent_physics_layer =  parent_physics_layer)

    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.checkForCollision(self.game.scenes[self.game.current_scene].children):
            self.func

        super().update()

    def draw(self):
        super().draw()

    def change(self, func = None, physics_check = None, parent_physics_layer = None):
        if func is not None:
            self.func = func

        if physics_check is not None:
            self.physics_check = physics_check

        if parent_physics_layer is not None:
            if parent_physics_layer == "all":
                self.parent_physics_check = self.allParentLayers
            else:
                self.parent_physics_check = self.parentLayers
                self.parent_physics = list(parent_physics_layer)

        super().modifierChange()

    def kill(self):
        super().kill()

    
    def allParentLayers(self, collision_area):
        return True
    
    def parentLayers(self, collision_area):
        return collision_area.physics_layer in self.parent_physics

    def checkForCollision(self, parentNode):
        for node in parentNode:
            if hasattr(node, "collision"):
                for collisionArea in node.collision:
                    if collisionArea.physics_layer == self.physics_check:
                        for collisionBlock in collisionArea.collision_blocks:
                            for parentColArea in self.parentNode.collision:
                                if self.parent_physics_check(parentColArea):
                                    for parentRect in parentColArea.collision_blocks:
                                        if parentRect.rect.colliderect(collisionBlock.rect):
                                            return True
            if hasattr(node, "children"):
                self.checkForCollision(node)

class OnCollideBothObjects(Modifier):
    def __init__(self, parentNode : Node, func : callable, physics_check : int, parent_physics_layer : int = None):
        super().__init__(parentNode)
        if parent_physics_layer is None:
            parent_physics_layer = "all"
            
        self.change(func = func, physics_check = physics_check, parent_physics_layer =  parent_physics_layer)

    def event(self, event):
        super().event(event)
    
    def update(self):
        output = self.checkForCollision(self.game.scenes[self.game.current_scene])
        if output[0]:
            self.func(output[1])

        super().update()

    def draw(self):
        super().draw()

    def change(self, func = None, physics_check = None, parent_physics_layer = None):
        if func is not None:
            self.func = func

        if physics_check is not None:
            self.physics_check = physics_check

        if parent_physics_layer is not None:
            if parent_physics_layer == "all":
                self.parent_physics_check = self.allParentLayers
            else:
                self.parent_physics_check = self.parentLayers
                self.parent_physics = list(parent_physics_layer)

        super().modifierChange()

    def kill(self):
        super().kill()

    
    def allParentLayers(self, collision_area):
        return True
    
    def parentLayers(self, collision_area):
        return collision_area.physics_layer in self.parent_physics

    def checkForCollision(self, parentNode):
        if hasattr(parentNode, "children"):
            for node in parentNode.children:
                if hasattr(node, "collision"):
                    for collisionArea in node.collision:
                        if collisionArea.physics_layer == self.physics_check:
                            for collisionBlock in collisionArea.collision_blocks:
                                for parentColArea in self.parentNode.collision:
                                    if self.parent_physics_check(parentColArea):
                                        for parentRect in parentColArea.collision_blocks:
                                            if parentRect.rect.colliderect(collisionBlock.rect):
                                                return [True, node]
                if hasattr(node, "children"):
                    self.checkForCollision(node)

        return [False, None]




#   # -- Sound/Music -- ##

class SoundEffectPlayer(Modifier):
    def __init__(self, parentNode : Node):
        super().__init__(parentNode)
        self.sound_effects = {}

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def change(self):
        super().modifierChange()

    def kill(self):
        super().kill()

    def add(self, name : str, sound):
        self.sound_effects[name] = sound
    
    def play(self, name : str):
        self.sound_effects[name].play()


