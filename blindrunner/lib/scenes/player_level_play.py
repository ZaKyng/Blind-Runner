import pygame
import os
from ZaKnode import *

from .. import lib


class Level:
    def __init__(self, game : nodes.Game, settings_node, global_assets):
        self.name = "player_level"

        self.scene = nodes.Scene(self.name, game, bg_color = (32, 32, 32))

        self.level_name = None
        self.label = nodes.Label(self.scene, "none", "main", "xl", offset_str = "top", offset = (0, 20),  zindex = 100)

        self.pause_menu = lib.PauseMenu(self.scene, self, self.level_name, settings_node, self.name, "editor_menu")

        self.level = lib.GameLevel(self.scene, global_assets, self.finish)

        # --- TEMP --- #
        lib.ButtonText(self.pause_menu.pause_menu, "Finish", "main", self.finish, offset_str = "bottom-right", offset = (-20, -20))

        # --- ---- --- #


    def load(self, name):
        self.pause_menu.update(name)
        self.pause_menu.change(active = False)
        self.level_name = name

        self.level.load(self.scene.game.directory("player_levels/" + name))
        
        self.label.change(text = name.removesuffix(".txt"), offset_str = "top", offset = (0, 20), zindex = 100)
    
    def finish(self):
        print(str(self.level_name) + " is finished")


