import math
import random
from ZaKnode import *
from pygame import Vector2

class button:
    def __init__(self, parent, text, font_name, font_size, txt_color, bg_color, padding, offset_str, offset, physics_layer, func, hover_color = None):
        self.button = nodes.TextBlock(parent, text, font_name, font_size = font_size, txt_color = txt_color, bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset)
        play_collision = nodes.CollisionArea(self.button, physics_layer)
        play_collision.addCollisionBlock(self.button.size)
        modifiers.ClickOn(self.button, physics_layer, func)
        hover_color = hover_color if hover_color is not None else bg_color
        modifiers.Hover(self.button, physics_layer, lambda: self.button.change(bg_color = hover_color, padding = padding + 4, offset_str = offset_str, offset = offset), lambda: self.button.change(bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset))
    

class player:
    def __init__(self, parentNode, score, endScreen, sprite, arrow, rocket_anim, rocket_end):
        sprite_size = 150
        hitbox_size = 100
        scope_size = 50
        self.scope_dist = 150
        self.origin = nodes.BaseNode(parentNode, zindex = 3, offset_str = "center")
        self.sprite = nodes.SpriteBlock(self.origin, (sprite_size, sprite_size), sprite, zindex = 0, offset_str = "center")
        self.collision = nodes.CollisionArea(self.origin, 1)
        self.collision.addCollisionBlock((hitbox_size, hitbox_size), offset_str = "center")
        self.arrow = nodes.BaseNode(self.origin, offset_str = "center", offset = (0, -self.scope_dist))
        self.arrow_sprite = nodes.SpriteBlock(self.arrow, (scope_size, scope_size), arrow, zindex = 2, offset_str = "center")
        self.arrow_move = modifiers.CircularMove(self.arrow, (0, self.scope_dist), self.scope_dist)

        self.score = score

        self.endScreen = endScreen

        self.rocket_anim = rocket_anim
        self.rocket_end = rocket_end

        modifiers.OnCollideBothObjects(self.origin, self.die, 2)

        self.alive = True

    def shoot(self, game_objects):
        if self.alive:
            angle = Vector2(0, 0).angle_to(self.arrow.offset)
            bullet(self, angle, game_objects, self.score, self.rocket_anim, self.rocket_end, self.scope_dist)
    
    def die(self, enemy):
        if self.alive:
            self.alive = False
            self.endScreen.show()
        enemy.kill()
    

class bullet:
    def __init__(self, parentNode, angle, game_objects, score, anim, end_anim, dist):
        rads = angle / 180 * math.pi

        self.game_objects = game_objects

        self.game_objects.append(self)

        self.score = score

        self.player = parentNode

        self.end_anim = end_anim

        sizer = 2
        self.size = 15 * sizer
        self.bullet = nodes.BaseNode(parentNode.origin, offset = [math.cos(rads) * dist, math.sin(rads) * dist])
        self.sprite = nodes.AnimatedSpriteBlock(self.bullet, (self.size, sizer * 32), anim.frames, 20, angle = -angle - 90, offset_str = "center")
        self.original_size = (self.size, sizer * 32)
        self.collision = nodes.CollisionArea(self.bullet, 3)
        self.collision.addCollisionBlock((self.size, self.size), offset_str = "center")
        self.end_timer = modifiers.Timer(self.bullet, 0.3, self.kill)
        
        end = [math.cos(rads) * (self.bullet.game.screen_size[0]), math.sin(rads) * (self.bullet.game.screen_size[1])]
        self.mover = modifiers.LinearMove(self.bullet, end, looping = False)

        modifiers.ForeverDo(self.bullet, self.outOfRange)

        modifiers.OnCollideBothObjects(self.bullet, self.hitEnemy, 2)
    
    def outOfRange(self):
        if -self.sprite.size.x - self.player.origin.offset.x > self.bullet.offset.x or self.bullet.offset.x > self.bullet.game.screen_size.x / 2 or -self.sprite.size.y - self.player.origin.offset.y > self.bullet.offset.y or self.bullet.offset.y > self.bullet.game.screen_size.y / 2:
            self.kill()
        
    def hitEnemy(self, enemy):
        if self.player.alive:
            self.score.score += 1
            self.score.fasterArrow()
        enemy.kill()
        self.mover.kill()
        self.sprite.change(frames_arr = self.end_anim.frames, angle = self.sprite.angle, size = self.original_size)
        self.end_timer.start()

    def kill(self):
        self.game_objects.remove(self)
        self.bullet.kill()


class enemy:
    def __init__(self, parentNode, player, game_objects, asteroid_grid):

        self.game_objects = game_objects

        self.game_objects.append(self)

        grid_x = random.randrange(0, 2)
        grid_y = random.randrange(0, 2)
        self.rotate_dir = -1 if random.randrange(0, 2) == 1 else 1
        init_angle = random.randrange(0, 360)

        size = 100
        sizer = 6
        angle = random.randrange(0, 360) / 180 * math.pi
        offset = [(math.cos(angle) + 1) * (parentNode.game.screen_size[0] + 2 * size) / 2 - size,
                (math.sin(angle) + 1) * (parentNode.game.screen_size[1] + 2 * size) / 2 - size]
        self.origin = nodes.BaseNode(parentNode, offset = offset)
        self.sprite = nodes.SpriteBlock(self.origin, (sizer * 18, sizer * 15), asteroid_grid[grid_x][grid_y], angle = init_angle, offset_str = "center")
        modifiers.ForeverDo(self.sprite, lambda: self.sprite.change(angle = self.sprite.angle + 0.2 * self.rotate_dir))
        collisionA = nodes.CollisionArea(self.origin, 2, show = False)
        nodes.CollisionBlock(collisionA, (size * 0.7, size * 0.7), offset_str = "center")
        modifiers.Follow(self.origin, player.origin, speed = 160)
    
    def kill(self):
        self.game_objects.remove(self)
        self.origin.kill()


class score:
    def __init__(self, parentNode):
        self.func = None
        self.player = None
        self.score = 0
        self.time = 0
        self.text = nodes.Label(parentNode, f"Score :{self.score}", "pixel", "l", offset = (40, 40))
        modifiers.ForeverDo(self.text, self.update )
    
    def update(self):
        self.time += 1
        self.text.change(text = f"Score: {self.score}")
        if self.score == 0:
            self.time = 0
            return
        
        if self.time >= self.get_spawn_delay():
            self.time = 0
            self.func()
    
    def get_spawn_delay(self):
        if self.score < 10:
            return 160
        elif self.score < 20:
            return 140
        elif self.score < 30:
            return 125
        elif self.score < 40:
            return 115
        elif self.score < 60:
            return 100
        elif self.score < 80:
            return 90
        elif self.score < 100:
            return 80
        elif self.score < 130:
            return 70
        else:
            return 55
    
    def fasterArrow(self):
        self.player.arrow_move.change(speed = min(self.player.arrow_move.speed + 7, 600))


class endScreen:
    def __init__(self, parentNode, score):
        self.parentNode = parentNode
        self.scoreNode = score
        self.background = None

    def show(self):
        self.hide()
        scores = self.maxScore(self.scoreNode.score)
        self.background = nodes.ColorBlock(self.parentNode, self.parentNode.game.screen_size, (0, 0, 0, 120), zindex = 10, alpha_channel = True)
        self.text = nodes.Label(self.background, "Game Over", "pixel", color = (255, 10, 10), offset_str = "center", offset = (0, -90))
        if len(scores) == 1:
            self.score = nodes.Label(self.background, scores[0], "pixel", "m", color = (255, 255, 255), offset_str = "center")
        else:
            self.score = nodes.Label(self.background, scores[0], "pixel", "s", color = (255, 255, 255), offset_str = "center", offset = (-180, 0))
            self.score = nodes.Label(self.background, scores[1], "pixel", "s", color = (255, 255, 255), offset_str = "center", offset = (180, 0))
        self.buttons = []
        self.buttons.append(button(self.background, "Restart", "pixel", "s", (244, 244, 244), (68, 68, 68), 16, offset_str = "center", offset = (-190, 120), physics_layer = 30, func = lambda: self.parentNode.game.changeScene("game")))
        self.buttons.append(button(self.background, "Menu", "pixel", "s", (244, 244, 244), (68, 68, 68), 16, offset_str = "center", offset = (50, 120), physics_layer = 31, func = self.restart))
        self.buttons.append(button(self.background, "Exit", "pixel", "s", (244, 244, 244), (68, 68, 68), 16, offset_str = "center", offset = (240, 120), physics_layer = 32, func = lambda: self.parentNode.game.end()))
    
    def hide(self):
        if callable(getattr(self.background, "kill", None)):
            self.background.kill()

    def restart(self):
        self.background.game.changeScene("menu")
        self.hide()

    def maxScore(self, score):
        scoreBigger = False

        path = self.parentNode.game.directory("max_score.txt")
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
