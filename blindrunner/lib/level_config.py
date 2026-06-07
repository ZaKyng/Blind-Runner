from ZaKnode import *

def configourateLevels(my_game):
    level1 = IngameLevel(my_game, "i_cant_see", [], [20, 20])
    level2 = IngameLevel(my_game, "grounded", [level1], [17, 61])
    level3 = IngameLevel(my_game, "analyse", [level2], [19, 99])
    level4 = IngameLevel(my_game, "lava_island", [level1], [54, 37])
    level5 = IngameLevel(my_game, "dont_fall", [level2, level4], [63, 80])
    level6 = IngameLevel(my_game, "deadly", [level3, level5], [68, 121])
    level7 = IngameLevel(my_game, "a_long_jump", [level4], [106, 25])
    level8 = IngameLevel(my_game, "not_friends", [level5, level7], [119, 56])
    level9 = IngameLevel(my_game, "they_fly_now", [level7], [176, 25])
    level10 = IngameLevel(my_game, "team_up", [level8, level9], [170, 58])
    level11 = IngameLevel(my_game, "icy", [level8], [113, 86])
    level12 = IngameLevel(my_game, "duel", [level6, level11], [125, 113])
    level13 = IngameLevel(my_game, "the_faster_the_better", [level10, level12], [182, 92])
    level14 = IngameLevel(my_game, "be_a_bait", [level9], [230, 62])
    level15 = IngameLevel(my_game, "dont_get_lost", [level13, level14], [236, 119])



class IngameLevel:
    def __init__(self, game : nodes.Game, name, locked_by : list, offset : list):
        self.name = name

        self.level = resources.ReadData(game.directory(f"player_levels/{name}.txt"))

        if self.level is None:
            return

        self.level["locked_by"] = []
        self.level["unlocks"] = []

        self.level["offset"] = offset
        self.level["finished"] = False

        for level in locked_by:
            self.level["locked_by"].append(level.name)

            locking_level = resources.ReadData(game.directory(f"backup_levels/{level.name}.txt"))

            locking_level["unlocks"].append(self.name)

            resources.SaveData(game.directory(f"backup_levels/{level.name}.txt"), "unlocks", locking_level["unlocks"])

        
        for key in self.level.keys():
            resources.SaveData(game.directory(f"backup_levels/{name}.txt"), key, self.level[key])