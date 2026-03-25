import pygame
from pygame import Vector2
import random
import math
from ZaKnode import *
from lib import *


# -- test -- #

"""
class button:
    def __init__(self, parent, text, font, txt_color, bg_color, padding, offset_str, offset, physics_layer, func, hover_color = None):
        self.button = nodes.TextBlock(parent, text, font, txt_color = txt_color, bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset)
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
        if -self.sprite.size.x > self.bullet.position.x or self.bullet.position.x > self.bullet.game.screen_size.x or -self.sprite.size.y > self.bullet.position.y or self.bullet.position.y > self.bullet.game.screen_size.y:
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

        size = 100
        sizer = 6
        angle = random.randrange(0, 360) / 180 * math.pi
        offset = [(math.cos(angle) + 1) * (parentNode.game.screen_size[0] + 2 * size) / 2 - size,
                (math.sin(angle) + 1) * (parentNode.game.screen_size[1] + 2 * size) / 2 - size]
        self.origin = nodes.BaseNode(parentNode, offset = offset)
        self.sprite = nodes.SpriteBlock(self.origin, (sizer * 18, sizer * 15), asteroid_grid[grid_x][grid_y], offset_str = "center")
        #modifiers.ForeverDo(self.sprite, lambda: self.sprite.change(angle = self.sprite.angle - 0.5))
        collisionA = nodes.CollisionArea(self.origin, 2)
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
        self.text = nodes.Label(parentNode, f"Score :{self.score}", parentNode.game.fonts["pixel"] "m",, offset = (40, 40))
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
        self.text = nodes.Label(self.background, "Game Over", self.parentNode.game.fonts["pixel"] "m",, (255, 10, 10), offset_str = "center", offset = (0, -90))
        if len(scores) == 1:
            self.score = nodes.Label(self.background, scores[0], self.parentNode.game.fonts["pixel"] "m",, (255, 255, 255), offset_str = "center")
        else:
            self.score = nodes.Label(self.background, scores[0], self.parentNode.game.fonts["pixel"] "m",, (255, 255, 255), offset_str = "center", offset = (-180, 0))
            self.score = nodes.Label(self.background, scores[1], self.parentNode.game.fonts["pixel"] "m",, (255, 255, 255), offset_str = "center", offset = (180, 0))
        self.buttons = []
        self.buttons.append(button(self.background, "Restart", self.parentNode.game.fonts["pixel"] "m",, (244, 244, 244), (68, 68, 68), 16, offset_str = "center", offset = (-190, 120), physics_layer = 30, func = lambda: self.parentNode.game.changeScene("game")))
        self.buttons.append(button(self.background, "Menu", self.parentNode.game.fonts["pixel"] "m",, (244, 244, 244), (68, 68, 68), 16, offset_str = "center", offset = (50, 120), physics_layer = 31, func = self.restart))
        self.buttons.append(button(self.background, "Exit", self.parentNode.game.fonts["pixel"] "m",, (244, 244, 244), (68, 68, 68), 16, offset_str = "center", offset = (240, 120), physics_layer = 32, func = lambda: self.parentNode.game.end()))
    
    def hide(self):
        if callable(getattr(self.background, "kill", None)):
            self.background.kill()

    def restart(self):
        self.background.game.changeScene("menu")
        self.hide()

    def maxScore(self, score):
        scoreBigger = False

        path = my_game.directory("max_score.txt")
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
"""

# -- end test -- #


# ----- Pygame setup ----- #
def run():
    screen_size = (1080, 1080)
    my_game = nodes.Game(screen_size, "Orbital Defender", fps = 120, screen_ratio = 1)
    my_game.addFont("pixel", my_game.directory("img/early_gameboy.ttf"))

    earth = resources.Image(my_game.directory("img/earth.png"), True)
    pygame.display.set_icon(earth.image)
    moon = resources.Image(my_game.directory("img/moon.png"), True)

    rocket_img = resources.SpriteSheet(my_game.directory("img/rocket.png"), pygame.Vector2(15, 24), True)
    rocket = resources.Animation(rocket_img.grid, 0, 6)
    rocket_end = resources.Animation(rocket_img.grid, 7, 7)

    asteroid = resources.SpriteSheet(my_game.directory("img/asteroid2.png"), (18, 15), True)

    menu = nodes.Scene("menu", my_game, (5, 5, 5))
    game = nodes.Scene("game", my_game, (5, 5, 5))
    stats = nodes.Scene("stats", my_game, (5, 5, 5))

    button(menu, "Play", "pixel", "m", (8, 8, 8), (156, 156, 156), 20, "center", (0, -160), 20, lambda: my_game.changeScene("game"), hover_color = (206, 206, 206))

    button(menu, "Stats", "pixel", "m", (8, 8, 8), (156, 156, 156), 20, "center", (0, 0), 21, lambda: my_game.changeScene("stats"), hover_color = (206, 206, 206))

    button(menu, "Exit", "pixel", "m", (8, 8, 8), (156, 156, 156), 20, "center", (0, 160), 22, lambda: my_game.end(), hover_color = (206, 206, 206))

    menu_bg = []

    menu_bg.append(nodes.SpriteBlock(menu, (500, 500), earth.image, offset_str = "bottom-left", offset = (-150, 150)))
    menu_bg.append(nodes.BaseNode(menu_bg[0], offset_str = "center", offset = (0, -480)))
    nodes.SpriteBlock(menu_bg[1], (120, 120), moon.image, offset_str = "center")
    modifiers.CircularMove(menu_bg[1], (0, 500))
    menu_bg.append(nodes.SpriteBlock(menu, (18 * 20, 15 * 20), asteroid.grid[1][0], offset_str = "top-right", offset = (-100, 100)))
    menu_bg.append(nodes.SpriteBlock(menu, (18 * 13, 15 * 13), asteroid.grid[0][1], offset_str = "top", offset = (-160, 30)))

    rocket_sizer = 4
    menu_rocket = nodes.AnimatedSpriteBlock(menu, (15 * rocket_sizer, 32 * rocket_sizer), rocket.frames, 20, angle = 45, offset = screen_size)
    menu_rocket_target = nodes.BaseNode(menu, offset = -menu_rocket.size)
    rocket_follow = modifiers.Follow(menu_rocket, menu_rocket_target)
    def reset_rocket(element):
        element.change(frames_arr = rocket.frames, angle = 45, size = (15 * rocket_sizer, 32 * rocket_sizer), offset = screen_size)
        rocket_follow.change(active = True)

    def menu_rocket_anim_func(element):
        if element.position == menu_rocket_target.position:
            reset_rocket(element)

    menu_rocket_collision = nodes.CollisionArea(menu_rocket, 67)
    menu_rocket_collision.addCollisionBlock((40, 40), offset_str = "center", offset = (-20, -20))
    menu_rocket_collision.addCollisionBlock((40, 40), offset_str = "center")
    menu_rocket_collision.addCollisionBlock((50, 50), offset_str = "center", offset = (20, 20))
    rocket_timer = modifiers.Timer(menu_rocket, 0.25, lambda: reset_rocket(menu_rocket))
    def on_rocket_click(element):
        rocket_follow.change(active = False)
        element.change(frames_arr = rocket_end.frames, angle = 45, size = (15 * rocket_sizer, 32 * rocket_sizer))
        rocket_timer.start()
    modifiers.ClickOn(menu_rocket, 67, lambda: on_rocket_click(menu_rocket))
    modifiers.ForeverDo(menu_rocket, lambda: menu_rocket_anim_func(menu_rocket))


    for scene in [game, stats]:
        button(scene, "Back", "pixel", "m", (0, 0, 0), (200, 200, 200), 10, "bottom-right", (0, 0), 23, lambda: my_game.changeScene("menu"))

    sectors = 5
    width = int(screen_size[0] / sectors)
    height = int(screen_size[1] / sectors)

    stars = []
    for x in range(sectors):
        for y in range(sectors):
            offset = pygame.Vector2(random.randrange(0, width) + width * x, random.randrange(0, height) + height * y)
            new_star = nodes.ColorBlock(menu, (2, 2), color = (246, 246, 246), zindex = -1, offset = offset)
            game.addChild(new_star)
            stats.addChild(new_star)

            stars.append(new_star)

    game_objects = []

    score_count = score(game)

    end_screen = endScreen(game, score_count)

    def clearGame(player, game_objects, score):
        for object in game_objects[:]:
            object.kill()

        player.alive = True
        player.arrow_move.change(clockwise = True, start_deg = 0, speed = 220)
        score.score = 0
        end_screen.hide()
        score_count.func()

    character = player(game, score_count, end_screen, earth.image, moon.image, rocket, rocket_end)

    def shoot(game_objects):
        if character.alive:  
            character.arrow_move.change(clockwise = character.arrow_move.direction == -1)
            character.shoot(game_objects)
    
    modifiers.Press(character.origin, pygame.K_SPACE, lambda: shoot(game_objects))

    def spawnEnemy():
        enemy(game, character, game_objects, asteroid.grid)
        pass

    
    score_count.func = spawnEnemy
    score_count.player = character

    #modifiers.Press(game, pygame.K_d, lambda: spawnEnemy())

    game.change(onEntry = lambda: clearGame(character, game_objects, score_count))


    score_text = nodes.Label(stats, "High score", "pixel", "m", color = (205, 205, 205), zindex = 5, offset_str = "center", offset = (0, -80))

    score_score = nodes.Label(stats, "0", "pixel", "m", zindex = 5, offset_str = "center", offset = (0, 0))

    stat_bg = nodes.SpriteBlock(stats, (500, 500), pygame.transform.hsl(earth.image, lightness = -0.25), 0, offset_str = "center", offset = (0, -20))

    def showStats():
        path = my_game.directory("max_score.txt")
        with open(path, "r") as r:
            try:
                maxScore = r.read()
            except:
                maxScore = "*error*"

        score_score.change(text = maxScore, offset_str = "center", offset = (0, 0))
    
    stats.change(onEntry = showStats)

    def global_input(event):
        pass

    def test():
        pass

    my_game.run(test, global_input = global_input)

if __name__ == "__main__":
    run()