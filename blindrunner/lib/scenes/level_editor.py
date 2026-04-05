import pygame
import os
from ZaKnode import *

from ..lib import *


class LevelEditor:
    def __init__(self, game : nodes.Game):
        self.scene = nodes.Scene("level_editor", game, bg_color = (150, 60, 105))

        self.name = None
        self.label = nodes.Label(self.scene, "Editor", "main", "xl", offset_str = "top")

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: self.scene.game.scenes.changeScene("editor_menu"))



    def load(self, name):
        if isinstance(name, str):
            self.name = name
            level_data = resources.ReadData(self.scene.game.directory("player_levels/" + name))


        else:
            self.name = "new_level.txt"

        self.label.change(text = "Editing " + self.name.removesuffix(".txt"), offset_str = "top")
    


