from platform import node

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


class PlayerMove(base.Modifier):
    def __init__(self, parentNode, colide_with : int, self_layers : int = None, die_layer : int = None, speed = 60, gravity = 10, jump_power = 35):
        super().__init__(parentNode)

        self.direction = pygame.Vector2(0, 0)
        self.jump = False
        self.on_ground = False

        if self_layers is None:
            self.self_colide = self.self_collide_all
        self.change(colide_with, self_layers, die_layer, speed, gravity, jump_power, active = True)

    def event(self, event):
        a_pressed = False
        d_pressed = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump = True
            elif event.key == pygame.K_a:
                a_pressed = True
            elif event.key == pygame.K_d:
                d_pressed = True
        
        self.direction.x = (d_pressed - a_pressed) if (a_pressed or d_pressed) else 0
        super().event(event)
    
    def update(self):
        offset_change = pygame.Vector2(0, 0)

        if self.direction.x != 0:
            offset_change.x = self.direction.x * self.speed * self.parentNode.game.delta_time
            offset_change = self.collide_x(offset_change)

        if self.jump and self.on_ground:
            self.on_ground = False
            offset_change.y -= self.jump_power
        
        offset_change.y += self.gravity * self.parentNode.game.delta_time
        offset_change = self.collide_y(offset_change)

        self.parentNode.change(offset = self.parentNode.offset + offset_change)
        super().update()

    def draw(self, scale = pygame.Vector2(1, 1)):
        super().draw(scale)

    def change(self, colide_with : int = None, self_layers : list = None, die_layer : int = None, speed = None, gravity = None, jump_power = None, active : bool = None):

        if colide_with is not None:
            self.physics_check = colide_with

        if self_layers is not None:
            self.self_colide_list = list(self_layers)
            self.self_colide = self.self_collide_check

        if die_layer is not None:
            self.die_layer = die_layer

        if speed is not None:
            self.speed = speed

        if gravity is not None:
            self.gravity = gravity

        if jump_power is not None:
            self.jump_power = jump_power

        super().modifierChange(active = active)

    def kill(self):
        super().kill()

    def self_collide_all(self, physics_layer):
        return True

    def self_collide_check(self, physics_layer):
        return physics_layer in self.self_colide_list

    def collide_x(self, offset_change):
        new_change = offset_change
        for node in self.game.scenes.scenes[self.game.scenes.current_scene].nodes:
            if node.physics_layer != self.physics_check:
                pass
            for ownHitBox in self.parentNode.collision:
                if self.self_colide(ownHitBox.physics_layer):
                    pass
                for targetHB in node.hitBoxes:
                    targetHB.update()
                    if ownHitBox.rect.colliderect(targetHB.rect):
                        if offset_change.x > 0: # Moving right
                            new_change.x = targetHB.rect.left - ownHitBox.size[0] - ownHitBox.offset[0] - self.parentNode.position[0]
                        elif offset_change.x < 0: # Moving left
                            new_change.x = targetHB.rect.right - ownHitBox.offset[0] - self.parentNode.position[0]
                    ownHitBox.update()
        return new_change
    
    def collide_y(self, offset_change):
        new_change = offset_change
        for node in self.game.scenes.scenes[self.game.scenes.current_scene].nodes:
            if node.physics_layer != self.physics_check:
                pass
            for ownHitBox in self.parentNode.collision:
                if self.self_colide(ownHitBox.physics_layer):
                    pass
                for targetHB in node.hitBoxes:
                    targetHB.update()
                    if ownHitBox.rect.colliderect(targetHB.rect):
                        if offset_change.y > 0: # Moving down
                            new_change.y = targetHB.rect.top - ownHitBox.size[1] - ownHitBox.offset[1] - self.parentNode.position[1]
                            self.on_ground = True
                        elif offset_change.y < 0: # Moving up
                            new_change.y = targetHB.rect.bottom - ownHitBox.offset[1] - self.parentNode.position[1]
                    ownHitBox.update()
        return new_change