import os
import sys
import json
import pygame
from pygame import Vector2
from pygame import Color

from .base import Node
from . import modifiers
from . import resources


"""
class default(Node):
    def __init__(self, parentNode, size, zindex : float = 0, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex)

        self.change(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = True)

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

    def change(self, size = None, offset_str = None, offset = None, zindex = None, active = None, sizer : float = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex)
        
    def kill(self):
        super().kill()
"""
# ----------- Nodes ------------ #

#   # -- Primary -- #

class Game:
    def __init__(self, window_size, file_location, name : str = "ZaKgame window", fps : int = 120, remember_window_size : bool = False, screen_ratio : float = None, over_flow_hidden : bool = False):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.file = file_location

        self.running = True

        self.offset = Vector2(0, 0)
        self.position = Vector2(0, 0)

        self.game = self
        
        self.fonts = FontManager(self)
        self.signals = SignalManager(self)
        self.scenes = SceneManager(self)
        
        if remember_window_size is not None:
            resources.SaveData(self.directory("ZaK-settings.txt"), "remember_window_size", remember_window_size)

        saved_info = resources.ReadData(self.directory("ZaK-settings.txt"))
        if saved_info is not None:
            if saved_info["remember_window_size"]:
                window_size = saved_info["window_size"]
        else:
            resources.SaveDataList(self.directory("ZaK-settings.txt"), ["window_size", "remember_window_size"], [window_size, remember_window_size if remember_window_size is not None else False])
            
        self.size = Vector2(window_size)
        self.screen_ratio = screen_ratio
        self.over_flow_hidden = over_flow_hidden
        self.overflow_blocks = []
        if self.screen_ratio is None:
            self.screen_size = self.size
        else:
            if self.size.x / self.screen_ratio <= self.size.y:
                self.screen_size = Vector2(self.size.x, self.size.x / self.screen_ratio)

                if self.over_flow_hidden:
                    for i in range(2):
                        new_surface = pygame.surface.Surface((self.screen_size.x, (self.size.y - self.screen_size.y) / 2))
                        new_surface.fill((0, 0, 0))
                        self.overflow_blocks.append(new_surface)
            else:
                self.screen_size = Vector2(self.size.y * self.screen_ratio, self.size.y)

                if self.over_flow_hidden:
                    for i in range(2):
                        new_surface = pygame.surface.Surface(((self.size.x - self.screen_size.x) / 2, self.screen_size.y))
                        new_surface.fill((0, 0, 0))
                        self.overflow_blocks.append(new_surface)

        self.vw = self.screen_size.x / 100
        self.vh = self.screen_size.y / 100

        self.original_screen_size = self.screen_size.copy()
        self.scale = Vector2(1, 1)
        
        Scene(self.scenes.default_scene_name, self)

        pygame.display.set_caption(name)

        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE) #pygame surface
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

                elif event.type == pygame.VIDEORESIZE:
                    self.windowResize(Vector2(event.size))

                if global_input:
                    global_input(event)
            
                self.scenes.scenes[self.scenes.current_scene].event(event)

            if func:
                func()

            self.screen.fill((0, 0, 0))

            self.scenes.scenes[self.scenes.current_scene].update()
            self.scenes.scenes[self.scenes.current_scene].draw(self.scale)

            if self.overflow_blocks:
                self.screen.blit(self.overflow_blocks[0], (0, 0))
                if self.size.x / self.screen_ratio <= self.size.y:
                    position = (0, (self.size.y + self.screen_size.y) / 2) 
                else:
                    position = ((self.size.x + self.screen_size.x) / 2, 0)

                self.screen.blit(self.overflow_blocks[1], position)

            pygame.display.flip()
        
        resources.SaveData(self.directory("ZaK-settings.txt"), "window_size", tuple(self.size))
        
        pygame.quit()
        sys.exit()
    
    def end(self):
        self.running = False
    
    def directory(self, src : str):
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(self.file))

        #return os.path.join(base_path, src)
        return os.path.normpath(os.path.join(base_path, src))

    def windowResize(self, new_size):
        self.signals.setOffSignal("window_size_changed")
        if self.screen_ratio is None:
            new_screen_size = new_size
        else:
            if new_size.x / self.screen_ratio <= new_size.y:
                new_screen_size = Vector2(new_size.x, new_size.x / self.screen_ratio)

                self.overflow_blocks.clear()
                for i in range(2):
                    new_surface = pygame.surface.Surface((new_screen_size.x, (new_size.y - new_screen_size.y) / 2 + 5 if i == 1 else (new_size.y - new_screen_size.y) / 2))
                    new_surface.fill((0, 0, 0))
                    self.overflow_blocks.append(new_surface)
            else:
                new_screen_size = Vector2(new_size.y * self.screen_ratio, new_size.y)

                self.overflow_blocks.clear()
                for i in range(2):
                    new_surface = pygame.surface.Surface(((new_size.x - new_screen_size.x) / 2 + 5 if i == 1 else (new_size.x - new_screen_size.x) / 2, new_screen_size.y))
                    new_surface.fill((0, 0, 0))
                    self.overflow_blocks.append(new_surface)
            
        self.size = new_size
        self.scale = Vector2(new_screen_size.x / self.original_screen_size.x, new_screen_size.y / self.original_screen_size.y)
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

        self.screen_size = new_screen_size
        self.vw = self.screen_size.x / 100
        self.vh = self.screen_size.y / 100
    
        """for name in self.fonts.fonts.keys():
            self.fonts.updateFont(name)"""

        for scene in self.scenes.scenes.values():
            scene.change(offset = Vector2((self.size.x - self.screen_size.x) / 2, (self.size.y - self.screen_size.y) / 2))
        
    def gameDraw(self, surface, node, scale):
        self.screen.blit(pygame.transform.scale(surface, Vector2(node.size.x * scale.x, node.size.y * scale.y)), Vector2((node.position.x - self.scenes.scenes[self.scenes.current_scene].position.x) * scale.x + self.scenes.scenes[self.scenes.current_scene].position.x, (node.position.y - self.scenes.scenes[self.scenes.current_scene].position.y) * scale.y + self.scenes.scenes[self.scenes.current_scene].position.y))



class FontManager:
    def __init__(self, game = Game):
        self.game = game
        self.fonts = {}
        
    def addFont(self, name, path, size : float = 2):
        font_sizes = {"xs" : int(size * self.game.vh), "s" : int((size + 1) * self.game.vh), "m" : int((size + 2) * self.game.vh), "l" : int((size + 3) * self.game.vh), "xl" : int((size + 4) * self.game.vh)}
        new_font = {}
        new_font["raw-font"] = path
        new_font["size"] = size
        new_font["font"] = {}
        for key in font_sizes.keys():
            new_font["font"][key] = pygame.font.Font(path, font_sizes[key])
        self.fonts[name] = new_font

    def updateFont(self, name):
        font_sizes = {"xs" : int(self.fonts[name]["size"] * self.game.vh),
                      "s" : int((self.fonts[name]["size"] + 1) * self.game.vh),
                      "m" : int((self.fonts[name]["size"] + 2) * self.game.vh),
                      "l" : int((self.fonts[name]["size"] + 3) * self.game.vh),
                      "xl" : int((self.fonts[name]["size"] + 4) * self.game.vh)
                      }
        for key in self.fonts[name]["font"].keys():
            if key != "raw-font" and key != "size":
                self.fonts[name]["font"][key] = pygame.font.Font(self.fonts[name]["raw-font"], font_sizes[key])

class SignalManager:
    def __init__(self, game = Game):
        self.game = game
        self.signals = {}
    
    def addSignal(self, name):
        self.signals[name] = False
    
    def setOffSignal(self, name):
        self.signals[name] = True

class SceneManager:
    def __init__(self, game = Game):
        self.game = game
        self.scenes = {}
        self.game.signals.addSignal("scene_changed")

        self.default_scene_name = "empty"
        self.current_scene = None

    
    def addScene(self, name : str, scene):
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
                if self.scenes[changer].active:
                    self.current_scene = changer
                    self.enterScene(self.scenes[self.current_scene])
            else:
                print("error")

        elif isinstance(changer, int):
            scene_names = list(self.scenes.keys())
            index = scene_names.index(self.current_scene)
            index += changer
            
            index = index % len(scene_names)

            if self.scenes[scene_names[index]].active:
                self.current_scene = scene_names[index]

                self.enterScene(self.scenes[self.current_scene])
            else:
                self.changeScene(changer + 1 if changer > 0 else changer - 1)
        else:
            self.changeScene(1)
        self.game.signals.setOffSignal("scene_changed")
        
    def enterScene(self, scene):
        if scene.onEntry is not None:
            scene.onEntry()

    def removeScene(self, name):
        self.scenes.pop(name)



class Scene(Node):
    def __init__(self, name : str, game : Game, bg_color = Color(0, 0, 0), onEntry : callable = None):
        self.game = game

        self.parentNode = game

        self.children = []
        self.collision = []
        
        self.name = name
        self.game.scenes.addScene(self.name, self)

        self.onEntry = None

        self.change(Color(bg_color), self.game.screen_size, offset_str = "center", offset = Vector2(0, 0), onEntry = onEntry, active = True)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, scale = Vector2(1, 1)):
        self.game.gameDraw(self.surface, self, scale)
        super().draw(scale)
    
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

    def change(self, bg_color = None, size = None, offset_str = None, offset = None, onEntry = None, active = None):
        if bg_color is not None:
            self.bg_color = bg_color
            try:
                self.surface.fill(self.bg_color)
            except:
                pass
        
        if onEntry is not None:
            self.onEntry = onEntry
        
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, active = active)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.bg_color)
        
        

class BaseNode(Node):
    def __init__(self, parentNode,  zindex : float = 0, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, size = Vector2(0, 0), zindex = zindex, offset_str = offset_str, offset = offset, active = True)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, scale = Vector2(1, 1)):
        super().draw(scale)
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, offset_str = None, offset = None, zindex = None, active = None, sizer = None):
        if sizer is not None:
            self.change(offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

        super().nodeChange(offset_str = offset_str, offset = offset, zindex = zindex, active = active)

    def kill(self):
        super().kill()

class ShowAxis():
    def __init__(self, parentNode : Node):
        self.parentNode = parentNode
        self.images = resources.SpriteSheet(parentNode.game.directory("assets/axis.png"), Vector2(15, 15), alpha_channel = True)

        size = Vector2(40, 40)
        gap = 50

        offsets = [Vector2(gap, size.x // -2), Vector2(size.x // -2, gap), Vector2(gap, gap)]
        axis = ["x", "y", None]
        lines = [lambda: pygame.draw.line(self.parentNode.game.screen, (255, 0, 0), Vector2(0, self.parentNode.position.y), Vector2(self.parentNode.game.size[0], self.parentNode.position.y), 4),
                 lambda: pygame.draw.line(self.parentNode.game.screen, (0, 255, 0), Vector2(self.parentNode.position.x, 0), Vector2(self.parentNode.position.x, self.parentNode.game.size[1]), 4)]

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
                self.modifiers.append(modifiers.Hold(self.parentNode, 98 + i, lines[i], button = 1))


    
    def hide(self):
        for tile in self.tiles:
            tile.kill()
        
        for hitarea in self.hitareas:
            hitarea.kill()


#   # -- Logic -- #

class CollisionArea(Node):
    def __init__(self, parentNode, physics_layer : int = 0, show : bool = False, show_self : bool = False):
        super().__init__(parentNode, size = parentNode.size, zindex = 100, offset_str = None, offset = Vector2(0, 0))
        self.physics_layer = physics_layer
        
        self.collision_blocks = []
        
        self.change(show = show, show_self = show_self, active = True)

        self.parentNode.addCollision(self)

        

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, scale = Vector2(1, 1)):
        if self.show_self:
            self.game.gameDraw(self.surface, self, scale)
        super().draw(scale)
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, show : bool = None, show_self : bool = None, size : Vector2 = None, offset_str : str = None, offset = None, zindex : int = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if show is not None:
            self.show = show
        
        if show_self is not None:
            self.show_self = show_self
            if self.show_self:
                self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
                self.surface.fill("#ff00ff44")
        
        if self.show_self and size is not None:
            self.surface = pygame.Surface(size, pygame.SRCALPHA)
            self.surface.fill("#ff00ff44")

        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))


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

        self.change()
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        
    def draw(self, scale = Vector2(1, 1)):
        if self.parentNode.show:
            self.game.gameDraw(self.surface, self, scale)
        super().draw(scale)
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, size = None, offset_str = None, offset = None, zindex = None, sizer = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex)

        self.rect = pygame.Rect(Vector2(self.position.x - self.game.scenes.scenes[self.game.scenes.current_scene].position.x, self.position.y - self.game.scenes.scenes[self.game.scenes.current_scene].position.y), self.size)
        if self.parentNode.show:
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
            self.surface.fill("#00ff0044")

        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

    def kill(self):
        self.parentNode.collision_blocks.remove(self)
        super().kill()



#   # -- Visuals -- #

class Label(Node):
    def __init__(self, parentNode, text : str, font_name : str, font_size : str = "m", color : Color = Color(255, 255, 255), zindex : float = 0, 
                offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, zindex = zindex, offset_str = offset_str, offset = offset)
        self.change(text = text, font_name = font_name, font_size = font_size, color = color, offset_str = offset_str, offset = offset, active = True)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        
    def draw(self, scale = Vector2(1, 1)):
        self.game.gameDraw(self.surface, self, scale)
        super().draw(scale)
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, text : str = None, font_name : str = None, font_size = None, color : Color = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        if text is not None:
            self.text = text
        
        if font_name is not None:
            try:
                self.font = self.game.fonts.fonts[font_name]
            except:
                self.font = self.game.fonts.fonts["default"]
        
        if font_size is not None:
            self.font_size = font_size

        if color is not None:
            self.color = Color(color)

        if text is not None or color is not None or font_name is not None or font_size is not None:
            try:
                self.message = self.font["font"][self.font_size].render(self.text, True, self.color)
            except:
                self.message = self.font["font"]["m"].render(self.text, True, self.color)

            self.surface = pygame.Surface(self.message.get_size(), pygame.SRCALPHA)

            self.surface.blit(self.message)

            self.size = Vector2(self.surface.get_size())

        if sizer is not None:
            self.change(font_size = self.font_size, offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

        super().nodeChange(offset_str = offset_str, offset = offset, zindex = zindex, active = active)


    def kill(self):
        super().kill()

class TextBlock(Node):
    def __init__(self, parentNode, text : str, font_name : str, font_size : str = "m", txt_color = Color(255, 255, 255), bg_color = Color(0, 0, 0), padding = 0, zindex = 0, 
                offset_str = None, offset = Vector2(0, 0), alpha_channel = False):
        super().__init__(parentNode, offset_str = offset_str, offset = offset, zindex = zindex)
        
        self.change(text = text, font_name = font_name, font_size = font_size, txt_color = txt_color, bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset, zindex = zindex, alpha_channel = alpha_channel, active = True)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        

    def draw(self, scale = Vector2(1, 1)):
        self.game.gameDraw(self.surface, self, scale)
        super().draw(scale)
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, text = None, font_name : str = None, font_size = None, txt_color = None, bg_color = None, padding = None, offset_str = None, offset = None, zindex = None, alpha_channel = None, sizer = None, active = None):
        relevant_change = False
        
        if text is not None:
            self.text = text
            relevant_change = True
        
        if font_name is not None:
            try:
                self.font = self.game.fonts.fonts[font_name]
            except:
                self.font = self.game.fonts.fonts["default"]
            relevant_change = True
        
        if font_size is not None:
            self.font_size = font_size
            relevant_change = True

        if txt_color is not None:
            self.color = Color(txt_color)
            relevant_change = True
        
        if bg_color is not None:
            self.background = Color(bg_color)
            relevant_change = True
        
        if padding is not None:
            self.padding = padding
            relevant_change = True

        if alpha_channel is not None:
            self.alpha = alpha_channel
            relevant_change = True

        if relevant_change:
            try:
                self.message = self.font["font"][self.font_size].render(self.text, True, self.color)
            except:
                self.message = self.font["font"]["m"].render(self.text, True, self.color)

            if self.alpha:
                self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                        self.message.get_size()[1] + self.padding * 2), pygame.SRCALPHA)
            else:
                self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                        self.message.get_size()[1] + self.padding * 2))
                
            self.surface.fill(self.background)
            self.surface.blit(self.message, (self.padding, self.padding))

            self.size = Vector2(self.surface.get_size())

        if sizer is not None:
            self.change(font_size = self.font_size, offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

        super().nodeChange(offset_str = offset_str, offset = offset, zindex = zindex, active = active)


    def kill(self):
        super().kill()

class ColorBlock(Node):
    def __init__(self, parentNode, size, color = Color(255, 255, 255, 255), zindex = 0, offset_str = None, offset = Vector2(0, 0), alpha_channel = False):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex)
    
        self.change(size = size, color = color, alpha_channel = alpha_channel, active = True)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        
    def draw(self, scale = Vector2(1, 1)):
        self.game.gameDraw(self.surface, self, scale)
        super().draw(scale)
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def change(self, size = None, color = None, alpha_channel = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if color is not None:
            self.color = color
        
        if alpha_channel is not None:
            self.alpha_channel = alpha_channel

        if self.alpha_channel:
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        elif size is not None:
            self.surface = pygame.Surface(self.size)
        
        if self.alpha_channel or size is not None or color is not None:
            self.surface.fill(self.color)
        
        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))
        
        
    
    def kill(self):
        super().kill()

class SpriteBlock(Node):
    def __init__(self, parentNode, size, image, angle : int = None, zindex = 0, offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = True)
        
        if angle is not None:
            self.change(image = image, angle = angle, offset_str = offset_str, offset = offset)
        else:
            self.angle = 0
            self.change(image = image)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, scale = Vector2(1, 1)):
        self.game.gameDraw(self.surface, self, scale)
        super().draw(scale)

    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def kill(self):
        super().kill()

    def change(self, image = None, size = None, angle = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if image is not None:
            self.orig_image = image
            self.orig_size = size
            self.surface = pygame.transform.scale(self.orig_image, self.size)

        elif size is not None:
            self.orig_size = size
            self.surface = pygame.transform.scale(self.orig_image, self.size)
            if self.angle != 0:
                angle = self.angle
        
        if angle is not None:
            self.angle = angle
            self.surface = pygame.transform.rotate(pygame.transform.scale(self.orig_image, self.orig_size), angle)
            
            super().nodeChange(size = Vector2(self.surface.get_size()), offset_str = offset_str, offset = offset)

        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

class AnimatedSpriteBlock(Node):
    def __init__(self, parentNode, size, framesArr, fps, angle = None, zindex = 0, offset_str = None, offset = pygame.Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset,  active = True)

        self.frames = []

        if angle is not None:
            self.change(frames_arr = framesArr, fps = fps, angle = angle, offset_str = offset_str, offset = offset)
        else:
            self.angle = 0
            self.change(frames_arr = framesArr, fps = fps)

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

    def draw(self, scale = Vector2(1, 1)):
        self.game.gameDraw(self.frame, self, scale)
        super().draw(scale)

    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

    def change(self, frames_arr = None, fps = None, angle = None, size = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if frames_arr is not None:
            self.frames.clear()
            for one_frame in frames_arr:
                frame = pygame.transform.scale(one_frame, self.size)
                self.frames.append(frame)
            
            self.frame = self.frames[0]
            
            self.count = 0
            self.index = 0
        
        if size is not None:
            temp = []
            for one_frame in self.frames:
                temp.append(pygame.transform.scale(one_frame, self.size))
            self.frames = list(temp)
        
        if fps is not None:
            self.fps = fps
        
        if angle is not None:
            self.angle = angle
            temp = []
            for one_frame in self.frames[:]:
                temp.append(pygame.transform.rotate(one_frame, angle))
            
            self.frames = temp
            super().nodeChange(size = self.frames[0].get_size(), offset_str = offset_str, offset = offset)
        
        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))
        
        self.frameLen = self.game.tick_speed // self.fps
        

    def kill(self):
        super().kill()

class TileMapBlock(Node):
    def __init__(self, parentNode, size, tile_node, coords, zindex = 0, offset_str=None, offset = pygame.Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
        
        self.change(tile_node = tile_node, coords = coords, active = True)


    def event(self, event):
        super().event(event)
    
    def update(self):
        
        super().update()

    def draw(self, scale = Vector2(1, 1)):
        self.game.gameDraw(self.surface, self, scale)
        super().draw(scale)

    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)

    def change(self, tile_node = None, coords = None, coords_change = None, size = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if tile_node is not None:
            self.tileNode = tile_node
    
        if coords is None:
            if coords_change is not None:
                if isinstance(coords_change, int):
                    new_x = int((self.coords[0] + coords_change) % self.tileNode.tileCount[0])
                    new_y = int((self.coords[1] + (self.coords[0] + coords_change) // self.tileNode.tileCount[0]) % self.tileNode.tileCount[1])
                else:
                    new_x = int((self.coords[0] + coords_change[0]) % self.tileNode.tileCount[0])
                    new_y = int((self.coords[1] + coords_change[1]) % self.tileNode.tileCount[1])
                self.coords = [new_x, new_y]
        else:
            self.coords = [int(coords[0] % self.tileNode.tileCount[0]), int(coords[1] % self.tileNode.tileCount[1])]
        
        self.surface = self.tileNode.grid[self.coords[0]][self.coords[1]]

        self.surface = pygame.transform.scale(self.surface, self.size)
    
        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))


    def kill(self):
        super().kill()

