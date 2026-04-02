import pygame
from ZaKnode import *




class Button:
    def __init__(self, parentNode, size, surface, func, higherBy = 6, offset_str = None, offset = (0, 0)):
        self.origin = nodes.BaseNode(parentNode, offset_str = offset_str, offset = offset)
        self.sprite = nodes.SpriteBlock(self.origin, size, surface, offset_str = "Center")
        self.collision = nodes.CollisionArea(self.origin, 1)
        self.collision.addCollisionBlock(size, offset_str = "center")
        modifiers.Hover(self.origin, 1, lambda: self.hoverReize((size[0] + higherBy, size[1] + (size[1] * higherBy / size[0] if size[0] != 0 else 0))), else_func = lambda: self.noHoverResize(size))
        modifiers.ClickObject(self.origin, 1, function = func, button = 1)
    
    def hoverReize(self, size):
        self.sprite.change(size = size, offset_str = "center")
        self.collision.children[0].change(size = size, offset_str = "center")

    
    def noHoverResize(self, size):
        self.sprite.change(size = size, offset_str = "center")
        self.collision.children[0].change(size = size, offset_str = "center")

class ButtonText:
    def __init__(self, parentNode, text, font_name, func, white_txt = True, button_down = False, offset_str = None, offset = (0, 0)):
        self.origin = nodes.BaseNode(parentNode, zindex = 4, offset_str = offset_str, offset = offset)
        self.sprite = nodes.TextBlock(self.origin, text, font_name, txt_color = (255, 255, 255) if white_txt else (0, 0, 0), bg_color = (0, 0, 0) if white_txt else (255, 255, 255), offset_str = "Center")
        self.collision = nodes.CollisionArea(self.origin, 1)
        self.collision.addCollisionBlock(self.sprite.size, offset_str = "center")
        modifiers.Hover(self.origin, 1, lambda: self.hoverResize("l"), else_func = lambda: self.hoverResize("m"))
        modifiers.ClickObject(self.origin, 1, function = func, button = 1, buttondown = button_down)
    
    def hoverResize(self, size):
        self.sprite.change(font_size = size, offset_str = "center")
        self.collision.children[0].change(size = self.sprite.size, offset_str = "center")

