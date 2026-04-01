import pygame
import os
from ZaKnode import *

from .lib import Button


class Levels:
    def __init__(self, game : nodes.Game, level_node):
        self.scene = nodes.Scene("levels", game, bg_color = (0, 0, 0))

        self.bg_image = resources.Image(game.directory("assets/background_test.png"))
        self.background = nodes.SpriteBlock(self.scene, (300 * game.vw, 200 * game.vh), self.bg_image.image)
        collision = nodes.CollisionArea(self.background, 12)
        collision.addCollisionBlock(self.background.size)
        modifiers.MouseDragMove(self.background, 12)
        modifiers.ForeverDo(self.background, self.snapBackground)

        unlocked = resources.SpriteSheet(game.directory("assets/level_icons.png"), [32, 32], alpha_channel = True)
        locked = resources.SpriteSheet(game.directory("assets/locked_icons.png"), [32, 32], alpha_channel = True)
        lock = resources.Image(game.directory("assets/lock.png"), alpha_channel = True)

        levels = resources.ReadData(game.directory("test-levels.txt"))
        for key in list(levels.keys()):
            oneLevel(self.background, key, level_node, levels[key], unlocked, locked, lock)

    def snapBackground(self):
        self.background.change(offset = pygame.Vector2(min(0, max(self.background.offset.x, self.scene.game.orig_screen_size.x - self.background.size.x)), min(0, max(self.background.offset.y, self.scene.game.orig_screen_size.y - self.background.size.y))))




class oneLevel:
    def __init__(self, parentNode, name, level_node, level_data, icons1, icons2, lock):
        self.level_node = level_node
        self.level_data = level_data
        self.origin = nodes.BaseNode(parentNode, offset = self.level_data["offset"])
        self.sprite = nodes.TileMapBlock(self.origin, (self.origin.game.vh * 15, self.origin.game.vh * 15), icons1, [self.level_data["icon"], 0], offset_str = "center")
        self.collision = nodes.CollisionArea(self.origin, 7)
        self.collision.addCollisionBlock(self.sprite.size - pygame.Vector2(0, self.sprite.size.y / 16 * 2), offset_str = "center")
        self.collision.addCollisionBlock(self.sprite.size - pygame.Vector2(self.sprite.size.y / 16 * 2, 0), offset_str = "center")

        self.click_modifier = modifiers.ClickObject(self.origin, 7, lambda: self.enterLevel(name), button = 1)

        if self.level_data["locked"]:
            self.sprite.change(tile_node = icons2)
            self.click_modifier.change(func = self.clickLocked)

            self.lock_node = nodes.SpriteBlock(self.origin, [self.origin.game.vh * 8, self.origin.game.vh * 8], pygame.transform.hsl(lock.image, lightness = 0.3), zindex = 1, offset_str = "center")

            self.lock_move = modifiers.AxisMove(self.lock_node, self.lock_node.offset.x - 10, self.lock_node.offset.x + 10, speed = 175)
            self.lock_move.change(active = False)

            self.timer = modifiers.Timer(self.lock_node, 0.3, self.resetLock)
    
    def enterLevel(self, name):
        self.level_node.load(name)
        self.origin.game.scenes.changeScene("level")
            
    def clickLocked(self):
        self.resetLock()
        self.lock_move.change(active = True, start = self.lock_node.offset.x - 10, end = self.lock_node.offset.x + 10)
        self.timer.start()
        
    def resetLock(self):
        self.lock_move.change(active = False)
        self.lock_node.change(offset_str = "center")
    


