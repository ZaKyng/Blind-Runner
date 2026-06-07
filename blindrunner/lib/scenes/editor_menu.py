import pygame
import os
from ZaKnode import *

from ..lib import *


class PlayerLevels:
    def __init__(self, game : nodes.Game, play_node, edit_node, global_assets):
        self.name = "editor_menu"
        self.play_node = play_node
        self.edit_node = edit_node
        self.global_assets = global_assets

        self.gap = 60
        self.button_size = (1250, 125)

        self.buttons_list = []

        self.scene = nodes.Scene(self.name, game, bg_color = (0, 0, 0), onEntry = self.enterScene, onExit = self.exitScene)

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene("menu"))

        self.background = nodes.ColorBlock(self.scene, (self.scene.size.x, self.scene.size.y  ), color = (9, 37, 12))
        drag_collision = nodes.CollisionArea(self.background, 13)
        drag_collision.addCollisionBlock(self.background.size)
        self.drag_move = modifiers.MouseDragMove(self.background, 13, "y")
        modifiers.ForeverDo(self.background, self.snapBackground)

        self.label = nodes.Label(self.background, "Your levels:", "main", "xl", offset_str = "top", offset = (0, self.gap))

        self.add_button = Button(self.background, self.button_size, self.global_assets["add_button"].image, func = self.edit, offset_str = "center")

    def enterScene(self):
        self.drag_move.mouse_clicked = False
        self.drag_move.change(active = True)

        self.load()
        
    def exitScene(self):
        self.drag_move.mouse_clicked = False
        self.drag_move.change(active = False)

    def load(self):
        for button in self.buttons_list[:]:
            button.body.kill()

        offset_y = self.gap + self.label.size.y + self.gap

        levels_folder = self.scene.game.directory("player_levels")

        last_y_size = 0

        for file_name in os.listdir(levels_folder):
            level_data = resources.ReadData(levels_folder + "/" + file_name)
            last_level = levelButton(self, file_name, offset_y, level_data.get("tile_set", 0), level_data.get("finished", False), level_data.get("possible", False), self.global_assets)
            self.buttons_list.append(last_level)
            last_y_size = last_level.body.size.y
            offset_y += last_level.body.size.y + self.gap

        self.add_button.origin.change(offset_str = "top", offset = (0, offset_y + self.button_size[1] / 2))

        offset_y += last_y_size + self.gap
        
        self.background.change(size = (self.background.size.x, max(offset_y + self.gap, self.background.game.vh * 120)))
        self.background.collision[0].collision_blocks[0].change(size = self.background.size)
    
    def playLevel(self, name):
        self.play_node.load(name)
        self.scene.game.scenes.changeScene("player_level")

    def edit(self, name = None):
        self.edit_node.load(name)
        self.scene.game.scenes.changeScene("level_editor")
    

    def snapBackground(self):
        speed = 2000 * self.background.game.delta

        if self.background.offset.y > 0:
            self.background.change(offset = self.background.offset - pygame.Vector2(0, speed))
            return
        
        if self.background.offset.y < -self.background.size.y + self.background.game.orig_screen_size.y:
            self.background.change(offset = self.background.offset + pygame.Vector2(0, speed))


    
    
class levelButton:
    def __init__(self, window, file_name, offset_y, tile_set : int, finished : bool, possible : bool, global_assets):
        if possible:
            possible_str = "possible"
            possible_color = (0, 255, 0)
        else:
            possible_str = "impossible"
            possible_color = (200, 200, 200)

        self.body = nodes.SpriteBlock(window.background, window.button_size, global_assets["level_card"].image, offset_str = "top", offset = (0, offset_y))
        nodes.SpriteBlock(self.body, (80, 80), global_assets["levels"]["unlocked"].grid[tile_set][0], offset_str = "left", offset = (20, 0))

        label_text = file_name.removesuffix(".txt").upper()
        label_text = label_text.replace("_", " ")

        nodes.Label(self.body, label_text, "main", "m", offset_str = "left", offset = (120, 10))
        nodes.Label(self.body, possible_str, "main", "xs", color = possible_color, offset_str = "bottom-right", offset = (-380, 20))

        if finished:
            nodes.SpriteBlock(self.body, (90, 60), global_assets["levels"]["check"].image, offset_str = "bottom-right", offset = (20, 18))

        Button(self.body, (160, 80), global_assets["buttons"].grid[4][0], lambda: window.playLevel(file_name), offset_str = "right", offset = (-290, 0))
        Button(self.body, (160, 80), global_assets["buttons"].grid[5][0], lambda: window.edit(file_name), offset_str = "right", offset = (-110, 0))

