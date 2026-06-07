import pygame
import os
from ZaKnode import *
from ..lib import Button
from ..lib import ButtonText



class Settings:
    def __init__(self, game, global_assets):
        self.last_scene = "main"

        self.name = "settings"

        self.game = game

        self.global_assets = global_assets

        self.scene = nodes.Scene(self.name, game, bg_color = (26, 26, 26))
        self.scene.change(onEntry = lambda: self.reset_screen.change(active = False))
        self.changers = []

        fps_tile = nodes.BaseNode(self.scene, offset_str = "top", offset = (0, 0))

        fps_label = nodes.Label(fps_tile, "Visual settings", "main", "l", offset_str = "top", offset = (0, 60))

        self.changers.append(IntChanger(fps_tile, "FPS cap", game.tick_speed, self.changeFPS, self.global_assets, step = 25, offset = (-220, 260)))
        self.changers.append(Toggle(fps_tile, "Show FPS", self.showFPS, self.global_assets, offset = (240, 260)))

        spacer1 = nodes.ColorBlock(self.scene, (1600, 5), (120, 120, 120), offset_str = "top", offset = (0, 340))

        audio_tile = nodes.BaseNode(self.scene, offset_str = "top", offset = (0, 380))

        audio_label = nodes.Label(audio_tile, "Audio settings", "main", "l", offset_str = "top", offset = (0, 0))
        
        self.changers.append(Slider(audio_tile, "Master audio volume", self.changeMusicVolume, self.global_assets, init = 1, offset = (0, 110)))
        self.changers.append(Slider(audio_tile, "Music volume", lambda value: self.game.audio_player.changeVolume(value, "music"), self.global_assets, init = 1, offset = (0, 170)))
        self.changers.append(Slider(audio_tile, "SFX volume", lambda value: self.game.audio_player.changeVolume(value, "sfx"), self.global_assets, init = 1, offset = (0, 230)))
        sfx_test = Button(audio_tile, (110, 45), self.global_assets["test_button"].image, self.testSFXVolume, offset = (400, 220))

        self.fps_display = nodes.Label(self.scene, f"{1 / self.scene.game.delta} FPS", "main", "s", color = (10, 250, 10), zindex = 100, offset_str = "top-right")
        self.fps_display.change(active = False)
        modifiers.ForeverDo(self.fps_display, self.updateFPS)
        self.display_update = 0.0

        spacer2 = nodes.ColorBlock(self.scene, (1600, 5), (120, 120, 120), offset_str = "top", offset = (0, 680))

        Button(self.scene, (240, 120), global_assets["buttons"].grid[9][0], lambda: game.scenes.changeScene("support"), 4, offset_str = "bottom", offset = (-390, -250))
        Button(self.scene, (240, 120), global_assets["buttons"].grid[10][0], lambda: game.scenes.changeScene("credits"), 4, offset_str = "bottom", offset = (0, -250))
        Button(self.scene, (240, 120), global_assets["buttons"].grid[11][0], self.switchResetScreen, 4, offset_str = "bottom", offset = (390, -250))

        self.reset_screen = nodes.ColorBlock(self.scene, self.scene.size, color = (14, 14, 14, 210), zindex = 900, alpha_channel = True)

        nodes.Label(self.reset_screen, "Do you want to reset the progress?", "main", "l", (248, 248, 248), offset_str = "center", offset = (0, -90))
        Button(self.reset_screen, (110, 110), global_assets["arrows"].grid[0][17], lambda: self.hardReset(game), 0, "center", (-130, 40))
        Button(self.reset_screen, (110, 110), global_assets["arrows"].grid[0][5], self.switchResetScreen, 0, "center", (130, 40))
        
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

    def changeMusicVolume(self, value):
        self.scene.game.audio_player.changeMasterVolume(volume = value)

    def testSFXVolume(self):
        self.game.audio_player.playMusic("sfx", "win")

    def switchResetScreen(self):
        self.reset_screen.change(active = self.reset_screen.active == False)

    def hardReset(self, game):
        backup_folder = game.directory("backup_levels")
        for file_name in os.listdir(backup_folder):
            real_data = resources.ReadData(backup_folder + "/" + str(file_name))

            for key in real_data.keys():
                resources.SaveData(game.directory("ingame_levels/" + str(file_name)), key, real_data[key])

        self.switchResetScreen()

    
    def open(self, scene):
        self.last_scene = scene
        self.scene.game.scenes.changeScene(self.name)
            


class IntChanger:
    def __init__(self, parentNode, title, value, func, global_assets, step = 10, offset = pygame.Vector2(0, 0)):
        self.func = func

        self.global_assets = global_assets

        self.origin = nodes.BaseNode(parentNode, offset_str = "top", offset = offset)
        self.text = nodes.Label(self.origin, title, "main", "m", color = (210, 210, 210), offset_str = "bottom", offset = [0, -20])
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

        self.text = nodes.Label(self.origin, title, "main", "m", color = (210, 210, 210), offset_str = "right")

        self.toggle = Button(self.origin, (100, 100), self.global_assets["arrows"].grid[0][9], self.changeState, offset_str = "left", offset = (80, -10))
    
    def changeState(self):
        self.state = self.state == False
        self.toggle.sprite.change(image = self.global_assets["arrows"].grid[0][8 if self.state else 9])
        self.func(self.state)

class Slider:
    def __init__(self, parentNode, title, func, global_assets, init = 0.5, offset = pygame.Vector2(0, 0)):
        self.parentNode = parentNode

        self.func = func

        self.value = init

        self.global_assets = global_assets

        self.dragging = False

        self.origin = nodes.BaseNode(parentNode, offset_str = "top", offset = offset)

        self.text = nodes.Label(self.origin, title, "main", "m", color = (210, 210, 210), offset_str = "right", offset = (-120, -5))

        self.slider_bg = Button(self.origin, (384, 20), self.global_assets["slider"]["bg"].image, self.clickSlider, higherBy = 0, offset_str = "left", offset = (100, -10))
        self.slider_fg = Button(self.slider_bg.origin, (36, 36), self.global_assets["slider"]["fg"].image, self.activateDrag, offset_str = "center", offset = (((self.value * 2) - 1) * 192, 0))
        self.slider_fg.origin.change(zindex = 100)
        self.slider_fg.sprite.change(zindex = 100)

        modifiers.ForeverDo(self.origin, self.dragSlider)
        modifiers.PressKey(self.origin, 1, self.deactivateDrag, keydown = False, mouse = True)


    
    def clickSlider(self):
        mouse_x_in_screen = pygame.mouse.get_pos()[0] - self.parentNode.game.scenes.scenes[self.parentNode.game.scenes.current_scene].position[0]
        mouse_x = int(mouse_x_in_screen / self.parentNode.game.scale.x)
        slider_zero_x = self.slider_bg.origin.position.x - (self.slider_bg.sprite.size.x - 4) / 2 - self.parentNode.game.scenes.scenes[self.parentNode.game.scenes.current_scene].position[0]


        distance = mouse_x - slider_zero_x

        self.value = max(0, min(1, distance / 384))

        self.slider_fg.origin.change(offset_str = "center", offset = (((self.value * 2) - 1) * 192, 0))

        self.func(self.value)
    
    def activateDrag(self):
        self.dragging = True

    def deactivateDrag(self):
        self.dragging = False
    
    def dragSlider(self):
        if not self.dragging:
            return
    
        mouse_x_in_screen = pygame.mouse.get_pos()[0] - self.parentNode.game.scenes.scenes[self.parentNode.game.scenes.current_scene].position[0]
        mouse_x = int(mouse_x_in_screen / self.parentNode.game.scale.x)
        slider_zero_x = self.slider_bg.origin.position.x - (self.slider_bg.sprite.size.x - 4) / 2 - self.parentNode.game.scenes.scenes[self.parentNode.game.scenes.current_scene].position[0]

        distance = mouse_x - slider_zero_x

        self.value = max(0, min(1, distance / 384))

        self.slider_fg.origin.change(offset_str = "center", offset = (((self.value * 2) - 1) * 192, 0))

        self.func(self.value)
        