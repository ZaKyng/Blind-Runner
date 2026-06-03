import pygame
import os
from ZaKnode import *

from ..lib import *


class LevelEditor:
    def __init__(self, game : nodes.Game, global_assets : dict):
        self.scene = nodes.Scene("level_editor", game, bg_color = (224, 130, 185))

        modifiers.OnEventFunc(self.scene, self.nameChanger)

        self.default_data = {
            "tile_count_x" : 20,
            "tile_set" : 0,
            "player_spawn" : [1, 1],
            "finish" : [2, 1],
            "possible" : False,
            "finished" : False,
            "spikes" : [],
            "ground" : [],
            "g_enemy" : [],
            "f_enemy" : []
        }

        self.level_node = EditorWindow(self.scene, self.default_data, global_assets)

        self.name = None
        self.old_name = None
        self.changing_name = False

        self.top_bar = nodes.ColorBlock(self.scene, (self.scene.size[0], 180), color = (132, 66, 244), offset = (0, 0), zindex = 5)
        
        self.little_label = nodes.Label(self.scene, "Editor", "main", "s", offset_str = "top", offset = (0, 30), zindex = 10)
        self.label = nodes.Label(self.scene, "Editor", "main", "l", offset_str = "top", offset = (0, 90), zindex = 10)
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


            for index in list(self.default_data.keys()):
                resources.SaveData(self.scene.game.directory("player_levels/" + self.name), index, self.default_data[index])

            level_data = resources.ReadData(self.scene.game.directory("player_levels/" + self.name))
            
            
            
        self.level_node.load(level_data, self.name)

        self.label.change(text = self.name.removesuffix(".txt").upper(), offset_str = "top", offset = (0, 90))
        self.label.collision[0].change(size = self.label.size, offset_str = "center")
        self.label.collision[0].children[0].change(size = (self.label.size[0] + 20, self.label.size[1] + 20), offset_str = "center")
    
    def save(self):
        if self.name is None:
            return
        
        level_data = self.level_node.save()
        for index in list(level_data.keys()):
            resources.SaveData(self.scene.game.directory("player_levels/" + self.name), index, level_data[index])

    def leave(self):
        
        if self.changing_name:
            self.rename(pygame.K_RETURN)
            
        self.save()

        

        self.scene.game.scenes.changeScene("editor_menu")

    def changeName(self):
        pygame.key.start_text_input()
        self.changing_name = True
        self.old_name = "new_level.txt"
        if self.name != "":
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
            if self.rename(event.key):
                return
            
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
        
        if update:
            self.label.change(text = self.name.upper(), offset_str = "top", offset = (0, 90))
            self.nameCollisionUpdate()
        
    def rename(self, event_key):
        if event_key == pygame.K_RETURN:
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

            self.label.change(text = self.name.removesuffix(".txt").upper(), color = (255, 255, 255), offset_str = "top", offset = (0, 90))
            self.nameCollisionUpdate()

            self.level_node.name = self.name
            return True
            

    def nameCollisionUpdate(self):
        self.label.collision[0].change(size = self.label.size, offset_str = "center")
        self.label.collision[0].children[0].change(size = (self.label.size[0] + 20, self.label.size[1] + 20), offset_str = "center")

class EditorWindow:
    def __init__(self, parentNode, default_data, global_assets):
        self.parentNode = parentNode
        self.level_data = default_data.copy()

        self.global_assets = global_assets

        self.loading = False

        self.window = nodes.ColorBlock(parentNode, (parentNode.size[0], parentNode.size[1] - 180), color = (0, 0, 0, 0), alpha_channel = True, offset = (0, 180))

        self.side_panel = nodes.ColorBlock(self.window, (320, self.window.size[1]), color = (80, 80, 80), offset_str = "right", zindex = 10)
        self.background = nodes.SpriteBlock(self.window, (self.window.size[0] - self.side_panel.size[0], self.window.size[1]), self.global_assets["backgrounds"][0].image, zindex = -10)

        self.grid_encloser = nodes.BaseNode(self.window, zindex = 4)
        self.grid_maxs = self.background.size.copy()

        self.level_grid = nodes.TileMap(self.grid_encloser, self.global_assets["tile_maps"][0], (10, 10), zindex = 4)
        self.ground = self.level_grid.addLayer()

        self.blocks = ["ground", "player_spawn", "finish", "spike", "g_enemy", "f_enemy"]
        self.noneditible = []
        self.selected_block = 0

        self.place_holding = False
        self.placing = True

        self.changed = False

        self.click_area = nodes.CollisionArea(self.window, physics_layer = 16)
        self.click_area.addCollisionBlock(self.window.size)

        modifiers.ClickObject(self.window, 16, function = lambda: self.togglePlacing(True), button = 1)
        modifiers.ClickObject(self.window, 16, function = lambda: self.togglePlacing(False), buttondown = False, button = 1)

        modifiers.ForeverDo(self.window, self.mousePlace)

        arrows = self.global_assets["arrows"]

        self.tile_resize = {"box" : nodes.BaseNode(self.side_panel, zindex = 1, offset_str = "top", offset = (0, 0))}

        self.tile_resize["label"] = nodes.Label(self.tile_resize["box"], "Tile Count", "main", "xs", offset_str = "top", offset = (0, 8), zindex = 2)
        self.tile_resize["bigger"] = Button(self.tile_resize["box"], (60, 60), arrows.grid[0][0], lambda: self.changeTileCount(self.level_data["tile_count_x"] + 1), higherBy = 2, offset_str = "top", offset = (110, 64))
        self.tile_resize["text"] = nodes.Label(self.tile_resize["box"], str(self.level_data["tile_count_x"]), "main", "l", offset_str = "top", offset = (0, 45), zindex = 2)
        self.tile_resize["smaller"] = Button(self.tile_resize["box"], (60, 60), arrows.grid[0][1], lambda: self.changeTileCount(self.level_data["tile_count_x"] - 1), higherBy = 2, offset_str = "top", offset = (-110, 64))


        separators = []
        separators.append(nodes.ColorBlock(self.side_panel, (self.side_panel.size[0] * 0.9, 4), color = (40, 40, 40), offset_str = "top", offset = (0, 130), zindex = 10))
        separators.append(nodes.ColorBlock(self.side_panel, (self.side_panel.size[0] * 0.9, 4), color = (40, 40, 40), offset_str = "top", offset = (0, 200), zindex = 10))

        self.design_changer = {"box" : nodes.BaseNode(self.side_panel, zindex = 1, offset_str = "top", offset = (0, 170))}
        self.level_icons = resources.SpriteSheet(self.parentNode.game.directory("assets/level-icons.png"), (32, 32), True)
        self.design_changer["icon"] = nodes.SpriteBlock(self.design_changer["box"], (55, 55), self.level_icons.grid[0][0], offset_str = "center", offset = (-110, 0), zindex = 2)
        self.design_changer["label"] = nodes.Label(self.design_changer["box"], "Tile Set", "main", "s", offset = (0, 10), offset_str = "center", zindex = 2)
        self.design_changer["button"] = Button(self.design_changer["box"], (50, 50), arrows.grid[0][2], self.changeTileSet, higherBy = 2, offset_str = "center", offset = (110, 0))


        self.block_select = {"box" : nodes.BaseNode(self.side_panel, zindex = 1, offset_str = "top", offset = (0, 225))}
        
        self.block_select["label"] = nodes.Label(self.block_select["box"], "Blocks:", "main", "xs", offset_str = "center", offset = (0, 10), zindex = 2)

        self.block_select["cards"] = []

        for i in range(len(self.blocks)):
            self.block_select["cards"].append(BlockCard(self.block_select["box"], i, self.global_assets["tile_maps"][0].grid[0][3], offset = (((((i % 2) * 2) - 1) * 70) - 60 , (i // 2 * 180) + 40), changerFunc = self.changeSelectedBlock))

        self.bottom_buttons = {"box" : nodes.BaseNode(self.side_panel, zindex = 1, offset_str = "bottom", offset = (0, -20))}
        self.bottom_buttons["save"] = Button(self.bottom_buttons["box"], (130, 65), self.global_assets["buttons"].grid[6][0], self.saveButton, offset_str = "bottom", offset = (-80, -45))
        self.bottom_buttons["save_timer"] = modifiers.Timer(self.bottom_buttons["save"].origin, 1.5, lambda: self.bottom_buttons["save"].sprite.change(image = self.global_assets["buttons"].grid[6][0]))
        self.bottom_buttons["delete"] = Button(self.bottom_buttons["box"], (130, 65), self.global_assets["buttons"].grid[8][0], self.showDeleteWindow, offset_str = "bottom", offset = (80, -45))

        self.delete_window = nodes.ColorBlock(self.parentNode, (self.parentNode.size), color = (0, 0, 0, 200), alpha_channel = True, zindex = 999)
        nodes.Label(self.delete_window, "Are you sure you want to delete this level?", "main", "l", offset_str = "center", offset = (0, -50))
        Button(self.delete_window, (100, 100), self.global_assets["arrows"].grid[0][7], self.delete, offset_str = "center", offset = (-100, 50))
        Button(self.delete_window, (100, 100), self.global_assets["arrows"].grid[0][5], lambda: self.showDeleteWindow(False), offset_str = "center", offset = (100, 50))

        self.delete_window.change(active = False)



    def load(self, level_data, name):
        # Bulk-load level data with reduced per-tile updates to avoid long stalls.
        self.loading = True
        
        self.changed = False

        self.level_data = level_data
        self.name = name

        self.noneditible = []

        self.delete_window.change(active = False)

        # Apply tile size first (may recreate internal structures)
        self.changeTileCount(self.level_data.get("tile_count_x", 20))
        self.changeTileSet(level_data.get("tile_set", 0)) # Apply tile set (may also recreate structures)
        self.level_grid.change(tile_node = self.global_assets["tile_maps"][self.level_data["tile_set"]])

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
                self.ground.addTile(coords, self.global_assets["tile_placement"]["ground"])

        # Player spawn: ensure the tile is present and marked
        pcoords = tuple(self.level_data["player_spawn"])
        try:
            self.ground.killTile(tuple(self.level_data["player_spawn"]))
        except Exception:
            pass
        if pcoords in self.ground.blocks.keys():
            self.ground.changeTile(pcoords, self.global_assets["tile_placement"]["player_spawn"])
        else:
            self.ground.addTile(pcoords, self.global_assets["tile_placement"]["player_spawn"])

        # Finish
        fcoords = tuple(self.level_data["finish"])
        try:
            self.ground.killTile(tuple(self.level_data["finish"]))
        except Exception:
            pass
        if fcoords in self.ground.blocks.keys():
            self.ground.changeTile(fcoords, self.global_assets["tile_placement"]["finish"])
        else:
            self.ground.addTile(fcoords, self.global_assets["tile_placement"]["finish"])

        # Spikes
        for spike in list(self.level_data["spikes"]):
            scoords = tuple(spike)
            if scoords in self.level_data["player_spawn"] or scoords in self.level_data["finish"]:
                continue
            if scoords in self.ground.blocks.keys():
                self.ground.changeTile(scoords, self.global_assets["tile_placement"]["spikes"])
            else:
                self.ground.addTile(scoords, self.global_assets["tile_placement"]["spikes"])
        
        for g_enemy in list(self.level_data["g_enemy"]):
            ecoords = tuple(g_enemy)
            if ecoords in self.level_data["player_spawn"] or ecoords in self.level_data["finish"]:
                continue
            if ecoords in self.ground.blocks.keys():
                self.ground.changeTile(ecoords, self.global_assets["tile_placement"]["g_enemy"])
            else:
                self.ground.addTile(ecoords, self.global_assets["tile_placement"]["g_enemy"])

        for f_enemy in list(self.level_data["f_enemy"]):
            ecoords = tuple(f_enemy)
            if ecoords in self.level_data["player_spawn"] or ecoords in self.level_data["finish"]:
                continue
            if ecoords in self.ground.blocks.keys():
                self.ground.changeTile(ecoords, self.global_assets["tile_placement"]["f_enemy"])
            else:
                self.ground.addTile(ecoords, self.global_assets["tile_placement"]["f_enemy"])

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

        self.changeSelectedBlock(0) # Ensure UI reflects the current block selection after loading

        self.updateNoneditible()
    

    def saveButton(self):
        self.save()

        self.bottom_buttons["save"].sprite.change(image = self.global_assets["buttons"].grid[7][0])

        self.bottom_buttons["save_timer"].end()
        self.bottom_buttons["save_timer"].start()

        self.updateNoneditible()


    def save(self):
        if self.changed:
            self.level_data["finished"] = False
            self.level_data["possible"] = False

        level_data = self.level_data

        """
        level_data["tile_size"] = list(self.level_grid.tile_size)
        level_data["ground"] = list(self.ground.blocks.keys())
        level_data["player_spawn"] = list(self.level_data["player_spawn"])
        level_data["finish"] = list(self.level_data["finish"])
        level_data["spikes"] = list(self.level_data["spikes"])
        """

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

        error_correction = (self.grid_encloser.position - self.grid_encloser.game.scenes.scenes[self.grid_encloser.game.scenes.current_scene].position)

        mouse_pos = pygame.Vector2(int(position_in_screen.x / self.grid_encloser.game.scale.x), int(position_in_screen.y / self.grid_encloser.game.scale.y)) - error_correction

        if mouse_pos.x < 0 or mouse_pos.y < 0 or mouse_pos.x > (self.grid_maxs[0] - self.grid_encloser.offset[0]) or mouse_pos.y > (self.grid_maxs[1] - self.grid_encloser.offset[1]):
            return

        coords = [int(mouse_pos.x // self.level_grid.tile_size[0]), int(mouse_pos.y // self.level_grid.tile_size[1])]
        
        self.place(coords)



    def place(self, coords):
        coords = tuple(coords)

        self.changed = True

        if self.selected_block == 0: #ground
            if coords in self.noneditible:
                return
            
            if self.placing:
                if list(coords) in self.level_data["ground"]:
                    return
                self.ground.addTile(coords, self.global_assets["tile_placement"]["ground"])
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
                self.ground.changeTile(coords, self.global_assets["tile_placement"]["player_spawn"])
                self.level_data["ground"].remove(list(coords))
                self.updateSurrounding(coords)
            else:
                self.ground.addTile(coords, self.global_assets["tile_placement"]["player_spawn"])

            self.level_data["player_spawn"] = list(coords)

            
        
        elif self.selected_block == 2: #finish

            if coords in self.noneditible:
                return

            self.ground.killTile(tuple(self.level_data["finish"]))

            if list(coords) in self.level_data["ground"]:
                self.ground.changeTile(coords, self.global_assets["tile_placement"]["finish"])
                self.level_data["ground"].remove(list(coords))
                self.updateSurrounding(coords)
            else:
                self.ground.addTile(coords, self.global_assets["tile_placement"]["finish"])

            self.level_data["finish"] = list(coords)

            

        
        elif self.selected_block == 3: #spikes
            if list(coords) == self.level_data["player_spawn"] or list(coords) == self.level_data["finish"]:
                return
            
            if self.placing:
                if list(coords) in self.level_data["spikes"]:
                    return
                
                if list(coords) in self.level_data["ground"]:
                    self.ground.changeTile(coords, self.global_assets["tile_placement"]["spikes"])
                    self.level_data["ground"].remove(list(coords))
                    self.updateSurrounding(coords)
                else:
                    self.ground.addTile(coords, self.global_assets["tile_placement"]["spikes"])
                self.level_data["spikes"].append(list(coords))

            else:
                if not list(coords) in self.level_data["spikes"]:
                    return
                self.level_data["spikes"].remove(list(coords))
                self.ground.killTile(coords)
        
        elif self.selected_block == 4: #ground_walking_enemy
            if list(coords) == self.level_data["player_spawn"] or list(coords) == self.level_data["finish"]:
                return
            
            if self.placing:
                if list(coords) in self.level_data["g_enemy"]:
                    return
                
                if list(coords) in self.level_data["ground"]:
                    self.ground.changeTile(coords, self.global_assets["tile_placement"]["g_enemy"])
                    self.level_data["ground"].remove(list(coords))
                    self.updateSurrounding(coords)
                else:
                    self.ground.addTile(coords, self.global_assets["tile_placement"]["g_enemy"])
                self.level_data["g_enemy"].append(list(coords))

            else:
                if not list(coords) in self.level_data["g_enemy"]:
                    return
                self.level_data["g_enemy"].remove(list(coords))
                self.ground.killTile(coords)
                
        
        elif self.selected_block == 5: #flying_enemy
            if list(coords) == self.level_data["player_spawn"] or list(coords) == self.level_data["finish"]:
                return
            
            if self.placing:
                if list(coords) in self.level_data["f_enemy"]:
                    return
                
                if list(coords) in self.level_data["ground"]:
                    self.ground.changeTile(coords, self.global_assets["tile_placement"]["f_enemy"])
                    self.level_data["ground"].remove(list(coords))
                    self.updateSurrounding(coords)
                else:
                    self.ground.addTile(coords, self.global_assets["tile_placement"]["f_enemy"])
                self.level_data["f_enemy"].append(list(coords))

            else:
                if not list(coords) in self.level_data["f_enemy"]:
                    return
                self.level_data["f_enemy"].remove(list(coords))
                self.ground.killTile(coords)
            

        
        if not self.loading:
            self.updateNoneditible()
    
    def updateSurrounding(self, coords):
        self.updateBlock([coords[0] + 1, coords[1]])
        self.updateBlock([coords[0], coords[1] + 1])
        self.updateBlock([coords[0] - 1, coords[1]])
        self.updateBlock([coords[0], coords[1] - 1])

    def updateBlock(self, coords):
        changeTileApearance(coords,self.global_assets, self.level_data, self.ground)
        

    def changeTileCount(self, count_x):
        last_count = self.level_data["tile_count_x"]
        tile_count = max(10, min(count_x, 90))
        size = [self.grid_maxs[0] / (tile_count - 1), self.grid_maxs[0] / (tile_count - 1)]

        size_int = int(size[0])
        if size[0] - float(int(size[0])) > 0.5:
            size[0] = int(size[0]) + 1
        else:
            size[0] = int(size[0])

        self.level_grid.change(one_tile_size = size)
        self.level_data["tile_count_x"] = tile_count
        self.tile_resize["text"].change(text = str(int(tile_count)))

        self.grid_encloser.change(offset = (-size[0] // 2, (size_int - (self.grid_maxs[1] % size_int)) // -2))


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
        for enemy_1 in self.level_data["g_enemy"]:
            self.noneditible.append(tuple(enemy_1))
        for enemy_2 in self.level_data["f_enemy"]:
            self.noneditible.append(tuple(enemy_2))
        self.noneditible.append(tuple(self.level_data["player_spawn"]))
        self.noneditible.append(tuple(self.level_data["finish"]))
    

    def changeTileSet(self, index = None):
        if index is not None:
            self.level_data["tile_set"] = index % len(self.global_assets["tile_maps"])
        else:
            self.level_data["tile_set"] = (self.level_data.get("tile_set", 0) + 1) % len(self.global_assets["tile_maps"])
        self.level_grid.change(tile_node = self.global_assets["tile_maps"][self.level_data["tile_set"]])
        self.background.change(image = self.global_assets["backgrounds"][self.level_data["tile_set"]].image)

        self.design_changer["icon"].change(image = self.level_icons.grid[self.level_data["tile_set"]][0])

        self.updateCards()

    
    def updateCards(self):
        card_icons = [
            self.global_assets["tile_maps"][self.level_data["tile_set"]].grid[self.global_assets["tile_placement"]["ground"][0]][self.global_assets["tile_placement"]["ground"][1]], 
            self.global_assets["tile_maps"][self.level_data["tile_set"]].grid[self.global_assets["tile_placement"]["player_spawn"][0]][self.global_assets["tile_placement"]["player_spawn"][1]], 
            self.global_assets["tile_maps"][self.level_data["tile_set"]].grid[self.global_assets["tile_placement"]["finish"][0]][self.global_assets["tile_placement"]["finish"][1]], 
            self.global_assets["tile_maps"][self.level_data["tile_set"]].grid[self.global_assets["tile_placement"]["spikes"][0]][self.global_assets["tile_placement"]["spikes"][1]], 
            self.global_assets["tile_maps"][self.level_data["tile_set"]].grid[self.global_assets["tile_placement"]["g_enemy"][0]][self.global_assets["tile_placement"]["g_enemy"][1]], 
            self.global_assets["tile_maps"][self.level_data["tile_set"]].grid[self.global_assets["tile_placement"]["f_enemy"][0]][self.global_assets["tile_placement"]["f_enemy"][1]]
        ]
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
