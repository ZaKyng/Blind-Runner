import pygame
import os
from ZaKnode import *

from .. import lib


class Level:
    def __init__(self, game : nodes.Game, settings_node, global_assets):
        self.name = "player_level"

        self.scene = nodes.Scene(self.name, game, bg_color = (32, 32, 32))

        self.level_name = None

        self.level = lib.GameLevel(self.scene, global_assets, self.finish, settings_node, self.name, self.level_name, self, "editor_menu")



    def load(self, name):
        self.level_name = name

        self.level.load(self.scene.game.directory("player_levels/" + name), name)
    
    def finish(self):
        resources.SaveData(self.scene.game.directory("player_levels/" + self.level_name), "finished", True)
        resources.SaveData(self.scene.game.directory("player_levels/" + self.level_name), "possible", True)



