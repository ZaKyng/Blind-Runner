import pygame
from ZaKnode import *
from ..lib import *






class Menu:
    def __init__(self, game):
        self.scene = nodes.Scene("menu", game, bg_color = (30, 64, 210))

        self.buttons = nodes.BaseNode(self.scene, offset_str = "center", offset = (520, -300))
        self.sprites = resources.SpriteSheet(game.directory("assets/buttons1.png"), (128, 64), alpha_channel = True)
        self.button_list = []
        funcs = [lambda: game.scenes.changeScene("levels"), lambda: game.scenes.changeScene("level_lib"), lambda: game.scenes.changeScene("settings"), game.end]
        for i in range(4):
            self.button_list.append(Button(self.buttons, (300, 150), self.sprites.grid[0][i], funcs[i], higherBy = 12, offset = [0, i * 190]))

        self.image = resources.Image(game.directory("assets/placeholder.png"), alpha_channel = True)
        self.image_node = nodes.SpriteBlock(self.scene, (800, 800), self.image.image, offset_str = "center", offset = (-300, 0))
        modifiers.AxisMove(self.image_node, start = self.image_node.offset.y - 20, end = self.image_node.offset.y + 20, axis = "y", speed = 10, mode = "ease-both", strength = 1.6)

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, game.end)




