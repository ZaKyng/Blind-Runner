import pygame
import random
from ZaKnode import *
from .lib import *



# ----- Pygame setup ----- #
def run():
    screen_size = (1080, 1080)
    my_game = nodes.Game(screen_size, fps = 120)

    earth = resources.Image(resources.directory(__file__, "img/earth.png"), True)
    moon = resources.Image(resources.directory(__file__, "img/moon.png"), True)

    rocket_img = resources.SpriteSheet(resources.directory(__file__, "img/rocket.png"), pygame.Vector2(15, 24), True)
    rocket = resources.Animation(rocket_img.grid, 0, 6)
    rocket_end = resources.Animation(rocket_img.grid, 7, 7)

    asteroid = resources.SpriteSheet(resources.directory(__file__, "img/asteroid.png"), (18, 15), True)

    menu = nodes.Scene("menu", my_game, (5, 5, 5))
    game = nodes.Scene("game", my_game, (5, 5, 5))
    stats = nodes.Scene("stats", my_game, (5, 5, 5))

    button(menu, "Play", my_game.fonts["main"], (8, 8, 8), (200, 200, 200), 20, "center", (0, -140), 20, lambda: my_game.changeScene("game"))

    button(menu, "Stats", my_game.fonts["main"], (8, 8, 8), (200, 200, 200), 20, "center", (0, 0), 21, lambda: my_game.changeScene("stats"))

    button(menu, "Exit", my_game.fonts["main"], (8, 8, 8), (200, 200, 200), 20, "center", (0, 140), 22, lambda: my_game.end())

    menu_bg = []

    menu_bg.append(nodes.SpriteBlock(menu, (500, 500), earth.image, offset_str = "bottom-left", offset = (-150, 150)))
    menu_bg.append(nodes.BaseNode(menu_bg[0], offset_str = "center", offset = (0, -480)))
    nodes.SpriteBlock(menu_bg[1], (120, 120), moon.image, offset_str = "center")
    modifiers.CircularMove(menu_bg[1], (0, 500))


    for scene in [game, stats]:
        button(scene, "Back", my_game.fonts["secondary"], (0, 0, 0), (200, 200, 200), 10, "bottom-right", (0, 0), 23, lambda: my_game.changeScene("menu"))

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
        player.arrow_move.change(clockwise = True, start_deg = 0, speed = 200)
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
        enemy(game, character, game_objects, asteroid.grid[0][0])

    
    score_count.func = spawnEnemy
    score_count.player = character

    #modifiers.Press(game, pygame.K_d, lambda: spawnEnemy())

    game.change(onEntry = lambda: clearGame(character, game_objects, score_count))


    score_text = nodes.Label(stats, "High score", my_game.fonts["secondary"], color = (190, 190, 190), zindex = 5, offset_str = "center", offset = (0, -80))

    score_score = nodes.Label(stats, "0", my_game.fonts["main"], zindex = 5, offset_str = "center", offset = (0, 0))

    stat_bg = nodes.SpriteBlock(stats, (500, 500), earth.image, 0, offset_str = "center", offset = (0, -20))

    def showStats():
        path = resources.directory(__file__, "max_score.txt")
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