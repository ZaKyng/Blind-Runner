import pygame
import os
from ZaKnode import *

from ..lib import *


class Level:
    def __init__(self, game : nodes.Game):
        self.scene = nodes.Scene("level", game, bg_color = (150, 60, 105))

        self.name = None
        self.label = nodes.Label(self.scene, "none", "main", "xl", offset_str = "top")

        self.pause_menu = nodes.ColorBlock(self.scene, self.scene.size, color = (0, 0, 0, 200), zindex = 10, alpha_channel = True)
        nodes.Label(self.pause_menu, "Paused", "main", "xl", offset_str = "center", offset = (0, -300))
        ButtonText(self.pause_menu, "Return", "main", lambda: self.pause_menu.change(active = self.pause_menu.active == False), white_txt = False, offset_str = "center", offset = (-200, 0))
        ButtonText(self.pause_menu, "Reset", "main", lambda: self.load(self.name), white_txt = False, offset_str = "center")
        ButtonText(self.pause_menu, "Leave", "main", lambda: game.scenes.changeScene("levels"), white_txt = False, offset_str = "center", offset = (200, 0))
        self.pause_menu.change(active = False)

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: self.pause_menu.change(active = self.pause_menu.active == False))

        # --- TEMP --- #
        ButtonText(self.pause_menu, "Finish", "main", self.finish, offset_str = "bottom-right", offset = (-20, -20))

        # --- ---- --- #


    def load(self, name):
        self.pause_menu.change(active = False)
        self.name = name

        level_data = resources.ReadData(self.scene.game.directory("test-levels.txt"), name)
        
        self.label.change(text = str(name))


    def finish(self):
        level_data = resources.ReadData(self.scene.game.directory("test-levels.txt"), self.name)
        level_data["finished"] = True
        resources.SaveData(self.scene.game.directory("test-levels.txt"), self.name, level_data)
        
        for unlocked_id in level_data["unlock"]:
            unlocked_level = resources.ReadData(self.scene.game.directory("test-levels.txt"), str(unlocked_id))

            if unlocked_level is not None and int(self.name) in unlocked_level["locked_by"]:
                unlocked_level["locked_by"].remove(int(self.name))
                resources.SaveData(self.scene.game.directory("test-levels.txt"), str(unlocked_id), unlocked_level)
    


