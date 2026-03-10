import pygame
from pygame import Vector2
from pygame import Color

from .base import Node
from . import modifiers
from . import resources


"""
class default(Node):
    def __init__(self, parentNode, size, zindex : float = 0, offset_str : str = None, offset : Vector2 = Vector2(0, 0), angle = 0):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)

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

    def change(self, size = None, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)
        
    def kill(self):
        super().kill()
"""


# ----------- Nodes ------------ #

# -- Primary -- #

class Game:
    def __init__(self, screen_size, name : str = "ZaKgame window", fps : int = 120):
        pygame.init()
        pygame.font.init()

        self.position = Vector2(0, 0)
        self.angle = 0

        self.game = self

        self.running = True
        self.screen_size = Vector2(screen_size)

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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
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

class Scene(Node):
    def __init__(self, name : str, game : Game, bg_color = Color(0, 0, 0)):
        self.game = game

        self.parentNode = game

        self.children = []
        self.collision = []
        
        self.name = name
        self.game.addScene(self.name, self)

        self.change(Color(bg_color), self.game.screen_size, offset = Vector2(0, 0), angle = 0)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()
    
    def kill(self):
        for child in self.children[:]:
            child.kill()

        self.children.clear()
        self.collision.clear()

        self.game.removeScene(self.name)
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

    def change(self, bg_color = None, size = None, offset = None, angle = None):
        if bg_color is not None:
            self.bg_color = bg_color
        super().nodeChange(size = size, offset = offset, angle = angle)

class BaseNode(Node):
    def __init__(self, parentNode,  zindex : float = 0, offset_str : str = None, offset : Vector2 = Vector2(0, 0), angle = 0):
        super().__init__(parentNode, size = Vector2(0, 0), offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)

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

    def change(self, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)
        
    def kill(self):
        super().kill()


class ShowAxis():
    def __init__(self, parentNode : Node):
        self.parentNode = parentNode
        self.images = resources.LoadImageGrid(resources.directory("img/axis.png"), Vector2(15, 15), alpha_chanel = True)

        size = Vector2(40, 40)
        gap = 50

        offsets = [Vector2(gap, size.x // -2), Vector2(size.x // -2, gap), Vector2(gap, gap)]
        axis = ["x", "y", None]
        lines = [lambda: pygame.draw.line(self.parentNode.game.screen, (255, 0, 0), Vector2(0, self.parentNode.position.y), Vector2(self.parentNode.game.screen_size[0], self.parentNode.position.y), 4),
                 lambda: pygame.draw.line(self.parentNode.game.screen, (0, 255, 0), Vector2(self.parentNode.position.x, 0), Vector2(self.parentNode.position.x, self.parentNode.game.screen_size[1]), 4)]

        self.tiles = []

        self.tiles.append(TileMapBlock(self.parentNode, size, self.images, [0, 0], 600))

        self.hitareas = []
        self.modifiers = []

        for i in range(3):
            self.tiles.append(TileMapBlock(self.parentNode, size, self.images, [1 + i, 0], 600, offset = offsets[i]))
            new_area = CollisionArea(self.parentNode, 98 + i)
            new_area.addCollisionBlock(size, offset = offsets[i])
            self.hitareas.append(new_area)

            self.modifiers.append(modifiers.MouseDragMove(self.parentNode, 98 + i, axis = axis[i]))
            if i < 2:
                self.modifiers.append(modifiers.Hold(self.parentNode, 98 + i, lines[i], 1))

    
    def hide(self):
        for tile in self.tiles:
            tile.kill()
        
        for hitarea in self.hitareas:
            hitarea.kill()


# -- Logic -- #

class CollisionArea(Node):
    def __init__(self, parentNode, physics_layer : int = 0, show : bool = False, show_self : bool = False):
        super().__init__(parentNode, size = parentNode.size, zindex = 100, offset_str = None, offset = Vector2(0, 0))
        self.physics_layer = physics_layer
        self.show = show

        self.show_self = show_self
        if self.show_self:
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
            self.surface.fill("#ff00ff44")

        self.parentNode.addCollision(self)

        self.collision_blocks = []

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        self.rect = pygame.Rect(self.position, self.size)

    def draw(self):
        if self.show_self:
            self.game.screen.blit(self.surface, self.rect)
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, size = None, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)

    def kill(self):
        for block in self.collision_blocks:
            block.kill()
        super().kill()
    

    def addCollisionBlock(self, size : Vector2, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        return CollisionBlock(self, size, offset_str = offset_str, offset = offset)

class CollisionBlock(Node):
    def __init__(self, parentNode : CollisionArea, size : Vector2, zindex : float = -5, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
        self.parentNode.collision_blocks.append(self)

        self.rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

        if self.parentNode.show:
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
            self.surface.fill("#00ff0044")
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        self.rect = pygame.Rect(self.position, self.size)
        
    def draw(self):
        if self.parentNode.show:
            self.game.screen.blit(self.surface, self.rect)
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, size = None, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)

    def kill(self):
        self.parentNode.collision_blocks.remove(self)
        super().kill()



# -- Visuals -- #

class Label(Node):
    def __init__(self, parentNode, text : str, font : pygame.font, color : Color = Color(255, 255, 255), zindex : float = 0, 
                offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
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

    def change(self, text : str = None, font : pygame.font = None, color : Color = None, size = None, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)
        if text is not None:
            self.text = text
        
        if font is not None:
            self.font = font

        if color is not None:
            self.color = Color(color)

        self.message = self.font.render(self.text, True, self.color)

        self.surface = pygame.Surface(self.message.get_size(), pygame.SRCALPHA)

        self.surface.blit(self.message)

        self.surface = pygame.transform.rotate(self.surface, self.angle)

        self.size = Vector2(self.surface.get_size())

    def kill(self):
        super().kill()


class TextBlock(Node):
    def __init__(self, parentNode, text : str, font, txt_color = Color(255, 255, 255), bg_color = Color(0, 0, 0), padding = 0, zindex = 0, 
                offset_str = None, offset = Vector2(0, 0), angle : int = 0, alpha_chanel = False):
        super().__init__(parentNode, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)
        
        self.change(text = text, font = font, txt_color = txt_color, bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle, alpha_chanel = alpha_chanel)


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
    
    def change(self, text = None, font = None, txt_color = None, bg_color = None, padding = None, offset_str = None, offset = None, zindex = None, angle = None, alpha_chanel = False):
        if text is not None:
            self.text = text
        
        if font is not None:
            self.font = font

        if txt_color is not None:
            self.color = Color(txt_color)
        
        if bg_color is not None:
            self.background = Color(bg_color)
        
        if padding is not None:
            self.padding = padding
        
        self.alpha = alpha_chanel

        self.message = self.font.render(self.text, True, self.color)
        if self.alpha:
            self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                       self.message.get_size()[1] + self.padding * 2), pygame.SRCALPHA)
        else:
            self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                       self.message.get_size()[1] + self.padding * 2))
            
        self.surface.fill(self.background)
        self.surface.blit(self.message, (self.padding, self.padding))

        self.surface = pygame.transform.rotate(self.surface, self.angle)

        self.size = self.surface.get_size()

        super().nodeChange(offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)


    def kill(self):
        super().kill()


class ColorBlock(Node):
    def __init__(self, parentNode, size, color = Color(255, 255, 255, 255), zindex = 0, offset_str = None, offset = Vector2(0, 0), angle = 0, alpha_channel = False):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)
    
        self.change(color = color, alpha_channel = alpha_channel)


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
    
    def change(self, color = None, alpha_channel = None, size = None, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)

        if color is not None:
            self.color = color
        
        if alpha_channel is not None:
            self.alpha_channel = alpha_channel

        if self.alpha_channel:
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        else:
            self.surface = pygame.Surface(self.size)

        self.surface.fill(self.color)

        self.surface = pygame.transform.rotate(self.surface, self.angle)
        
        
    
    def kill(self):
        super().kill()


class SpriteBlock(Node):
    def __init__(self, parentNode, size, image, zindex = 0, offset_str = None, offset = Vector2(0, 0), angle = 0):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)
        
        self.change(image = image)

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

    def change(self, image = None, size = None, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)

        if image is not None:
            self.surface = pygame.transform.scale(image, self.size)

        self.surface = pygame.transform.rotate(self.surface, 45)


class AnimatedSpriteBlock(Node):
    def __init__(self, parentNode, size, framesArr, fps, zindex = 0, offset_str=None, offset = pygame.Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)


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

    def change(self, frames_arr = None, fps = None, size = None, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)

        if frames_arr is not None:
            self.frames.clear()
            for one_frame in frames_arr:
                frame = pygame.transform.scale(one_frame, self.size)
                self.frames.append(frame)

            self.count = 0
            self.index = 0
        
        new_frames = []
        for frame in self.frames:
            new_frames.append(pygame.transform.rotate(frame, self.angle))
        
        self.frames.clear()
        self.frames = new_frames


    def kill(self):
        super().kill()


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

    def change(self, tile_node = None, coords = None, changer = None, size = None, offset_str = None, offset = None, zindex = None, angle = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, angle = angle)

        if tile_node is not None:
            self.tileNode = tile_node
    
        if coords is None:
            if changer is None:
                return
            elif isinstance(changer, int):
                new_x = int((self.coords[0] + changer) % self.tileNode.tileCount[0])
                new_y = int((self.coords[1] + (self.coords[0] + changer) // self.tileNode.tileCount[0]) % self.tileNode.tileCount[1])
            else:
                new_x = int((self.coords[0] + changer[0]) % self.tileNode.tileCount[0])
                new_y = int((self.coords[1] + changer[1]) % self.tileNode.tileCount[1])
            self.coords = [new_x, new_y]
        else:
            self.coords = [int(coords[0] % self.tileNode.tileCount[0]), int(coords[1] % self.tileNode.tileCount[1])]
        
        self.surface = self.tileNode.grid[self.coords[0]][self.coords[1]]

        self.surface = pygame.transform.scale(self.surface, self.size)

        self.surface = pygame.transform.rotate(self.surface, 45)


    def kill(self):
        super().kill()

