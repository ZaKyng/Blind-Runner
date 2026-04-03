import pygame
import os
from ZaKnode import *

from ..lib import *


class Level:
    def __init__(self, game : nodes.Game):
        self.scene = nodes.Scene("level", game, bg_color = (150, 60, 105))

        self.name = None
        self.label = nodes.Label(self.scene, "none", "main", "xl", offset_str = "top")

        # --- TEMP --- #
        ButtonText(self.scene, "Finish", "main", self.finish, offset_str = "center")

        # --- ---- --- #


    def load(self, name):
        self.name = name

        level_data = resources.ReadData(self.scene.game.directory("test-levels.txt"), name)
        
        self.label.change(text = str(name))


    def finish(self):
        level_data = resources.ReadData(self.scene.game.directory("test-levels.txt"), self.name)
        level_data["finished"] = True
        
        for unlocked_id in level_data["unlock"]:
            unlocked_level = resources.ReadData(self.scene.game.directory("test-levels.txt"), str(unlocked_id))

            if unlocked_level is not None and int(self.name) in unlocked_level["locked_by"]:
                unlocked_level["locked_by"].remove(int(self.name))
                resources.SaveData(self.scene.game.directory("test-levels.txt"), str(unlocked_id), unlocked_level)


