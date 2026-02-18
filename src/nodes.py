import math
import os
import pygame
from pygame import Vector2
from pygame import Color

def positionFromStr(string, size, parentNode_size):
    sw, sh = Vector2(size)
    w, h = Vector2(parentNode_size)
    
    max_x, max_y = w - sw, h - sh
    mid_x, mid_y = max_x / 2, max_y / 2

    pos = {
        "top-left":     Vector2(0, 0),
        "left":         Vector2(0, mid_y),
        "bottom-left":  Vector2(0, max_y),
        "top-right":    Vector2(max_x, 0),
        "right":        Vector2(max_x, mid_y),
        "bottom-right": Vector2(max_x, max_y),
        "top":          Vector2(mid_x, 0),
        "bottom":       Vector2(mid_x, max_y),
        "center":       Vector2(mid_x, mid_y)
    }

    output = pos.get(string)
    
    if output:
        return [output, string]
    return [output, None]


# ----- Base of nodes ----- #


class Backbone:
    def __init__(self):
        self.children = []
    
    def event(self, event):
        for node in self.children:
            node.event(event)
    
    def update(self):
        for node in self.children:
            node.update()

    def draw(self):
        for node in self.children:
            node.draw()

class Modifiers(Backbone):
    def __init__(self, parentNode):
        super().__init__()
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.scene = self.parentNode.scene
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

class Node(Modifiers):
    def __init__(self, parentNode, size = Vector2(0, 0), offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode)

        self.size = Vector2(size)

        
        if (offset_str):
            self.offset, offset_str = positionFromStr(offset_str.lower(), self.size, self.parentNode.size)
        
        if offset_str is None:
            self.offset = Vector2(offset)

        self.position = self.parentNode.position + self.offset

        for otherNode in self.parentNode.children:
            if otherNode.position == self.position and otherNode is not self:
                print("Too many nodes at the same position, could not find a free spot")
                pygame.quit()
                exit()
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        self.position = self.parentNode.position + self.offset
        super().update()

    def draw(self):
        super().draw()
    
    def kill(self):
        self.parentNode.children.remove(self)


# ----- Nodes ----- #

class Scene(Backbone):
    def __init__(self, screen, screen_size):
        super().__init__()
        self.scene = self
        self.screen = screen    #Pygame - surface
        self.size = Vector2(screen_size)
        self.position = Vector2(0, 0)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

class BaseNode(Node):
    def __init__(self, parentNode, physics_layer = None, offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode, Vector2(0, 0), offset_str, offset)

        self.physics_layer = 0
        if (physics_layer and isinstance(physics_layer, int)):
            self.physics_layer = physics_layer
        
        self.hitBoxes = []
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()

class ColorBlock(Node):
    def __init__(self, parentNode, size, color = Color(255, 255, 255, 255), 
                offset_str = None, offset = Vector2(0, 0), alpha_chanel = False, changable = False):
        super().__init__(parentNode, size, offset_str, offset)
        self.color = pygame.Color(color)
        
        if not alpha_chanel:
            self.color.a = 255
        
        self.alpha_chanel = alpha_chanel
        self.changable = changable

        if self.alpha_chanel:
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        else:
            self.image = pygame.Surface(self.size)
        self.image.fill(self.color)

    def event(self, event):
        super().event(event)
    
    def update(self):
        self.rect = pygame.Rect(self.position, self.size)
        if self.changable:
            if self.alpha_chanel:
                self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            else:
                self.image = pygame.Surface(self.size)

            self.image.fill(self.color)
        super().update()

    def draw(self):
        # Místo přímého kreslení obdélníku vykreslíme připravený Surface
        self.scene.screen.blit(self.image, self.rect)
        super().draw()

    def kill(self):
        super().kill()

class SpriteBlock(Node):
    def __init__(self, parentNode, size, src, offset_str=None, offset=pygame.Vector2(0, 0), 
                alpha_chanel = False, changable = False):
        super().__init__(parentNode, size, offset_str, offset)
        self.src = src
        self.image = pygame.image.load(src).convert_alpha()

        self.alpha_chanel = alpha_chanel
        self.changable = changable

        self.surface = pygame.Surface(self.image.get_size()).convert_alpha()
        self.surface.blit(self.image, Vector2(0, 0))
        self.surface = pygame.transform.scale(self.surface, size)

    def event(self, event):
        super().event(event)
    
    def update(self):
        
        super().update()

    def draw(self):
        self.scene.screen.blit(self.surface, self.position)
        super().draw()

    def kill(self):
        super().kill()

class AnimatedSpriteBlock(Node):
    def __init__(self, parentNode, size, src, oneFrameSize, start, end, frameLen, offset_str=None, offset = pygame.Vector2(0, 0), 
                alpha_chanel = False, changable = False):
        super().__init__(parentNode, size, offset_str, offset)
        self.src = src
        self.image = pygame.image.load(src).convert_alpha()

        self.alpha_chanel = alpha_chanel
        self.changable = changable

        self.frameLen = frameLen
        self.count = 0
        self.index = 0

        if start > end:
            temp = end
            end = start
            start = temp

        tileCount = Vector2(self.image.get_size()[0] / oneFrameSize[0], self.image.get_size()[1] / oneFrameSize[1])
        self.frames = []
        for i in range(end - start + 1):
            frame = pygame.Surface(oneFrameSize).convert_alpha()
            frame.blit(self.image, Vector2(0, 0), 
                (oneFrameSize[0] * (i % tileCount[0]), oneFrameSize[1] * (i // tileCount[0]), oneFrameSize[0], oneFrameSize[1]))
            frame = pygame.transform.scale(frame, size)
            self.frames.append(frame)

    def event(self, event):
        super().event(event)
    
    def update(self):
        self.count += 1
        if self.count >= self.frameLen:
            self.count = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
        super().update()

    def draw(self):
        self.scene.screen.blit(self.frames[self.index], self.position)
        super().draw()

    def kill(self):
        super().kill()

class TilemapBlock(Node):
    def __init__(self, parentNode, size, src, oneFrameSize, coords, offset_str=None, offset = pygame.Vector2(0, 0), 
                alpha_chanel = False, changable = False):
        super().__init__(parentNode, size, offset_str, offset)
        self.src = src
        self.image = pygame.image.load(src).convert_alpha()

        self.alpha_chanel = alpha_chanel
        self.changable = changable

        self.surface = pygame.Surface(oneFrameSize).convert_alpha()
        self.surface.blit(self.image, Vector2(0, 0), 
            (oneFrameSize[0] * coords[0], oneFrameSize[1] * coords[1], oneFrameSize[0], oneFrameSize[1]))
        self.surface = pygame.transform.scale(self.surface, size)

    def event(self, event):
        super().event(event)
    
    def update(self):
        
        super().update()

    def draw(self):
        self.scene.screen.blit(self.surface, self.position)
        super().draw()

    def kill(self):
        super().kill()


# ----- Modifiers ----- #

class MouseClick(Modifiers):
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

class KeayboardMove(Modifiers):
    def __init__(self, parentNode, speed = 20):
        super().__init__(parentNode)

        self.velocity = Vector2(0, 0)
        self.speed = speed
    

    def event(self, event):
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            i = 1 if event.type == pygame.KEYDOWN else -1
            speed = self.speed * i
            if event.key == pygame.K_LEFT:
                self.velocity[0] += -speed
            elif event.key == pygame.K_RIGHT:
                self.velocity[0] += speed
            elif event.key == pygame.K_UP:
                self.velocity[1] += -speed
            elif event.key == pygame.K_DOWN:
                self.velocity[1] += speed
        super().event(event)
    
    def update(self):
        self.parentNode.offset += self.velocity
        super().update()

    def draw(self):
        super().draw()

    def kill(self):
        super().kill()