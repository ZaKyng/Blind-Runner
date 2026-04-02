import pygame
import os
from ZaKnode import *

from ..lib import Button


class Level:
    def __init__(self, game : nodes.Game):
        self.scene = nodes.Scene("level", game, bg_color = (150, 60, 105))

    def load(self, name):
        level_data = resources.ReadData(self.scene.game.directory("test-levels.txt"), name)


