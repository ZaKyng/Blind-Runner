import pygame
from pygame import Vector2
from pygame import Color

from .base import *

# ----------- Nodes ------------ #

# -- Primary -- #

class Game:
    def __init__(self, screen_size, name = "ZaKgame window", fps = 120):
        pygame.init()
        pygame.font.init()

        self.game = self

        self.running = True
        self.screen_size = tuple(screen_size)

        self.default_scene_name = "empty"

        self.scenes = {}
        self.current_scene = None
        Scene(self.default_scene_name, self)
        

        pygame.display.set_caption(name)

        self.fonts = {}
        self.fonts["main"] = pygame.font.SysFont('Arial', 50)
        self.fonts["secondary"] = pygame.font.SysFont('Arial', 30)

        self.screen = pygame.display.set_mode(self.screen_size) #pygame surface
        self.clock = pygame.time.Clock()

        self.tick_speed = fps

        self.delta = 1 / fps
    
    def run(self):
        while self.running:
            dt_ms = self.clock.tick(self.tick_speed)
            self.delta = dt_ms / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        scene_names = list(self.scenes.keys())
                        index = scene_names.index(self.current_scene)
                        index += 1
                        if index >= len(scene_names):
                            index = 0
                        self.current_scene = scene_names[index]

                self.scenes[self.current_scene].event(event)

            self.screen.fill(self.scenes[self.current_scene].bg_color)

            self.scenes[self.current_scene].update()
            self.scenes[self.current_scene].draw()

            pygame.display.flip()
    

    def addScene(self, name, scene):
        self.scenes[name] = scene
        if not self.current_scene:
            self.current_scene = name
        elif self.current_scene == self.default_scene_name and name != self.default_scene_name:
            self.current_scene = name
            self.scenes.pop(self.default_scene_name)
        
    
    def changeScene(self, name):
        self.current_scene = name

    
    def removeScene(self, name):
        self.scenes.pop(name)

class Scene(Parent):
    def __init__(self, name : str, game, bg_color = Color(0, 0, 0)):
        super().__init__(game)
        self.game = game
        
        self.name = name
        self.game.addScene(self.name, self)

        self.size = self.game.screen_size

        self.offset = Vector2(0, 0)

        self.position = self.offset

        self.bg_color = Color(bg_color)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()
    
    def kill(self):
        self.game.removeScene(self.name)
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

class BaseNode(Node):
    def __init__(self, parentNode,  zindex = 0, offset_str = None, offset = Vector2(0, 0), show_hitboxes = False):
        super().__init__(parentNode, size = Vector2(0, 0), zindex = zindex, offset_str = offset_str, offset = offset)
        
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

    def kill(self):
        super().kill()



# -- Logic -- #

class CollisionArea(Node):
    def __init__(self, parentNode, physics_layer = 0, show = False):
        super().__init__(parentNode, size = Vector2(0, 0), zindex = -10, offset_str = None, offset = Vector2(0, 0))
        self.physics_layer = physics_layer
        self.show = show

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

    def kill(self):
        super().kill()


class CollisionBlock(Node):
    def __init__(self, parentNode, size, zindex = 0, 
                offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)


# -- Visuals -- #

class ColorBlock(Node):
    def __init__(self, parentNode, size, color = Color(255, 255, 255, 255), zindex = 0, 
                offset_str = None, offset = Vector2(0, 0), alpha_chanel = True, changable = False):
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
        # Draw the pre-rendered Surface instead of drawing a rectangle directly
        self.game.screen.blit(self.image, self.rect)
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

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
        self.game.screen.blit(self.surface, self.position)
        super().draw()

    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def kill(self):
        super().kill()
    

    def change(self, image):
        self.surface = pygame.transform.scale(image, self.size)

class AnimatedSpriteBlock(Node):
    def __init__(self, parentNode, size, framesArr, fps, zindex = 0, offset_str=None, offset = pygame.Vector2(0, 0), 
                alpha_chanel = False, changable = False):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)

        self.alpha_chanel = alpha_chanel
        self.changable = changable

        self.frameLen = self.game.tick_speed // fps
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
        self.game.screen.blit(self.frame, self.position)
        super().draw()

    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

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
        self.game.screen.blit(self.surface, self.position)
        super().draw()

    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

    def kill(self):
        super().kill()
    
    
    def change(self, newCoords):
        self.surface = self.tileMap[newCoords[0]][newCoords[1]]
        self.surface = pygame.transform.scale(self.surface, self.size)