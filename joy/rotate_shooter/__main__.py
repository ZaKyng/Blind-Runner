import pygame
from ZaKnode import *
from .lib import *

# ----- Pygame setup ----- #
def run():
    screen_size = (1080, 1080)
    my_game = nodes.Game(screen_size, fps = 120)

    menu = nodes.Scene("menu", my_game, (3, 20, 7))
    game = nodes.Scene("game", my_game, (100, 180, 115))
    stats = nodes.Scene("stats", my_game, (90, 30, 42))

    button(menu, "Play", my_game.fonts["main"], (8, 8, 8), (200, 200, 200), 20, "center", (0, -140), 20, lambda: my_game.changeScene("game"))

    button(menu, "Stats", my_game.fonts["main"], (8, 8, 8), (200, 200, 200), 20, "center", (0, 0), 21, lambda: my_game.changeScene("stats"))

    button(menu, "Exit", my_game.fonts["main"], (8, 8, 8), (200, 200, 200), 20, "center", (0, 140), 22, lambda: my_game.end())


    for scene in [game, stats]:
        button(scene, "Back", my_game.fonts["secondary"], (0, 0, 0), (200, 200, 200), 10, "bottom-right", (0, 0), 23, lambda: my_game.changeScene("menu"))

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

    character = player(game, score_count, end_screen)

    def shoot(game_objects):
        if character.alive:
            character.arrow_move.change(clockwise = character.arrow_move.direction == -1)
            character.shoot(game_objects)
    
    modifiers.Press(character.origin, pygame.K_SPACE, lambda: shoot(game_objects))

    def spawnEnemy():
        enemy(game, character, game_objects)

    
    score_count.func = spawnEnemy
    score_count.player = character

    #modifiers.Press(game, pygame.K_d, lambda: spawnEnemy())

    game.change(onEntry = lambda: clearGame(character, game_objects, score_count))


    score_text = nodes.Label(stats, "High score", my_game.fonts["secondary"], color = (220, 220, 220), offset_str = "center", offset = (0, -80))

    score_score = nodes.Label(stats, "0", my_game.fonts["main"], offset_str = "center", offset = (0, 0))

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