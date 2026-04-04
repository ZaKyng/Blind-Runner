import pygame
import os
from ZaKnode import *

from ..lib import Button


class Levels:
    def __init__(self, game : nodes.Game, level_node):
        self.scene = nodes.Scene("levels", game, bg_color = (0, 0, 0))

        self.bg_image = resources.Image(game.directory("assets/blindrunner-map.png"))
        self.background = nodes.SpriteBlock(self.scene, (296 * game.vh, 184 * game.vh), self.bg_image.image, offset = (-20 * game.vh, -20 * game.vh))
        self.background_limits = [[self.background.offset.x, game.orig_screen_size.x - self.background.size.x - self.background.offset.x], [self.background.offset.y, game.orig_screen_size.y - self.background.size.y - self.background.offset.y]]
        collision = nodes.CollisionArea(self.background, 12)
        collision.addCollisionBlock(self.background.size)
        self.drag_move = modifiers.MouseDragMove(self.background, 12)
        modifiers.ForeverDo(self.background, self.snapBackground)
        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene("menu"))

        self.scene.change(onEntry = self.enterScene, onExit = self.exitScene)

        unlocked = resources.SpriteSheet(game.directory("assets/level-icons.png"), [32, 32], alpha_channel = True)
        locked = resources.SpriteSheet(game.directory("assets/locked-icons.png"), [32, 32], alpha_channel = True)
        check = resources.Image(game.directory("assets/level-check.png"), alpha_channel = True)
        lock = resources.Image(game.directory("assets/lock.png"), alpha_channel = True)

        self.level_array = []
        levels = resources.ReadData(game.directory("test-levels.txt"))
        if levels is not None and len(levels) > 0:
            for key in list(levels.keys()):
                self.level_array.append(oneLevel(self.background, key, level_node, unlocked, locked, check, lock))

    def snapBackground(self):
        outside = False
        speed = 2000 * self.background.game.delta
        new_offset = self.background.offset
        if self.background_limits[0][0] < self.background.offset.x:
            new_offset.x -= speed
            outside = True
        elif self.background.offset.x < self.background_limits[0][1]:
            new_offset.x += speed
            outside = True

        if self.background_limits[1][0] < self.background.offset.y:
            new_offset.y -= speed
            outside = True
        elif self.background.offset.y < self.background_limits[1][1]:
            new_offset.y += speed
            outside = True

        if outside:
            self.background.change(offset = new_offset)


    def enterScene(self):
        self.drag_move.mouse_clicked = False
        self.drag_move.change(active = True)

        for level in self.level_array:
            level.update()
        
    def exitScene(self):
        self.drag_move.mouse_clicked = False
        self.drag_move.change(active = False)



class oneLevel:
    def __init__(self, parentNode, name, level_node, icons1, icons2, check, lock):
        self.parentNode = parentNode
        self.level_node = level_node
        self.name = name
        self.icons = [icons1, icons2]
        self.lock = lock

        level_data = resources.ReadData(self.parentNode.game.directory("test-levels.txt"), str(self.name))
        self.origin = nodes.BaseNode(parentNode, offset = [level_data["offset"][0] * self.parentNode.game.vh, level_data["offset"][1] * self.parentNode.game.vh,])
        
        self.click_modifier = modifiers.ClickObject(self.origin, 7, lambda: self.enterLevel(name), button = 1)
        self.sprite = nodes.TileMapBlock(self.origin, (self.origin.game.vh * 15, self.origin.game.vh * 15), icons1, [level_data["icon"], 0], offset_str = "center")

        self.check = nodes.SpriteBlock(self.origin, (self.origin.game.vh * 7.5, self.origin.game.vh * 5), check.image, zindex = 5, offset = (self.origin.game.vh * 2.5, self.origin.game.vh * 3))

        self.collision = nodes.CollisionArea(self.origin, 7)
        self.collision.addCollisionBlock(self.sprite.size - pygame.Vector2(0, self.sprite.size.y / 16 * 2), offset_str = "center")
        self.collision.addCollisionBlock(self.sprite.size - pygame.Vector2(self.sprite.size.y / 16 * 2, 0), offset_str = "center")

        self.lock_node = nodes.SpriteBlock(self.origin, [self.origin.game.vh * 8, self.origin.game.vh * 8], pygame.transform.hsl(lock.image, lightness = 0.3), zindex = 1, offset_str = "center")
        self.lock_node.change(active = False)

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

    def update(self):
        level_data = resources.ReadData(self.origin.game.directory("test-levels.txt"), str(self.name))

        if level_data["locked_by"] != []:
            self.sprite.change(tile_node = self.icons[1])
            self.click_modifier.change(func = self.clickLocked)

            self.lock_node.change(active = True)
        else:
            self.sprite.change(tile_node = self.icons[0])
            self.click_modifier.change(func = lambda: self.enterLevel(self.name))

            self.lock_node.change(active = False)

        self.check.change(active = level_data["finished"])
    


