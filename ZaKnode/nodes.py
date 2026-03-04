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
    
    def run(self, func = None, global_input : callable = None):
        while self.running:
            dt_ms = self.clock.tick(self.tick_speed)
            self.delta = dt_ms / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if global_input:
                    global_input(event)
            
                self.scenes[self.current_scene].event(event)

            if func:
                func()

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
        
    
    def changeScene(self, changer = None):
        if isinstance(changer, str):
            last = self.current_scene

            if changer in self.scenes:
                self.current_scene = changer
            else:
                print("error")

        elif isinstance(changer, int):
            scene_names = list(self.scenes.keys())
            index = scene_names.index(self.current_scene)
            index += changer
            
            index = index % len(scene_names)

            self.current_scene = scene_names[index]
        else:
            self.changeScene(1)

    
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

        self.parentNode.addCollision(self)

        self.collision_blocks = []

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
    

    def addRect(self, size, offset_str = None, offset = Vector2(0, 0)):
        CollisionBlock(self, size, offset_str = offset_str, offset = offset)

class CollisionBlock(Node):
    def __init__(self, parentNode, size, zindex = -5, offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
        self.parentNode.collision_blocks.append(self)

        self.rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        self.rect = None
        self.rect = pygame.Rect(self.position, self.size)
        
    def draw(self):
        if self.parentNode.show:
            surface = pygame.Surface(self.size, pygame.SRCALPHA)
            surface.fill("#00ff0044")
            self.game.screen.blit(surface, self.rect)
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

    def kill(self):
        self.parentNode.collision_blocks.remove(self)
        super().kill()


# -- Visuals -- #

class Label(Node):
    def __init__(self, parentNode, text : str, font, color = Color(255, 255, 255), zindex = 0, 
                offset_str = None, offset = Vector2(0, 0), changable = False):
        
        
        self.text = text
        self.color = Color(color)
        self.font = font
        self.message = self.font.render(self.text, True, self.color)
        self.surface = pygame.Surface(self.message.get_size(), pygame.SRCALPHA)
        self.surface.blit(self.message)
        
        size = Vector2(self.surface.get_size())

        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)

        self.rect = pygame.Rect(self.position, self.size)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        self.rect = pygame.Rect(self.position, self.size)
        

    def draw(self):
        self.game.screen.blit(self.surface, self.rect)
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, newText = None, newFont = None, newColor = None):
        if newText is not None:
            self.text = newText
        
        if newFont is not None:
            self.font = newFont

        if newColor is not None:
            self.color = Color(newColor)

        self.message = self.font.render(self.text, True, self.color)
        self.surface = pygame.Surface(self.message.get_size(), pygame.SRCALPHA)
        self.surface.blit(self.message)

        self.size = Vector2(self.surface.get_size())


    def kill(self):
        super().kill()

class TextBlock(Node):
    def __init__(self, parentNode, text : str, font, txt_color = Color(255, 255, 255), bg_color = Color(0, 0, 0), padding = 0, zindex = 0, 
                offset_str = None, offset = Vector2(0, 0)):
        
        self.text = text
        self.color = Color(txt_color)
        self.background = Color(bg_color)
        self.font = font

        self.message = self.font.render(self.text, True, self.color)
        
        self.padding = padding

        self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                       self.message.get_size()[1] + self.padding * 2), pygame.SRCALPHA)
        self.surface.fill(self.background)
        self.surface.blit(self.message, (self.padding, self.padding))

        size = Vector2(self.surface.get_size())
        
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)

        self.rect = pygame.Rect(self.position, self.size)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        self.rect = pygame.Rect(self.position, self.size)
        

    def draw(self):
        self.game.screen.blit(self.surface, self.rect)
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, text = None, font = None, txt_color = None, bg_color = None, padding = None):
        if text is not None:
            self.text = text
        
        if font is None:
            self.font = font

        if txt_color is None:
            self.color = Color(txt_color)
        
        if bg_color is None:
            self.background = Color(bg_color)
        
        if padding is None:
            self.padding = padding


        self.message = self.font.render(self.text, True, self.color)
        self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                       self.message.get_size()[1] + self.padding * 2), pygame.SRCALPHA)
        self.surface.fill(self.background)
        self.surface.blit(self.message, (self.padding, self.padding))

        self.size = self.surface.get_size()


    def kill(self):
        super().kill()

class ColorBlock(Node):
    def __init__(self, parentNode, size, color = Color(255, 255, 255, 255), zindex = 0, 
                offset_str = None, offset = Vector2(0, 0), alpha_chanel = False):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
        self.color = pygame.Color(color)
        
        self.alpha_chanel = alpha_chanel

        if self.alpha_chanel:
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        else:
            self.image = pygame.Surface(self.size)
        self.image.fill(self.color)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        self.rect = pygame.Rect(self.position, self.size)
        

    def draw(self):
        # Draw the pre-rendered Surface instead of drawing a rectangle directly
        self.game.screen.blit(self.image, self.rect)
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, newSize = None, newColor = None):
        if newSize is None:
            newSize = self.size
        
        if newColor is None:
            newColor = self.color

        self.size = newSize
        self.color = newColor

        if self.changable:
            if self.alpha_chanel:
                self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            else:
                self.image = pygame.Surface(self.size)
            self.image.fill(self.color)
        else:
            print("Cant change")

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
        self.frames.clean()
        for i in range(len(framesArr)):
            frame = pygame.transform.scale(framesArr[i], self.size)
            self.frames.append(frame)

        self.count = 0
        self.index = 0

class TileMapBlock(Node):
    def __init__(self, parentNode, size, tile_node, coords, zindex = 0, offset_str=None, offset = pygame.Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
        
        self.size = size

        self.tileNode = tile_node

        self.coords = [int(coords[0] % self.tileNode.tileCount[0]), int(coords[1] % self.tileNode.tileCount[1])]


        self.surface = self.tileNode.grid[self.coords[0]][self.coords[1]]
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
    
    
    def change(self, coords = None, changer = None):
        if coords is None:
            if changer is None:
                return
            self.coords = [int((self.coords[0] + changer[0]) % self.tileNode.tileCount[0]), int((self.coords[1] + changer[1]) % self.tileNode.tileCount[1])]
        else:
            self.coords = [int(coords[0] % self.tileNode.tileCount[0]), int(coords[1] % self.tileNode.tileCount[1])]
        
        self.surface = self.tileNode.grid[self.coords[0]][self.coords[1]]
        self.surface = pygame.transform.scale(self.surface, self.size)