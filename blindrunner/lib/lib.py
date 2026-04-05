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
    def __init__(self, parentNode, text, font_name, func, white_txt = True, button_down = True, offset_str = None, offset = (0, 0)):
        self.offset_str = offset_str
        self.origin = nodes.BaseNode(parentNode, zindex = 4, offset_str = offset_str, offset = offset)
        self.sprite = nodes.TextBlock(self.origin, text, font_name, txt_color = (255, 255, 255) if white_txt else (0, 0, 0), bg_color = (0, 0, 0) if white_txt else (255, 255, 255), offset_str = offset_str)
        self.collision = nodes.CollisionArea(self.origin, 1)
        self.collision.addCollisionBlock(self.sprite.size, offset_str = offset_str)
        modifiers.Hover(self.origin, 1, lambda: self.hoverResize("l"), else_func = lambda: self.hoverResize("m"))
        self.click_mod = modifiers.ClickObject(self.origin, 1, function = func, button = 1, buttondown = button_down)
    
    def hoverResize(self, size):
        self.sprite.change(font_size = size, offset_str = self.offset_str)
        self.collision.children[0].change(size = self.sprite.size, offset_str = self.offset_str)


class PauseMenu:
    def __init__(self, parentNode, level_node, name, settings_node, scene_name, parent_scene_name):
        self.level_node = level_node

        self.pause_menu = nodes.ColorBlock(parentNode, parentNode.size, color = (0, 0, 0, 200), zindex = 100, alpha_channel = True)

        nodes.Label(self.pause_menu, "Paused", "main", "xl", offset_str = "center", offset = (0, -300))
        ButtonText(self.pause_menu, "Return", "main", lambda: self.change(active = self.pause_menu.active == False), white_txt = False, offset_str = "center", offset = (-330, 0))
        self.reset_button = ButtonText(self.pause_menu, "Reset", "main", lambda: self.level_node.load(name), white_txt = False, offset_str = "center", offset = (-130, 0))
        ButtonText(self.pause_menu, "Settings", "main", lambda: settings_node.open(scene_name), white_txt = False, offset_str = "center", offset = (105, 0))
        ButtonText(self.pause_menu, "Leave", "main", lambda: parentNode.game.scenes.changeScene(parent_scene_name), white_txt = False, offset_str = "center", offset = (330, 0))

        self.pause_menu.change(active = False)

        modifiers.PressKey(parentNode, pygame.K_ESCAPE, lambda: self.change(active = self.pause_menu.active == False))
    
    def change(self, active = False):
        self.pause_menu.change(active = active)
    
    def update(self, name):
        self.reset_button.click_mod.change(func = lambda: self.level_node.load(name))


