import pygame
import os
from ZaKnode import *

from ..lib import *


class PlayerLevels:
    def __init__(self, game : nodes.Game):
        self.scene = nodes.Scene("level_lib", game, bg_color = (30, 176, 57))


        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene("menu"))



    def load(self, name):
        self.pause_menu.change(active = False)
        self.name = name

        level_data = resources.ReadData(self.scene.game.directory("test-levels.txt"), name)
        
        self.label.change(text = str(name))


