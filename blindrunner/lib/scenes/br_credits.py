from ZaKnode import *
import pygame


class Credits:
    def __init__(self, game, global_assets):
        self.name = "credits"

        self.scene = nodes.Scene(self.name, game)

        self.title = nodes.Label(self.scene, "Credits", "main", "l", offset_str = "top", offset = (0, 70))
        self.text = []
        self.text.append(nodes.BaseNode(self.scene, offset_str = "top", offset = (0, 180)))
        nodes.Label(self.text[-1], "Made by:", "main", "m", color = (190, 190, 190), offset = (-260, 0))
        nodes.Label(self.text[-1], "ZaKyng", "main", "l", offset = (0, 0))

        self.text.append(nodes.BaseNode(self.scene, offset_str = "top", offset = (0, 270)))

        nodes.Label(self.text[-1], "Drawn by:", "main", "m", color = (190, 190, 190), offset = (-280, 0))
        nodes.Label(self.text[-1], "ZaKyng", "main", "l", offset = (0, 0))

        self.text.append(nodes.BaseNode(self.scene, offset_str = "top", offset = (0, 360)))

        nodes.Label(self.text[-1], "Drawn in:", "main", "m", color = (190, 190, 190), offset = (-260, 0))
        nodes.Label(self.text[-1], "Piskel", "main", "l", offset = (20, 0))
        nodes.SpriteBlock(self.text[-1], (50, 50), global_assets["arrows"].grid[0][18], offset = (240, 0))

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene("settings"))
    

class Final:
    def __init__(self, game, global_assets):
        self.name = "thanks"

        self.scene = nodes.Scene(self.name, game)

        self.title = nodes.Label(self.scene, "Thanks", "main", "l", color = (190, 190, 190), offset_str = "top", offset = (0, 70))
        self.text = []
        self.text.append(nodes.Label(self.scene, "  In the beginning, Blind Runner was only a thought,\n but now you finished it. \nThank you so much for finishing it and I hope you liked it.", "main", "m", offset_str = "top", offset = (0, 300)))
        self.text.append(nodes.Label(self.scene, "ZaKyng", "main", "l", color = (190, 190, 190), offset_str = "top", offset = (0, 800)))

        self.sprite_box = nodes.BaseNode(self.scene, offset = (360, 600))

        self.sprites = []
        self.sprites.append(nodes.AnimatedSpriteBlock(self.sprite_box, (120, 120), global_assets["animations"][0]["player"]["finish"].frames, 18, offset = (-300, 0)))

        for i in range(4):
            self.sprites.append(nodes.AnimatedSpriteBlock(self.sprite_box, (120, 120), global_assets["animations"][i]["g_enemy"]["run"]["right"].frames, 15, offset = (i * 380, 0)))
            self.sprites.append(nodes.AnimatedSpriteBlock(self.sprite_box, (120, 120), global_assets["animations"][i]["f_enemy"]["idle"]["right"].frames, 20, offset = (i * 380 + 190, 0)))
        
        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene("menu"))