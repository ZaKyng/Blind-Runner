from ZaKnode import *
import pygame


class Support:
    def __init__(self, game, global_assets):
        self.name = "support"

        self.scene = nodes.Scene(self.name, game, bg_color = (23, 23, 23))

        self.title = nodes.Label(self.scene, "Support", "main", "l", offset_str = "top", offset = (0, 40))
        spacer1 = nodes.ColorBlock(self.scene, (1600, 5), (120, 120, 120), offset_str = "top", offset = (0, 140))
        self.parts = []
        self.parts.append(nodes.BaseNode(self.scene, offset_str = "top", offset = (0, 180)))
        nodes.Label(self.parts[-1], "Controls", "main", "m", color = (190, 190, 190), offset_str = "top", offset = (0, 0))
        line = nodes.BaseNode(self.parts[-1], offset = (-300, 90))
        tile_size = 60
        nodes.SpriteBlock(line, (tile_size, tile_size), global_assets["arrows"].grid[0][15])
        nodes.SpriteBlock(line, (tile_size, tile_size), global_assets["arrows"].grid[0][16], offset = (tile_size, 0))
        nodes.SpriteBlock(line, (tile_size, tile_size), global_assets["arrows"].grid[0][12], offset = (2.5 * tile_size, 0))
        nodes.SpriteBlock(line, (tile_size, tile_size), global_assets["arrows"].grid[0][0], offset = (4 * tile_size, 0))
        nodes.Label(line, "- JUMP", "main", "l", offset = (5.5 * tile_size, 0))

        line = nodes.BaseNode(self.parts[-1], offset = (-300, 180))
                              
        nodes.SpriteBlock(line, (tile_size, tile_size), global_assets["arrows"].grid[0][13])
        nodes.SpriteBlock(line, (tile_size, tile_size), global_assets["arrows"].grid[0][3], offset = (1.5 * tile_size, 0))
        nodes.Label(line, "- LEFT", "main", "l", offset = (3 * tile_size, 0))

        line = nodes.BaseNode(self.parts[-1], offset = (-300, 270))
                              
        nodes.SpriteBlock(line, (tile_size, tile_size), global_assets["arrows"].grid[0][14])
        nodes.SpriteBlock(line, (tile_size, tile_size), global_assets["arrows"].grid[0][2], offset = (1.5 * tile_size, 0))
        nodes.Label(line, "- RIGHT", "main", "l", offset = (3 * tile_size, 0))

        spacer2 = nodes.ColorBlock(self.scene, (1600, 5), (120, 120, 120), offset_str = "top", offset = (0, 570))

        self.parts.append(nodes.BaseNode(self.scene, offset_str = "top", offset = (0, 740)))
        nodes.Label(self.parts[-1], "Logic", "main", "m", color = (190, 190, 190), offset_str = "top", offset = (0, -100))

        nodes.SpriteBlock(self.parts[-1], (450, 225), global_assets["buttons"].grid[12][0], offset_str = "center", offset = (-320, 0))
        nodes.SpriteBlock(self.parts[-1], (450, 225), global_assets["buttons"].grid[13][0], offset_str = "center", offset = (320, 0))

        spacer3 = nodes.ColorBlock(self.scene, (1600, 5), (120, 120, 120), offset_str = "top", offset = (0, 880))

        self.parts.append(nodes.BaseNode(self.scene, offset_str = "top", offset = (0, 910)))
        nodes.Label(self.parts[-1], "Naming", "main", "m", color = (190, 190, 190), offset_str = "top", offset = (0, 0))
        nodes.Label(self.parts[-1], "In level name '_' translates to Space", "main", "m", offset_str = "top", offset = (0, 80))

        

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene("settings"))