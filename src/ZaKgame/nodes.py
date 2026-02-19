import pygame
from pygame import Vector2
from pygame import Color

from .base import *

# ----- Nodes ----- #

class Scene(Default):
    def __init__(self, screen, screen_size, bg_color = Color(0, 0, 0)):
        super().__init__()
        self.scene = self
        self.screen = screen    #Pygame - surface
        self.size = Vector2(screen_size)
        self.position = Vector2(0, 0)

        self.bg_color = Color(bg_color)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)

class BaseNode(Node):
    def __init__(self, parentNode, physics_layer = None, zindex = 0, offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode, size = Vector2(0, 0), zindex = zindex, offset_str = offset_str, offset = offset)

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
    
    def addChild(self, newChild):
        super().addChild(newChild)

    def kill(self):
        super().kill()


# --- Visuals --- #

class ColorBlock(Node):
    def __init__(self, parentNode, size, color = Color(255, 255, 255, 255), zindex = 0, 
                offset_str = None, offset = Vector2(0, 0), alpha_chanel = False, changable = False):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
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
    def __init__(self, parentNode, size, image, zindex = 0, offset_str=None, offset=pygame.Vector2(0, 0), 
                alpha_chanel = False, changable = False):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)

        self.alpha_chanel = alpha_chanel
        self.changable = changable

        self.size = size

        self.surface = pygame.transform.scale(image, self.size)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        self.scene.screen.blit(self.surface, self.position)
        super().draw()

    def addChild(self, newChild):
        super().addChild(newChild)
    
    def kill(self):
        super().kill()
    


    def change(self, image):
        self.surface = pygame.transform.scale(image, self.size)


class AnimatedSpriteBlock(Node):
    def __init__(self, parentNode, size, framesArr, frameLen, zindex = 0, offset_str=None, offset = pygame.Vector2(0, 0), 
                alpha_chanel = False, changable = False):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)

        self.alpha_chanel = alpha_chanel
        self.changable = changable

        self.frameLen = frameLen
        self.count = 0
        self.index = 0

        self.siez = size

        self.frames = []
        for i in range(len(framesArr)):
            frame = pygame.transform.scale(framesArr[i], self.size)
            self.frames.append(frame)

        self.frame = self.frames[0]

    def event(self, event):
        super().event(event)
    
    def update(self):
        self.count += 1
        if self.count >= self.frameLen:
            self.count = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
        
        self.frame = self.frames[self.index]
        super().update()

    def draw(self):
        self.scene.screen.blit(self.frame, self.position)
        super().draw()

    def addChild(self, newChild):
        super().addChild(newChild)

    def kill(self):
        super().kill()



    def change(self, framesArr):
        self.frames = []
        for i in range(len(framesArr)):
            frame = pygame.transform.scale(framesArr[i], self.size)
            self.frames.append(frame)
        self.count = 0
        self.index = 0

class TileMapBlock(Node):
    def __init__(self, parentNode, size, image_grid, coords, zindex = 0, offset_str=None, offset = pygame.Vector2(0, 0), 
                alpha_chanel = False, changable = False):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
        self.alpha_chanel = alpha_chanel
        self.changable = changable

        self.size = size

        self.tileMap = image_grid


        self.surface = self.tileMap[coords[0]][coords[1]]
        self.surface = pygame.transform.scale(self.surface, self.size)

    def event(self, event):
        super().event(event)
    
    def update(self):
        
        super().update()

    def draw(self):
        self.scene.screen.blit(self.surface, self.position)
        super().draw()

    def addChild(self, newChild):
        super().addChild(newChild)

    def kill(self):
        super().kill()
    
    
    
    def change(self, newCoords):
        self.surface = self.tileMap.tiles[newCoords[0]][newCoords[1]]
        self.surface = pygame.transform.scale(self.surface, self.size)