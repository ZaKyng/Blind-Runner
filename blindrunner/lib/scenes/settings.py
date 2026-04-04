import pygame
from ZaKnode import *
from ..lib import Button
from ..lib import ButtonText



class Settings:
    def __init__(self, game):
        self.scene = nodes.Scene("settings", game, bg_color = (26, 26, 26))
        self.changers = []
        self.changers.append(IntChanger(self.scene, "FPS cap", game.tick_speed, self.changeFPS, step = 25, offset = (0, 120)))
        self.changers.append(Toggle(self.scene, "Show FPS", self.showFPS, offset = (0, 280)))
        self.changers.append(ButtonText(self.scene, "Factory reset", "main", lambda: self.hardReset(game), white_txt = False, offset_str = "top", offset = (0, 420)))

        self.fps_display = nodes.Label(self.scene, f"{1 / self.scene.game.delta} FPS", "main", "s", color = (10, 250, 10), zindex = 100, offset_str = "top-right")
        self.fps_display.change(active = False)
        modifiers.ForeverDo(self.fps_display, lambda: self.fps_display.change(text = f"{int(1 / max(self.scene.game.delta, 0.001))} FPS", offset_str = "top-right", offset = (-10, 10)))

        
        modifiers.PressKey(self.scene, pygame.K_ESCAPE, lambda: game.scenes.changeScene("menu"))
    
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
    
    def addFPSToScenes(self):
        for scene in list(self.scene.game.scenes.scenes.values()):
            scene.addChild(self.fps_display)

    def hardReset(self, game):
        backup = resources.ReadData(game.directory("levels_backup.txt"))

        resources.SaveDataList(game.directory("test-levels.txt"), list(backup.keys()), list(backup.values()))
            


class IntChanger:
    def __init__(self, parentNode, title, value, func, step = 10, offset = pygame.Vector2(0, 0)):
        self.func = func

        self.origin = nodes.BaseNode(parentNode, offset_str = "top", offset = offset)
        self.text = nodes.Label(self.origin, title, "main", "l", offset_str = "bottom", offset = [0, -20])
        self.value_txt = nodes.Label(self.origin, str(value), "main", "m", offset_str = "right")
        surface = pygame.Surface([90, 80])
        surface.fill((60, 230, 50))
        self.arrow_up = Button(self.origin, [90, 30], surface.copy(), lambda: self.addValue(step), offset = [65, -20])
        surface.fill((240, 30, 50))
        self.arrow_down = Button(self.origin, [90, 30], surface, lambda: self.addValue(-step), offset = [65, 20])

    def addValue(self, num):
        self.value_txt.change(text = self.func(num), offset_str = "right")
        

class Toggle:
    def __init__(self, parentNode, title, func, init = False, offset = pygame.Vector2(0, 0)):
        self.func = func

        self.origin = nodes.BaseNode(parentNode, offset_str = "top", offset = offset)

        self.text = nodes.Label(self.origin, title, "main", "l", offset_str = "right")
        self.surface = pygame.Surface((self.text.size.y * 0.7, self.text.size.y * 0.7))

        self.state = init
        self.surface.fill((25, 255, 25) if self.state else (255, 25, 25))
       
        self.toggle = Button(self.origin, (self.text.size.y * 0.7, self.text.size.y * 0.7), self.surface, self.changeState, offset_str = "left")
    
    def changeState(self):
        self.state = self.state == False
        self.surface.fill((25, 255, 25) if self.state else (255, 25, 25))
        self.func(self.state)



        