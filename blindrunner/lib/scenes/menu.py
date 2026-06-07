import pygame
from ZaKnode import *
from ..lib import *






class Menu:
    def __init__(self, game, settings_node, global_assets):
        self.name = "menu"

        self.scene = nodes.Scene(self.name, game, bg_color = (2, 2, 2))

        game.fonts.addFont("giga_main", game.directory("assets/font_utendo_a.ttf"), 10)

        self.title = nodes.Label(self.scene, "Blind Runner", "giga_main", "xl", offset_str = "top", offset = (-280, 80))

        self.background = nodes.SpriteBlock(self.scene, (self.scene.size[0] * 0.98, self.scene.size[1] * 0.98), global_assets["backgrounds"][0].image, offset_str = "center", zindex = -50)

        nodes.AnimatedSpriteBlock(self.scene, (500, 500), global_assets["animations"][0]["player"]["idle"]["right"].frames, 4, offset_str = "left",offset = (160, 60))



        self.buttons = nodes.BaseNode(self.scene, offset_str = "center", offset = (520, -300))
        self.sprites = global_assets["buttons"]
        self.button_list = []
        funcs = [lambda: game.scenes.changeScene("levels"), lambda: game.scenes.changeScene("editor_menu"), lambda: settings_node.open(self.name), game.end]
        for i in range(4):
            self.button_list.append(Button(self.buttons, (300, 150), self.sprites.grid[i][0], funcs[i], higherBy = 12, offset = [0, i * 190]))


        modifiers.PressKey(self.scene, pygame.K_ESCAPE, game.end)




