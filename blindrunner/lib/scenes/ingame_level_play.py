import pygame
import os
from ZaKnode import *

from .. import lib 


class Level:
    def __init__(self, game : nodes.Game, settings_node, global_assets):
        self.name = "ingame_level"

        self.scene = nodes.Scene(self.name, game, bg_color = (32, 32, 32))

        self.level_name = None
        self.label = nodes.Label(self.scene, "none", "main", "xl", offset_str = "top", offset = (0, 20),  zindex = 100)

        self.level = lib.GameLevel(self.scene, global_assets, self.finish, settings_node, self.name, self.level_name, self, "editor_menu")


    def load(self, name):
        self.level.pause_menu.update(name)
        self.level.pause_menu.change(active = False)
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
    


