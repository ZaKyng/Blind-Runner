import pygame
import os
from ZaKnode import *

from .. import lib 


class Level:
    def __init__(self, game : nodes.Game, settings_node, global_assets):
        self.name = "ingame_level"

        self.scene = nodes.Scene(self.name, game, bg_color = (150, 60, 105))

        self.level_name = None

        self.label = nodes.Label(self.scene, "none", "main", "xl", offset_str = "top")

        self.pause_menu = lib.PauseMenu(self.scene, self, self.level_name, settings_node, self.name, "levels")

        self.level = lib.GameLevel(self.scene, global_assets, self.finish)

        # --- TEMP --- #
        lib.ButtonText(self.pause_menu.pause_menu, "Finish", "main", self.finish, offset_str = "bottom-right", offset = (-20, -20))

        # --- ---- --- #


    def load(self, name):
        self.pause_menu.update(name)
        self.pause_menu.change(active = False)
        self.level_name = name

        level_data = resources.ReadData(self.scene.game.directory("test-levels.txt"), name)
        
        self.label.change(text = str(name))


    def finish(self):
        level_data = resources.ReadData(self.scene.game.directory("test-levels.txt"), self.level_name)
        level_data["finished"] = True
        resources.SaveData(self.scene.game.directory("test-levels.txt"), self.level_name, level_data)
        
        for unlocked_id in level_data["unlock"]:
            unlocked_level = resources.ReadData(self.scene.game.directory("test-levels.txt"), str(unlocked_id))

            if unlocked_level is not None and int(self.level_name) in unlocked_level["locked_by"]:
                unlocked_level["locked_by"].remove(int(self.level_name))
                resources.SaveData(self.scene.game.directory("test-levels.txt"), str(unlocked_id), unlocked_level)
    


