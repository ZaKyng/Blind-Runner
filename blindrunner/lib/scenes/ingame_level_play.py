import pygame
import os
from ZaKnode import *

from .. import lib 


class Level:
    def __init__(self, game : nodes.Game, settings_node, global_assets):
        self.name = "ingame_level"

        self.scene = nodes.Scene(self.name, game, bg_color = (32, 32, 32))

        self.level_name = None

        self.level = lib.GameLevel(self.scene, global_assets, self.finish, settings_node, self.name, self.level_name, self, "levels")


    def load(self, name):
        self.level_name = name

        self.level.load(self.scene.game.directory("player_levels/" + name), name)


    def finish(self):
        level_dir = self.scene.game.directory("ingame_levels/" + str(self.level_name))
        level_data = resources.ReadData(level_dir)

        if level_data["finished"]:
            return

        resources.SaveData(level_dir, "finished", True)
        
        for unlocked_level_name in level_data["unlocks"]:
            unlocked_url = self.scene.game.directory(f"ingame_levels/{unlocked_level_name}.txt")
            unlocked_level = resources.ReadData(unlocked_url)

            level_name = str(self.level_name).removesuffix(".txt")

            if unlocked_level is not None and level_name in unlocked_level["locked_by"]:
                unlocked_level["locked_by"].remove(level_name)
                resources.SaveData(unlocked_url, "locked_by", unlocked_level["locked_by"])
    


