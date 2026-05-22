import pygame
import os
from ZaKnode import *

from ..lib import *


class LevelEditor:
    def __init__(self, game : nodes.Game):
        self.scene = nodes.Scene("level_editor", game, bg_color = (150, 60, 105))

        modifiers.OnEventFunc(self.scene, self.nameChanger)

        self.level_node = EditorWindow(self.scene)

        self.name = None
        self.old_name = None
        self.changing_name = False

        self.top_bar = nodes.ColorBlock(self.scene, (self.scene.size[0], 140), color = (132, 66, 244), offset = (0, 0), zindex = 5)
        
        self.little_label = nodes.Label(self.scene, "Editor", "main", "s", offset_str = "top", offset = (0, 0), zindex = 10)
        self.label = nodes.Label(self.scene, "Editor", "main", "l", offset_str = "top", offset = (0, 50), zindex = 10)
        nodes.CollisionArea(self.label, 18).addCollisionBlock((self.label.size[0] + 20, self.label.size[1] + 20), offset_str = "center")

        modifiers.ClickObject(self.label, 18, function = self.changeName, button = 1)

        modifiers.PressKey(self.scene, pygame.K_ESCAPE, self.leave)

    def load(self, name):
        if isinstance(name, str):
            self.name = name
            path = self.scene.game.directory("player_levels/" + name)
            level_data = resources.ReadData(path)

        else:
            self.name = "new_level"
            while os.path.exists(self.scene.game.directory("player_levels/" + self.name + ".txt")):
                    self.name += "_"
            self.name += ".txt"

            default_data = {
                "tile_count_x" : 20,
                "tile_set" : 0,
                "player_spawn" : [1, 1],
                "finish" : [2, 1],
                "possible" : False,
                "finished" : False,
                "spikes" : [],
                "ground" : []
            }

            for index in list(default_data.keys()):
                resources.SaveData(self.scene.game.directory("player_levels/" + self.name), index, default_data[index])
            
            level_data = default_data
            
        self.level_node.load(level_data, self.name)

        self.label.change(text = self.name.removesuffix(".txt"), offset_str = "top", offset = (0, 50))
        self.label.collision[0].change(size = self.label.size, offset_str = "center")
        self.label.collision[0].children[0].change(size = (self.label.size[0] + 20, self.label.size[1] + 20), offset_str = "center")
    
    def save(self):
        if self.name is None:
            return
        
        level_data = self.level_node.save()
        for index in list(level_data.keys()):
            resources.SaveData(self.scene.game.directory("player_levels/" + self.name), index, level_data[index])

    def leave(self):
        self.save()
        self.scene.game.scenes.changeScene("editor_menu")

    def changeName(self):
        pygame.key.start_text_input()
        self.changing_name = True
        self.old_name = self.name
        self.name = ""
        self.label.change(color = (90, 190, 90))
    
    def nameChanger(self, event):
        if not self.changing_name:
            return
        
        update = False
        
        if event.type == pygame.TEXTINPUT:
            self.name += event.text
            self.name = self.name.strip()
            update = True
        elif event.type == pygame.KEYDOWN:
            update = True
            if event.key == pygame.K_RETURN:
                pygame.key.stop_text_input()
                self.changing_name = False

                if self.name == "":
                    self.name = "_"
                
                self.name = self.name.replace(" ", "_")
                self.name = self.name.replace("/", "")
                self.name = self.name.replace("\\", "")
                
                while os.path.exists(self.scene.game.directory("player_levels/" + self.name + ".txt")):
                    self.name += "_"
                self.name += ".txt"

                old_file = "player_levels/" + self.old_name
                
                if os.path.exists(self.scene.game.directory(old_file)):
                    os.rename(self.scene.game.directory(old_file), self.scene.game.directory("player_levels/" + self.name.lower()))

                self.label.change(text = self.name.removesuffix(".txt"), color = (255, 255, 255), offset_str = "top", offset = (0, 50))
                self.nameCollisionUpdate()

                self.level_node.name = self.name
                return
            
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
        
        if update:
            self.label.change(text = self.name, offset_str = "top", offset = (0, 50))
            self.nameCollisionUpdate()
            

    def nameCollisionUpdate(self):
        self.label.collision[0].change(size = self.label.size, offset_str = "center")
        self.label.collision[0].children[0].change(size = (self.label.size[0] + 20, self.label.size[1] + 20), offset_str = "center")

class EditorWindow:
    def __init__(self, parentNode):
        self.parentNode = parentNode

        self.level_data = {
            "tile_count_x" : 20,
            "tile_set" : 0,
            "player_spawn" : [1, 1],
            "finish" : [2, 1],
            "possible" : False,
            "finished" : False,
            "spikes" : [],
            "ground" : []
        }

        self.loading = False

        self.window = nodes.ColorBlock(parentNode, (parentNode.size[0], parentNode.size[1] - 140), color = (0, 0, 0, 200), alpha_channel = True, offset = (0, 140))

        self.tile_node = []
        self.tile_node.append(resources.SpriteSheet(self.parentNode.game.directory("assets/test_tiles1.png"), (4, 4)))
        self.tile_node.append(resources.SpriteSheet(self.parentNode.game.directory("assets/test_tiles2.png"), (4, 4)))
        self.tile_node.append(resources.SpriteSheet(self.parentNode.game.directory("assets/test_tiles3.png"), (4, 4)))


        self.grid_encloser = nodes.BaseNode(self.window, zindex = 4)
        self.grid_maxs = (self.window.size[0] - 400, self.window.size[1])

        self.level_grid = nodes.TileMap(self.grid_encloser, self.tile_node[0], (10, 10), zindex = 4)
        self.ground = self.level_grid.addLayer()

        self.blocks = ["ground", "player_spawn", "finish", "spike", "enemy_1"]
        self.noneditible = []
        self.selected_block = 0

        self.place_holding = False
        self.placing = True

        self.click_area = nodes.CollisionArea(self.window, physics_layer = 16)
        self.click_area.addCollisionBlock(self.window.size)

        modifiers.ClickObject(self.window, 16, function = lambda: self.togglePlacing(True), button = 1)
        modifiers.ClickObject(self.window, 16, function = lambda: self.togglePlacing(False), buttondown = False, button = 1)

        modifiers.ForeverDo(self.window, self.mousePlace)



        arrows = resources.SpriteSheet(self.parentNode.game.directory("assets/arrows.png"), (16, 16), True)

        self.side_panel = nodes.ColorBlock(self.window, (400, self.window.size[1]), color = (80, 80, 80), offset_str = "right", zindex = 10)

        self.tile_resize = {"box" : nodes.BaseNode(self.side_panel, zindex = 1)}

        self.tile_resize["label"] = nodes.Label(self.tile_resize["box"], "Tile Size", "main", "xs", offset = (140, 10), zindex = 2)
        self.tile_resize["bigger"] = Button(self.tile_resize["box"], (75, 75), arrows.grid[0][0], lambda: self.changeTileCount(self.level_data["tile_count_x"] + 1), higherBy = 2, offset = (64, 64))
        self.tile_resize["text"] = nodes.Label(self.tile_resize["box"], str(self.level_data["tile_count_x"]), "main", "l", offset = (140, 45), zindex = 2)
        self.tile_resize["smaller"] = Button(self.tile_resize["box"], (75, 75), arrows.grid[0][1], lambda: self.changeTileCount(self.level_data["tile_count_x"] - 1), higherBy = 2, offset = (340, 64))


        separator = []
        separator.append(nodes.ColorBlock(self.side_panel, (380, 4), color = (40, 40, 40), offset_str = "top", offset = (0, 130), zindex = 10))
        separator.append(nodes.ColorBlock(self.side_panel, (380, 4), color = (40, 40, 40), offset_str = "top", offset = (0, 200), zindex = 10))

        self.design_changer = {"box" : nodes.BaseNode(self.side_panel, zindex = 1, offset = (30, 170))}
        self.level_icons = resources.SpriteSheet(self.parentNode.game.directory("assets/level-icons.png"), (32, 32), True)
        self.design_changer["icon"] = nodes.SpriteBlock(self.design_changer["box"], (55, 55), self.level_icons.grid[0][0], offset_str = "left", zindex = 2)
        self.design_changer["label"] = nodes.Label(self.design_changer["box"], "Tile Set", "main", "s", offset = (75, 0), offset_str = "left", zindex = 2)
        self.design_changer["button"] = Button(self.design_changer["box"], (50, 50), arrows.grid[0][1], self.changeTileSet, higherBy = 2, offset_str = "right", offset = (290, 0))


        self.block_select = {"box" : nodes.BaseNode(self.side_panel, zindex = 1, offset = (0, 210))}
        
        self.block_select["label"] = nodes.Label(self.block_select["box"], "Blocks:", "main", "xs", offset = (140, 10), zindex = 2)

        self.block_select["cards"] = []
        card_icons = [self.tile_node[0].grid[1][0], self.tile_node[0].grid[0][3], self.tile_node[0].grid[3][3], self.tile_node[0].grid[3][4], self.tile_node[0].grid[0][3]]

        for i in range(len(self.blocks)):
            self.block_select["cards"].append(BlockCard(self.block_select["box"], i, card_icons[i], offset = ((i % 2 * 140) + 80, (i // 2 * 180) + 80), changerFunc = self.changeSelectedBlock))

        self.bottom_buttons = {"box" : nodes.BaseNode(self.side_panel, zindex = 1, offset_str = "bottom-left", offset = (0, -60))}
        self.bottom_buttons["save"] = ButtonText(self.bottom_buttons["box"], "Save", "main", self.save, offset_str = "left", offset = (40, 0))
        self.bottom_buttons["delete"] = ButtonText(self.bottom_buttons["box"], "Delete", "main", self.showDeleteWindow, offset_str = "left", offset = (205, 0))

        self.delete_window = nodes.ColorBlock(self.parentNode, (self.parentNode.size), color = (0, 0, 0, 200), alpha_channel = True, zindex = 999)
        nodes.Label(self.delete_window, "Are you sure you want to delete this level?", "main", "l", offset_str = "center", offset = (0, -50))
        ButtonText(self.delete_window, "Yes", "main", self.delete, white_txt = False, offset_str = "center", offset = (-100, 50))
        ButtonText(self.delete_window, "No", "main", lambda: self.showDeleteWindow(False), offset_str = "center", offset = (100, 50))

        self.delete_window.change(active = False)



    def load(self, level_data, name):
        # Bulk-load level data with reduced per-tile updates to avoid long stalls.
        self.loading = True

        self.level_data = level_data
        self.name = name

        # Apply tile size first (may recreate internal structures)
        self.changeTileCount(self.level_data.get("tile_count_x", 20))
        self.changeTileSet(level_data.get("tile_set", 0)) # Apply tile set (may also recreate structures)
        self.level_grid.change(tile_node = self.tile_node[self.level_data["tile_set"]])

        # Clear existing tiles quickly
        for i in list(self.ground.blocks.keys()):
            self.ground.blocks[i].kill()
            self.ground.blocks.pop(i)

        # Temporarily disable per-tile neighbor updates for bulk placement
        orig_updateBlock = self.updateBlock
        orig_updateSurrounding = self.updateSurrounding
        self.updateBlock = lambda coords: None
        self.updateSurrounding = lambda coords: None

        # Bulk add ground tiles (fast, without neighbor recalculation)
        for block in list(self.level_data["ground"]):
            coords = tuple(block)
            if coords not in self.ground.blocks.keys():
                self.ground.addTile(coords, [3, 0])

        # Player spawn: ensure the tile is present and marked
        pcoords = tuple(self.level_data["player_spawn"])
        try:
            self.ground.killTile(tuple(self.level_data["player_spawn"]))
        except Exception:
            pass
        if pcoords in self.ground.blocks.keys():
            self.ground.changeTile(pcoords, [0, 3])
        else:
            self.ground.addTile(pcoords, [0, 3])

        # Finish
        fcoords = tuple(self.level_data["finish"])
        try:
            self.ground.killTile(tuple(self.level_data["finish"]))
        except Exception:
            pass
        if fcoords in self.ground.blocks.keys():
            self.ground.changeTile(fcoords, [3, 3])
        else:
            self.ground.addTile(fcoords, [3, 3])

        # Spikes
        for spike in list(self.level_data["spikes"]):
            scoords = tuple(spike)
            if scoords in self.level_data["player_spawn"] or scoords in self.level_data["finish"]:
                continue
            if scoords in self.ground.blocks.keys():
                self.ground.changeTile(scoords, [3, 4])
            else:
                self.ground.addTile(scoords, [3, 4])

        # Restore update functions and run a single neighbor update per tile
        self.updateBlock = orig_updateBlock
        self.updateSurrounding = orig_updateSurrounding

        for block in list(self.ground.blocks.keys()):
            try:
                self.updateBlock(block)
            except Exception:
                # Be conservative: ignore per-block failures during bulk update
                pass

        self.loading = False
        self.updateNoneditible()


    def save(self):
        level_data = self.level_data

        """
        level_data["tile_size"] = list(self.level_grid.tile_size)
        level_data["ground"] = list(self.ground.blocks.keys())
        level_data["player_spawn"] = list(self.level_data["player_spawn"])
        level_data["finish"] = list(self.level_data["finish"])
        level_data["spikes"] = list(self.level_data["spikes"])
        """

        self.noneditible = []

        return level_data
    

    def showDeleteWindow(self, show = True):
        self.delete_window.change(active = show)


    def delete(self):
        if self.name is None:
            return
        
        path = self.window.game.directory("player_levels/" + self.name)
        if os.path.exists(path):
            os.remove(path)
        
        self.showDeleteWindow(False)
        
        self.window.game.scenes.changeScene("editor_menu")



    def togglePlacing(self, placing):
        self.place_holding = placing
        
        position_in_screen = pygame.mouse.get_pos() - self.grid_encloser.game.scenes.scenes[self.grid_encloser.game.scenes.current_scene].position
        mouse_pos = pygame.Vector2(int(position_in_screen.x / self.grid_encloser.game.scale.x), int(position_in_screen.y / self.grid_encloser.game.scale.y)) - (self.grid_encloser.position - self.grid_encloser.game.scenes.scenes[self.grid_encloser.game.scenes.current_scene].position)

        coords = [int(mouse_pos.x // self.level_grid.tile_size[0]), int(mouse_pos.y // self.level_grid.tile_size[1])]

        if tuple(coords) in self.ground.blocks.keys():
            self.placing = False
        else:
            self.placing = True

    def mousePlace(self):
        if not self.place_holding:
            return
        
        position_in_screen = pygame.mouse.get_pos() - self.grid_encloser.game.scenes.scenes[self.grid_encloser.game.scenes.current_scene].position
        mouse_pos = pygame.Vector2(int(position_in_screen.x / self.grid_encloser.game.scale.x), int(position_in_screen.y / self.grid_encloser.game.scale.y)) - (self.grid_encloser.position - self.grid_encloser.game.scenes.scenes[self.grid_encloser.game.scenes.current_scene].position)

        if mouse_pos.x < 0 or mouse_pos.y < 0 or mouse_pos.x > self.grid_maxs[0] or mouse_pos.y > self.grid_maxs[1]:
            return

        coords = [int(mouse_pos.x // self.level_grid.tile_size[0]), int(mouse_pos.y // self.level_grid.tile_size[1])]
        
        self.place(coords)



    def place(self, coords):
        coords = tuple(coords)

        if self.selected_block == 0: #ground
            if coords in self.noneditible:
                return
            
            print(self.placing)
            
            if self.placing:
                if list(coords) in self.level_data["ground"]:
                    return
                self.ground.addTile(coords, [3, 0])
                self.level_data["ground"].append(list(coords))
            else:
                if not list(coords) in self.level_data["ground"]:
                    return
                self.ground.killTile(coords)
                self.level_data["ground"].remove(list(coords))

            self.updateBlock(coords)
            self.updateSurrounding(coords)
        
        elif self.selected_block == 1: #player_spawn

            if coords in self.noneditible:
                return

            self.ground.killTile(tuple(self.level_data["player_spawn"]))

            if list(coords) in self.level_data["ground"]:
                self.ground.changeTile(coords, [0, 3])
                self.level_data["ground"].remove(list(coords))
                self.updateSurrounding(coords)
            else:
                self.ground.addTile(coords, [0, 3])

            self.level_data["player_spawn"] = list(coords)

            
        
        elif self.selected_block == 2: #finish

            if coords in self.noneditible:
                return

            self.ground.killTile(tuple(self.level_data["finish"]))

            if list(coords) in self.level_data["ground"]:
                self.ground.changeTile(coords, [3, 3])
                self.level_data["ground"].remove(list(coords))
                self.updateSurrounding(coords)
            else:
                self.ground.addTile(coords, [3, 3])

            self.level_data["finish"] = list(coords)

            

        
        elif self.selected_block == 3: #spikes
            if list(coords) == self.level_data["player_spawn"] or list(coords) == self.level_data["finish"]: # to be able to edit spikes
                return
            
            if self.placing:
                if list(coords) in self.level_data["spikes"]:
                    return
                
                if list(coords) in self.level_data["ground"]:
                    self.ground.changeTile(coords, [3, 4])
                    self.level_data["ground"].remove(list(coords))
                    self.updateSurrounding(coords)
                else:
                    self.ground.addTile(coords, [3, 4])
                self.level_data["spikes"].append(list(coords))

            else:
                if not list(coords) in self.level_data["spikes"]:
                    return
                self.level_data["spikes"].remove(list(coords))
                self.ground.killTile(coords)
            

        
        if not self.loading:
            self.updateNoneditible()
    
    def updateSurrounding(self, coords):
        self.updateBlock([coords[0] + 1, coords[1]])
        self.updateBlock([coords[0], coords[1] + 1])
        self.updateBlock([coords[0] - 1, coords[1]])
        self.updateBlock([coords[0], coords[1] - 1])

    def updateBlock(self, coords):
        coords = tuple(coords)

        if not list(coords) in self.level_data["ground"] or not coords in self.ground.blocks.keys():
            return

        coord_check = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        checks = []

        states = {
            (False, False, False, False) : [4, 0],
            (False, False, False, True) : [3, 1],
            (False, False, True, False) : [4, 2],
            (False, False, True, True) : [2, 0],
            (False, True, False, False) : [3, 2],
            (False, True, False, True) : [3, 0],
            (False, True, True, False) : [0, 0],
            (False, True, True, True) : [1, 0],
            (True, False, False, False) : [4, 1],
            (True, False, False, True) : [2, 2],
            (True, False, True, False) : [5, 0],
            (True, False, True, True) : [2, 1],
            (True, True, False, False) : [0, 2],
            (True, True, False, True) : [1, 2],
            (True, True, True, False) : [0, 1],
            (True, True, True, True) : [1, 1]
        }

        for checked in coord_check:
            temp = [coords[0] + checked[0], coords[1] + checked[1]]

            checks.append(temp in self.level_data["ground"])
        
        self.ground.changeTile(coords, states[tuple(checks)])
        

    def changeTileCount(self, count_x):
        last_count = self.level_data["tile_count_x"]
        tile_count = max(10, min(count_x, 90))
        size = ((self.window.size[0] - 400) // (tile_count), (self.window.size[0] - 400) // (tile_count))
        self.level_grid.change(one_tile_size = size)
        self.level_data["tile_count_x"] = tile_count
        self.tile_resize["text"].change(text = str(int(tile_count)))

        self.grid_maxs = [((self.window.size[0] - 400) // self.level_grid.tile_size[0] + 1) * self.level_grid.tile_size[0], (self.window.size[1] // self.level_grid.tile_size[1] + 1) * self.level_grid.tile_size[1]]
        self.grid_encloser.change(offset = ((self.grid_maxs[0] - (self.window.size[0] - 400)) // -2, (self.grid_maxs[1] - self.window.size[1]) // -2))

        if last_count < tile_count:
            for block in list(self.ground.blocks.keys()):
                if block[0] * size[0] >= self.grid_maxs[0] or block[1] * size[1] >= self.grid_maxs[1]:
                    temp_selected = self.selected_block
                    temp_placing = self.placing

                    self.selected_block = 0
                    self.placing = False
                    self.place(block)

                    self.selected_block = temp_selected
                    self.placing = temp_placing
    
    def changeSelectedBlock(self, index):
        self.selected_block = index
        for card in self.block_select["cards"]:
            card.highlight.change(active = False)
        
        self.block_select["cards"][index].highlight.change(active = True)
    

    def updateNoneditible(self):
        self.noneditible = []
        for spikes in self.level_data["spikes"]:
            self.noneditible.append(tuple(spikes))
        self.noneditible.append(tuple(self.level_data["player_spawn"]))
        self.noneditible.append(tuple(self.level_data["finish"]))
    

    def changeTileSet(self, index = None):
        if index is not None:
            self.level_data["tile_set"] = index % len(self.tile_node)
        else:
            self.level_data["tile_set"] = (self.level_data.get("tile_set", 0) + 1) % len(self.tile_node)
        self.level_grid.change(tile_node = self.tile_node[self.level_data["tile_set"]])

        self.design_changer["icon"].change(image = self.level_icons.grid[self.level_data["tile_set"]][0])

        self.updateCards()

    
    def updateCards(self):
        card_icons = [self.tile_node[self.level_data["tile_set"]].grid[1][0], self.tile_node[self.level_data["tile_set"]].grid[0][3], self.tile_node[self.level_data["tile_set"]].grid[3][3], self.tile_node[self.level_data["tile_set"]].grid[3][4], self.tile_node[self.level_data["tile_set"]].grid[0][3]]
        for i in range(len(self.blocks)):
            self.block_select["cards"][i].changeImage(card_icons[i])



class BlockCard:
    def __init__(self, parentNode, index, image, offset, changerFunc):
        self.parentNode = parentNode
        self.index = index
        self.changerFunc = changerFunc

        self.base = nodes.BaseNode(parentNode, zindex = 4, offset = offset)
        self.highlight = nodes.ColorBlock(self.base, (130, 170), color = (0, 255, 0), alpha_channel = True, zindex = 1, offset = (-5, -5))
        self.highlight.change(active = False)
        self.background = nodes.ColorBlock(self.base, (120, 160), color = (100, 100, 100), zindex = 2)
        self.image = nodes.SpriteBlock(self.background, (60, 60), image, zindex = 3, offset_str = "center")

        nodes.CollisionArea(self.background, physics_layer = 16).addCollisionBlock(self.background.size)

        modifiers.ClickObject(self.background, 16, function = lambda: self.select(self.index), button = 1)

    def select(self, index):
        self.highlight.change(active = False)
        self.changerFunc(index)
    
    def changeImage(self, image):
        self.image.change(image = image)
