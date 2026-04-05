import pygame
import os
from ZaKnode import *

from ..lib import *


class PlayerLevels:
    def __init__(self, game : nodes.Game, play_node, edit_node):
        self.name = "editor_menu"
        self.play_node = play_node
        self.edit_node = edit_node

        self.gap = 60
        self.button_size = (65 * game.vw, 12 * game.vh)

        self.scene = nodes.Scene(self.name, game, bg_color = (0, 0, 0), onEntry = self.enterScene, onExit = self.exitScene)

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene("menu"))

        self.background = nodes.ColorBlock(self.scene, (self.scene.size.x, self.scene.size.y  ), color = (9, 37, 12))
        drag_collision = nodes.CollisionArea(self.background, 13)
        drag_collision.addCollisionBlock(self.background.size)
        self.drag_move = modifiers.MouseDragMove(self.background, 13, "y")
        modifiers.ForeverDo(self.background, self.snapBackground)

        self.label = nodes.Label(self.background, "Your levels:", "main", "xl", offset_str = "top", offset = (0, self.gap))

        temp_surface = pygame.Surface(self.button_size)
        temp_surface.fill((30, 40, 170))
        self.add_button = Button(self.background, self.button_size, temp_surface, func = self.edit, offset_str = "center")
        nodes.Label(self.add_button.origin, "Create new", "main", zindex = 5, offset_str = "center")

    def enterScene(self):
        self.drag_move.mouse_clicked = False
        self.drag_move.change(active = True)

        self.load()
        
    def exitScene(self):
        self.drag_move.mouse_clicked = False
        self.drag_move.change(active = False)

    def load(self):
        offset_y = self.gap + self.label.size.y + self.gap

        levels_folder = self.scene.game.directory("player_levels")

        for file_name in os.listdir(levels_folder):
            last_level = levelButton(self, file_name, offset_y)
            offset_y += last_level.body.size.y + self.gap

        self.add_button.origin.change(offset_str = "top", offset = (0, offset_y + self.button_size[1] / 2))

        offset_y += last_level.body.size.y + self.gap
        
        self.background.change(size = (self.background.size.x, max(offset_y + self.gap, self.background.game.vh * 100)))
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
    def __init__(self, window, file_name, offset_y):
        self.body = nodes.ColorBlock(window.background, window.button_size, (60, 140, 45), offset_str = "top", offset = (0, offset_y))
        nodes.Label(self.body, file_name.removesuffix(".txt"), "main", "m", offset_str = "left", offset = (30, 0))
        ButtonText(self.body, "Play", "main", lambda: window.playLevel(file_name), offset_str = "right", offset = (-220, 0))
        ButtonText(self.body, "Edit", "main", lambda: window.edit(file_name), offset_str = "right", offset = (-50, 0))

