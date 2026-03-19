import math
import random
from ZaKnode import *
from pygame import Vector2

class button:
    def __init__(self, parent, text, font, txt_color, bg_color, padding, offset_str, offset, physics_layer, func):
        self.button = nodes.TextBlock(parent, text, font, txt_color = txt_color, bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset)
        play_collision = nodes.CollisionArea(self.button, physics_layer)
        play_collision.addCollisionBlock(self.button.size)
        modifiers.ClickOn(self.button, physics_layer, func)
        modifiers.Hover(self.button, physics_layer, lambda: self.button.change(padding = padding + 4, offset_str = offset_str, offset = offset), lambda: self.button.change(padding = padding, offset_str = offset_str, offset = offset))
    

class player:
    def __init__(self, parentNode, score, endScreen):
        sprite_size = 100
        hitbox_size = sprite_size
        scope_size = 20
        self.origin = nodes.BaseNode(parentNode, zindex = 3, offset_str = "center")
        self.sprite = nodes.ColorBlock(self.origin, (sprite_size, sprite_size), zindex = 0, offset_str = "center")
        self.collision = nodes.CollisionArea(self.origin, 1)
        self.collision.addCollisionBlock((hitbox_size, hitbox_size), offset = self.sprite.offset)
        self.arrow = nodes.ColorBlock(self.origin, (scope_size, scope_size), (200, 180, 170),zindex = 2, offset_str = "center", offset = (0, -100))
        self.arrow_move = modifiers.CircularMove(self.arrow, (0, 100), 100)

        self.score = score

        self.endScreen = endScreen

        modifiers.OnCollideBothObjects(self.origin, self.die, 2)

        self.alive = True

    def shoot(self, game_objects):
        if self.alive:
            angle = Vector2(0, 0).angle_to(self.arrow.offset)
            bullet(self, angle, game_objects, self.score)
    
    def die(self, enemy):
        if self.alive:
            self.alive = False
            self.endScreen.show()
        enemy.kill()
    

class bullet:
    def __init__(self, parentNode, angle, game_objects, score):
        angle = angle / 180 * math.pi

        self.game_objects = game_objects

        self.game_objects.append(self)

        self.score = score

        self.player = parentNode

        self.size = 5
        self.bullet = nodes.BaseNode(parentNode.origin, offset = [math.cos(angle) * 100, math.sin(angle) * 100])
        self.sprite = nodes.ColorBlock(self.bullet, (self.size, self.size), offset_str = "center")
        self.collision = nodes.CollisionArea(self.bullet, 3)
        self.collision.addCollisionBlock(self.sprite.size, offset = self.sprite.offset)
        
        end = [math.cos(angle) * (self.bullet.game.screen_size[0]), math.sin(angle) * (self.bullet.game.screen_size[1])]
        modifiers.LinearMove(self.bullet, end, looping = False)

        modifiers.ForeverDo(self.bullet, self.outOfRange)

        modifiers.OnCollideBothObjects(self.bullet, self.hitEnemy, 2)
    
    def outOfRange(self):
        if -self.size > self.bullet.position.x > self.bullet.game.screen_size.x or -self.size > self.bullet.position.y > self.bullet.game.screen_size.y:
            self.kill()
        
    def hitEnemy(self, enemy):
        if self.player.alive:
            self.score.score += 1
        enemy.kill()
        self.kill()

    def kill(self):
        self.game_objects.remove(self)
        self.bullet.kill()


class enemy:
    def __init__(self, parentNode, player, game_objects):

        self.game_objects = game_objects

        self.game_objects.append(self)

        size = 120
        angle = random.randrange(0, 360) / 180 * math.pi
        offset = [(math.cos(angle) + 1) * (parentNode.game.screen_size[0] + 2 * size) / 2 - size,
                (math.sin(angle) + 1) * (parentNode.game.screen_size[1] + 2 * size) / 2 - size]
        self.origin = nodes.BaseNode(parentNode, offset = offset)
        self.sprite = nodes.ColorBlock(self.origin, (size, size), (250, 30, 80), offset_str = "center")
        collisionA = nodes.CollisionArea(self.origin, 2)
        nodes.CollisionBlock(collisionA, self.sprite.size, offset = self.sprite.offset)
        modifiers.Follow(self.origin, player.origin, speed = 160)
    
    def kill(self):
        self.game_objects.remove(self)
        self.origin.kill()


class score:
    def __init__(self, parentNode):
        self.func = lambda: print()
        self.player = None
        self.score = 0
        self.time = 0
        self.text = nodes.Label(parentNode, f"Score :{self.score}", parentNode.game.fonts["main"], offset = (40, 40))
        modifiers.ForeverDo(self.text, self.update )
    
    def update(self):
        self.time += 1
        self.text.change(text = f"Score: {self.score}")
        if self.score == 0:
            self.time = 0
            return
        
        if self.time >= max(10, 60 / self.score * 15):
            self.time = 0
            self.player.arrow_move.change(speed = self.player.arrow_move.speed + 5)
            self.func()


class endScreen:
    def __init__(self, parentNode, score):
        self.parentNode = parentNode
        self.scoreNode = score
        self.background = None

    def show(self):
        self.hide()
        scores = self.maxScore(self.scoreNode.score)
        self.background = nodes.ColorBlock(self.parentNode, self.parentNode.game.screen_size, (0, 0, 0, 120), zindex = 10, alpha_channel = True)
        self.text = nodes.Label(self.background, "Game Over", self.parentNode.game.fonts["main"], (255, 10, 10), offset_str = "center", offset = (0, -60))
        if len(scores) == 1:
            self.score = nodes.Label(self.background, scores[0], self.parentNode.game.fonts["secondary"], (255, 255, 255), offset_str = "center")
        else:
            self.score = nodes.Label(self.background, scores[0], self.parentNode.game.fonts["secondary"], (255, 255, 255), offset_str = "center", offset = (-140, 0))
            self.score = nodes.Label(self.background, scores[1], self.parentNode.game.fonts["secondary"], (255, 255, 255), offset_str = "center", offset = (80, 0))
        self.buttons = []
        self.buttons.append(button(self.background, "Restart", self.parentNode.game.fonts["secondary"], (244, 244, 244), (23, 230, 45), 16, offset_str = "center", offset = (-140, 80), physics_layer = 30, func = lambda: self.parentNode.game.changeScene("game")))
        self.buttons.append(button(self.background, "Menu", self.parentNode.game.fonts["secondary"], (244, 244, 244), (23, 230, 45), 16, offset_str = "center", offset = (0, 80), physics_layer = 31, func = self.restart))
        self.buttons.append(button(self.background, "Exit", self.parentNode.game.fonts["secondary"], (244, 244, 244), (23, 230, 45), 16, offset_str = "center", offset = (140, 80), physics_layer = 32, func = lambda: self.parentNode.game.end()))
    
    def hide(self):
        if callable(getattr(self.background, "kill", None)):
            self.background.kill()

    def restart(self):
        self.background.game.changeScene("menu")
        self.hide()

    def maxScore(self, score):
        scoreBigger = False

        path = resources.directory(__file__, "max_score.txt")
        with open(path, "r") as r:
            try:
                maxScore = int(r.read())
            except:
                maxScore = 0
            if maxScore < score:
                scoreBigger = True
        
        if scoreBigger:
            with open(path, "w") as w:
                w.write(str(score))
            return [f"New high score {score}"]

        return [f"Score: {score}", f"High score: {maxScore}"]
