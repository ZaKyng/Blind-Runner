import pygame
from ZaKnode import *
from ..lib import Button
from ..lib import ButtonText



class Settings:
    def __init__(self, game, global_assets):
        self.last_scene = "main"

        self.name = "settings"

        self.global_assets = global_assets

        self.scene = nodes.Scene(self.name, game, bg_color = (26, 26, 26))
        self.changers = []
        self.changers.append(IntChanger(self.scene, "FPS cap", game.tick_speed, self.changeFPS, self.global_assets, step = 25, offset = (0, 120)))
        self.changers.append(Toggle(self.scene, "Show FPS", self.showFPS, self.global_assets, offset = (0, 280), ))
        self.changers.append(ButtonText(self.scene, "Factory reset", "main", lambda: self.hardReset(game), white_txt = False, offset_str = "top", offset = (0, 420)))

        self.fps_display = nodes.Label(self.scene, f"{1 / self.scene.game.delta} FPS", "main", "s", color = (10, 250, 10), zindex = 100, offset_str = "top-right")
        self.fps_display.change(active = False)
        modifiers.ForeverDo(self.fps_display, self.updateFPS)
        self.display_update = 0.0

        
        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene(self.last_scene))
    
    def changeFPS(self, num):
        max_value = 600
        if num < 0 and self.scene.game.tick_speed > max_value:
            self.scene.game.tick_speed = max_value
        else:
            self.scene.game.tick_speed = max(self.scene.game.tick_speed + num, 10)
            if self.scene.game.tick_speed > max_value:
                self.scene.game.tick_speed = max_value * 100
                return "Unlimited"

        return str(self.scene.game.tick_speed)

    def showFPS(self, state):
        self.fps_display.change(active = state)
    
    def updateFPS(self):
        self.display_update += self.scene.game.delta
        if self.display_update >= 0.4:
            self.fps_display.change(text = f"{int(1 / max(self.scene.game.delta, 0.0001))} FPS", offset_str = "top-right", offset = (-10, 10))
            self.display_update = 0

    
    def addFPSToScenes(self):
        for scene in list(self.scene.game.scenes.scenes.values()):
            scene.addChild(self.fps_display)

    def hardReset(self, game):
        backup = resources.ReadData(game.directory("levels_backup.txt"))

        resources.SaveDataList(game.directory("test-levels.txt"), list(backup.keys()), list(backup.values()))

        self.scene.game.scenes.changeScene("menu")
    
    def open(self, scene):
        self.last_scene = scene
        self.scene.game.scenes.changeScene(self.name)
            


class IntChanger:
    def __init__(self, parentNode, title, value, func, global_assets, step = 10, offset = pygame.Vector2(0, 0)):
        self.func = func

        self.global_assets = global_assets

        self.origin = nodes.BaseNode(parentNode, offset_str = "top", offset = offset)
        self.text = nodes.Label(self.origin, title, "main", "l", offset_str = "bottom", offset = [0, -20])
        self.value_txt = nodes.Label(self.origin, str(value), "main", "m", offset_str = "right", offset = (0, 10))
        self.arrow_up = Button(self.origin, [60, 30], self.global_assets["fps_buttons"].grid[0][0], lambda: self.addValue(step), offset = [65, -18])
        self.arrow_down = Button(self.origin, [60, 30], self.global_assets["fps_buttons"].grid[0][1], lambda: self.addValue(-step), offset = [65, 18])

    def addValue(self, num):
        self.value_txt.change(text = self.func(num), offset_str = "right", offset = (0, 10))
        

class Toggle:
    def __init__(self, parentNode, title, func, global_assets, init = False, offset = pygame.Vector2(0, 0)):
        self.func = func

        self.state = init

        self.global_assets = global_assets

        self.origin = nodes.BaseNode(parentNode, offset_str = "top", offset = offset)

        self.text = nodes.Label(self.origin, title, "main", "l", offset_str = "right")

        self.toggle = Button(self.origin, (100, 100), self.global_assets["arrows"].grid[0][9], self.changeState, offset_str = "left", offset = (80, -10))
    
    def changeState(self):
        self.state = self.state == False
        self.toggle.sprite.change(image = self.global_assets["arrows"].grid[0][8 if self.state else 9])
        self.func(self.state)



        