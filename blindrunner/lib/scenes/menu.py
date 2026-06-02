import pygame
from ZaKnode import *
from ..lib import *






class Menu:
    def __init__(self, game, settings_node, global_assets):
        self.name = "menu"

        self.scene = nodes.Scene(self.name, game, bg_color = (130, 50, 50))

        self.buttons = nodes.BaseNode(self.scene, offset_str = "center", offset = (520, -300))
        self.sprites = global_assets["buttons"]
        self.button_list = []
        funcs = [lambda: game.scenes.changeScene("levels"), lambda: game.scenes.changeScene("editor_menu"), lambda: settings_node.open(self.name), game.end]
        for i in range(4):
            self.button_list.append(Button(self.buttons, (300, 150), self.sprites.grid[i][0], funcs[i], higherBy = 12, offset = [0, i * 190]))

        self.image = resources.Image(game.directory("assets/placeholder.png"), alpha_channel = True)
        self.image_node = nodes.SpriteBlock(self.scene, (800, 800), self.image.image, offset_str = "center", offset = (-300, 0))
        modifiers.AxisMove(self.image_node, start = self.image_node.offset.y - 20, end = self.image_node.offset.y + 20, axis = "y", speed = 10, mode = "ease-both", strength = 1.6)

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, game.end)




