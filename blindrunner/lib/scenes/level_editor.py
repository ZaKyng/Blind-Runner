import pygame
import os
from ZaKnode import *

from ..lib import *


class LevelEditor:
    def __init__(self, game : nodes.Game):
        self.scene = nodes.Scene("level_editor", game, bg_color = (150, 60, 105))

        modifiers.OnEventFunc(self.scene, self.nameChanger)

        self.level_node = EditorWindow(self.scene)

        self.name = None
        self.old_name = None
        self.changing_name = False
        
        self.little_label = nodes.Label(self.scene, "Editor", "main", "s", offset_str = "top", offset = (0, 0))
        self.label = nodes.Label(self.scene, "Editor", "main", "l", offset_str = "top", offset = (0, 50))
        nodes.CollisionArea(self.label, 18).addCollisionBlock((self.label.size[0] + 20, self.label.size[1] + 20), offset_str = "center")

        modifiers.ClickObject(self.label, 18, function = self.changeName, button = 1)

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, self.leave)

    def load(self, name):
        if isinstance(name, str):
            self.name = name
            level_data = resources.ReadData(self.scene.game.directory("player_levels/" + name))

            self.level_node.load(level_data)
        else:
            self.name = "new_level.txt"

        self.label.change(text = self.name.removesuffix(".txt"), offset_str = "top", offset = (0, 50))
        self.label.collision[0].change(size = self.label.size, offset_str = "center")
        self.label.collision[0].children[0].change(size = (self.label.size[0] + 20, self.label.size[1] + 20), offset_str = "center")
    
    def save(self):
        if self.name is None:
            return
        
        level_data = self.level_node.save()
        resources.WriteData(self.scene.game.directory("player_levels/" + self.name), level_data)

    def leave(self):
        self.save()
        self.scene.game.scenes.changeScene("editor_menu")

    def changeName(self):
        pygame.key.start_text_input()
        self.changing_name = True
        self.name = ""
        self.old_name = self.name
        self.label.change(color = (90, 190, 90))
    
    def nameChanger(self, event):
        if not self.changing_name:
            return
        
        update = False
        
        if event.type == pygame.TEXTINPUT:
            self.name += event.text
            self.name = self.name.strip()
            update = True
        elif event.type == pygame.KEYDOWN:
            update = True
            if event.key == pygame.K_RETURN:
                pygame.key.stop_text_input()
                self.changing_name = False
                while os.path.exists(self.scene.game.directory("player_levels/" + self.name + ".txt")):
                    self.name += "_"
                self.name += ".txt"
                if os.path.exists(self.scene.game.directory("player_levels/" + self.old_name)):
                    os.rename(self.scene.game.directory("player_levels/" + self.old_name), self.scene.game.directory("player_levels/" + self.name))
                self.label.change(color = (255, 255, 255))
                return
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
        
        if update:
            self.label.change(text = self.name, offset_str = "top", offset = (0, 50))
            self.label.collision[0].change(size = self.label.size, offset_str = "center")
            self.label.collision[0].children[0].change(size = (self.label.size[0] + 20, self.label.size[1] + 20), offset_str = "center")

class EditorWindow:
    def __init__(self, parentNode):
        self.parentNode = parentNode

        self.window = nodes.ColorBlock(parentNode, (parentNode.size[0], parentNode.size[1] - 140), color = (0, 0, 0, 200), alpha_channel = True, offset = (0, 140))

        self.block_picker = nodes.ColorBlock(self.window, (400, self.window.size[1]), color = (80, 80, 80), offset_str = "right")

    def load(self, level_data):
        self.level_data = level_data

    def save(self):
        return self.level_data