from platform import node

import pygame
from ZaKnode import *


class Button:
    def __init__(self, parentNode, size, surface, func, higherBy = 6, offset_str = None, offset = (0, 0)):
        self.origin = nodes.BaseNode(parentNode, offset_str = offset_str, offset = offset)
        self.sprite = nodes.SpriteBlock(self.origin, size, surface, offset_str = "Center")
        self.collision = nodes.CollisionArea(self.origin, 1)
        self.collision.addCollisionBlock(size, offset_str = "center")
        modifiers.Hover(self.origin, 1, lambda: self.hoverReize((size[0] + higherBy, size[1] + (size[1] * higherBy / size[0] if size[0] != 0 else 0))), else_func = lambda: self.noHoverResize(size))
        modifiers.ClickObject(self.origin, 1, function = func, button = 1)
    
    def hoverReize(self, size):
        self.sprite.change(size = size, offset_str = "center")
        self.collision.children[0].change(size = size, offset_str = "center")

    
    def noHoverResize(self, size):
        self.sprite.change(size = size, offset_str = "center")
        self.collision.children[0].change(size = size, offset_str = "center")

class ButtonText:
    def __init__(self, parentNode, text, font_name, func, white_txt = True, button_down = True, offset_str = None, offset = (0, 0)):
        self.offset_str = offset_str
        self.origin = nodes.BaseNode(parentNode, zindex = 4, offset_str = offset_str, offset = offset)
        self.sprite = nodes.TextBlock(self.origin, text, font_name, txt_color = (255, 255, 255) if white_txt else (0, 0, 0), bg_color = (0, 0, 0) if white_txt else (255, 255, 255), offset_str = offset_str)
        self.collision = nodes.CollisionArea(self.origin, 1)
        self.collision.addCollisionBlock(self.sprite.size, offset_str = offset_str)
        modifiers.Hover(self.origin, 1, lambda: self.hoverResize("l"), else_func = lambda: self.hoverResize("m"))
        self.click_mod = modifiers.ClickObject(self.origin, 1, function = func, button = 1, buttondown = button_down)
    
    def hoverResize(self, size):
        self.sprite.change(font_size = size, offset_str = self.offset_str)
        self.collision.children[0].change(size = self.sprite.size, offset_str = self.offset_str)


class PauseMenu:
    def __init__(self, game_level_node, parentNode, level_node, settings_node, scene_name, parent_scene_name):
        self.level_node = level_node
        self.game_level_node = game_level_node

        self.pause_menu = nodes.ColorBlock(parentNode, parentNode.size, color = (0, 0, 0, 200), zindex = 100, alpha_channel = True)

        nodes.Label(self.pause_menu, "Paused", "main", "xl", offset_str = "center", offset = (0, -300))
        Button(self.pause_menu, [110, 110], self.game_level_node.global_assets["arrows"].grid[0][6], self.pause, offset_str = "center", offset = (-330, 0))
        self.reset_button = Button(self.pause_menu, [110, 110], self.game_level_node.global_assets["arrows"].grid[0][4], self.reset, offset_str = "center", offset = (-130, 0))
        Button(self.pause_menu, [110, 110], self.game_level_node.global_assets["arrows"].grid[0][10], lambda: settings_node.open(scene_name), offset_str = "center", offset = (105, 0))
        Button(self.pause_menu, [110, 110], self.game_level_node.global_assets["arrows"].grid[0][11], lambda: parentNode.game.scenes.changeScene(parent_scene_name), offset_str = "center", offset = (330, 0))

        self.pause_menu.change(active = False)

        modifiers.PressKey(parentNode, pygame.K_ESCAPE, self.pause)
    
    def change(self, active = False):
        self.pause_menu.change(active = active)

    
    def pause(self):
        if not self.pause_menu.active:
            self.change(active = True)
            self.game_level_node.pause()
        
        else:
            self.change(active = False)
            self.game_level_node.unpause()
    
    def reset(self):
        self.game_level_node.reset()
        self.pause()
    


class PlayerMove(base.Modifier):
    def __init__(self, parentNode, colide_with : int, self_layers : int = None, die_layer : int = None, speed = 60, gravity = 10, jump_power = 35):
        super().__init__(parentNode)

        self.direction = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.jump = False
        self.on_ground = False

        self.a_pressed = False
        self.d_pressed = False

        if self_layers is None:
            self.self_colide = self.self_collide_all
        self.change(colide_with, self_layers, die_layer, speed, gravity, jump_power, active = True)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump = True
            elif event.key == pygame.K_a:
                self.a_pressed = True
            elif event.key == pygame.K_d:
                self.d_pressed = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.jump = False
            elif event.key == pygame.K_a:
                self.a_pressed = False
            elif event.key == pygame.K_d:
                self.d_pressed = False
        
        self.direction.x = (self.d_pressed - self.a_pressed) if (self.a_pressed or self.d_pressed) else 0
        super().event(event)
    
    def update(self):
        dt = self.parentNode.game.delta

        was_on_ground = self.on_ground
        self.on_ground = False
        self.velocity.x = self.direction.x * self.speed
        self.velocity.y += self.gravity * dt

        if self.jump and was_on_ground:
            self.velocity.y = -self.jump_power
            self.on_ground = False
            self.jump = False

        offset_change = pygame.Vector2(self.velocity.x * dt, self.velocity.y * dt)
        offset_change = self.collide_x(offset_change, self.game.scenes.scenes[self.game.scenes.current_scene])
        offset_change = self.collide_y(offset_change, self.game.scenes.scenes[self.game.scenes.current_scene])

        self.parentNode.change(offset = self.parentNode.offset + offset_change)
        super().update()

    def draw(self, scale = pygame.Vector2(1, 1)):
        super().draw(scale)

    def change(self, colide_with : int = None, self_layers : list = None, die_layer : int = None, speed = None, gravity = None, jump_power = None, active : bool = None):

        if colide_with is not None:
            self.physics_check = colide_with

        if self_layers is not None:
            self.self_colide_list = list(self_layers)
            self.self_colide = self.self_collide_check

        if die_layer is not None:
            self.die_layer = die_layer

        if speed is not None:
            self.speed = speed

        if gravity is not None:
            self.gravity = gravity

        if jump_power is not None:
            self.jump_power = jump_power

        super().modifierChange(active = active)

    def kill(self):
        super().kill()

    def self_collide_all(self, physics_layer):
        return True

    def self_collide_check(self, physics_layer):
        return physics_layer in self.self_colide_list

    def get_overlap(self, ownHitBox, targetHB):
        def get_bounds(shape):
            if hasattr(shape, "position") and hasattr(shape, "size"):
                left = float(shape.position.x)
                top = float(shape.position.y)
                width = float(shape.size.x)
                height = float(shape.size.y)
                return left, top, left + width, top + height

            rect = shape.rect if hasattr(shape, "rect") else shape
            return rect.left, rect.top, rect.right, rect.bottom

        own_left, own_top, own_right, own_bottom = get_bounds(ownHitBox)
        target_left, target_top, target_right, target_bottom = get_bounds(targetHB)

        overlap_x = min(own_right, target_right) - max(own_left, target_left)
        overlap_y = min(own_bottom, target_bottom) - max(own_top, target_top)
        return overlap_x, overlap_y

    def collide_x(self, offset_change, parent_node):
        new_change = pygame.Vector2(offset_change)
        if not hasattr(parent_node, "children"):
            return new_change

        for node in parent_node.children:
            child_change = self.collide_x(new_change, node)
            if child_change != new_change:
                return child_change

            if not isinstance(node, nodes.CollisionArea):
                continue

            if node.physics_layer != self.physics_check:
                continue

            for ownHitArea in self.parentNode.collision:
                if not self.self_colide(ownHitArea.physics_layer):
                    continue

                for ownHitBox in ownHitArea.collision_blocks:
                    ownHitBox.update()
                    predicted_left = ownHitBox.position.x + offset_change.x
                    predicted_top = ownHitBox.position.y
                    predicted_right = predicted_left + ownHitBox.size.x
                    predicted_bottom = predicted_top + ownHitBox.size.y

                    for targetHB in node.collision_blocks:
                        targetHB.update()
                        target_left = targetHB.position.x
                        target_top = targetHB.position.y
                        target_right = target_left + targetHB.size.x
                        target_bottom = target_top + targetHB.size.y

                        if predicted_right <= target_left or predicted_left >= target_right:
                            continue
                        if predicted_bottom <= target_top or predicted_top >= target_bottom:
                            continue

                        overlap_x = min(predicted_right, target_right) - max(predicted_left, target_left)
                        overlap_y = min(predicted_bottom, target_bottom) - max(predicted_top, target_top)
                        if overlap_x <= 0 or overlap_y <= 0:
                            continue

                        if overlap_x >= overlap_y:
                            continue

                        if offset_change.x > 0: # Moving right
                            penetration = predicted_right - target_left
                            new_change.x = offset_change.x - penetration
                            self.velocity.x = 0
                        elif offset_change.x < 0: # Moving left
                            penetration = target_right - predicted_left
                            new_change.x = offset_change.x + penetration
                            self.velocity.x = 0

                        ownHitBox.update()
        return new_change

    def collide_y(self, offset_change, parent_node):
        new_change = pygame.Vector2(offset_change)
        if not hasattr(parent_node, "children"):
            return new_change

        for node in parent_node.children:
            child_change = self.collide_y(new_change, node)
            if child_change != new_change:
                return child_change

            if not isinstance(node, nodes.CollisionArea):
                continue

            if node.physics_layer != self.physics_check:
                continue

            for ownHitArea in self.parentNode.collision:
                if not self.self_colide(ownHitArea.physics_layer):
                    continue

                for ownHitBox in ownHitArea.collision_blocks:
                    ownHitBox.update()
                    predicted_left = ownHitBox.position.x
                    predicted_top = ownHitBox.position.y + offset_change.y
                    predicted_right = predicted_left + ownHitBox.size.x
                    predicted_bottom = predicted_top + ownHitBox.size.y

                    for targetHB in node.collision_blocks:
                        targetHB.update()
                        target_left = targetHB.position.x
                        target_top = targetHB.position.y
                        target_right = target_left + targetHB.size.x
                        target_bottom = target_top + targetHB.size.y

                        if predicted_right <= target_left or predicted_left >= target_right:
                            continue
                        if predicted_bottom <= target_top or predicted_top >= target_bottom:
                            continue

                        overlap_x = min(predicted_right, target_right) - max(predicted_left, target_left)
                        overlap_y = min(predicted_bottom, target_bottom) - max(predicted_top, target_top)
                        if overlap_x <= 0 or overlap_y <= 0:
                            continue

                        if overlap_y >= overlap_x:
                            continue

                        if offset_change.y > 0: # Moving down
                            penetration = predicted_bottom - target_top
                            new_change.y = offset_change.y - penetration
                            self.velocity.y = 0
                            self.on_ground = True
                        elif offset_change.y < 0: # Moving up
                            penetration = target_bottom - predicted_top
                            new_change.y = offset_change.y + penetration
                            self.velocity.y = 0

                        ownHitBox.update()
        return new_change


class EnemyMove(PlayerMove):
    def __init__(self, parentNode, colide_with : int, self_layers : int = None, die_layer : int = None, speed = 60, gravity = 0, jump_power = 0):
        super().__init__(parentNode, colide_with, self_layers, die_layer, speed = speed, gravity = gravity, jump_power = jump_power)
        self.direction = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.jump = False
        self.on_ground = False

    def event(self, event):
        pass

    def update(self):
        dt = self.parentNode.game.delta

        self.on_ground = False
        self.velocity.x = self.direction.x * self.speed
        if self.gravity:
            self.velocity.y += self.gravity * dt
        else:
            self.velocity.y = self.direction.y * self.speed

        offset_change = pygame.Vector2(self.velocity.x * dt, self.velocity.y * dt)
        offset_change = self.collide_x(offset_change, self.game.scenes.scenes[self.game.scenes.current_scene])
        offset_change = self.collide_y(offset_change, self.game.scenes.scenes[self.game.scenes.current_scene])

        self.parentNode.change(offset = self.parentNode.offset + offset_change)
        super().update()

    def self_collide_all(self, physics_layer):
        return True

    def self_collide_check(self, physics_layer):
        return physics_layer in self.self_colide_list

    def get_overlap(self, ownHitBox, targetHB):
        def get_bounds(shape):
            if hasattr(shape, "position") and hasattr(shape, "size"):
                left = float(shape.position.x)
                top = float(shape.position.y)
                width = float(shape.size.x)
                height = float(shape.size.y)
                return left, top, left + width, top + height

            rect = shape.rect if hasattr(shape, "rect") else shape
            return rect.left, rect.top, rect.right, rect.bottom

        own_left, own_top, own_right, own_bottom = get_bounds(ownHitBox)
        target_left, target_top, target_right, target_bottom = get_bounds(targetHB)

        overlap_x = min(own_right, target_right) - max(own_left, target_left)
        overlap_y = min(own_bottom, target_bottom) - max(own_top, target_top)
        return overlap_x, overlap_y

    def collide_x(self, offset_change, parent_node):
        new_change = pygame.Vector2(offset_change)
        if not hasattr(parent_node, "children"):
            return new_change

        for node in parent_node.children:
            child_change = self.collide_x(new_change, node)
            if child_change != new_change:
                return child_change

            if not isinstance(node, nodes.CollisionArea):
                continue

            if node.physics_layer != self.physics_check:
                continue

            for ownHitArea in self.parentNode.collision:
                if not self.self_colide(ownHitArea.physics_layer):
                    continue

                for ownHitBox in ownHitArea.collision_blocks:
                    ownHitBox.update()
                    predicted_left = ownHitBox.position.x + offset_change.x
                    predicted_top = ownHitBox.position.y
                    predicted_right = predicted_left + ownHitBox.size.x
                    predicted_bottom = predicted_top + ownHitBox.size.y

                    for targetHB in node.collision_blocks:
                        targetHB.update()
                        target_left = targetHB.position.x
                        target_top = targetHB.position.y
                        target_right = target_left + targetHB.size.x
                        target_bottom = target_top + targetHB.size.y

                        if predicted_right <= target_left or predicted_left >= target_right:
                            continue
                        if predicted_bottom <= target_top or predicted_top >= target_bottom:
                            continue

                        overlap_x = min(predicted_right, target_right) - max(predicted_left, target_left)
                        overlap_y = min(predicted_bottom, target_bottom) - max(predicted_top, target_top)
                        if overlap_x <= 0 or overlap_y <= 0:
                            continue

                        if overlap_x >= overlap_y:
                            continue

                        if offset_change.x > 0: # Moving right
                            penetration = predicted_right - target_left
                            new_change.x = offset_change.x - penetration
                            self.velocity.x = 0
                        elif offset_change.x < 0: # Moving left
                            penetration = target_right - predicted_left
                            new_change.x = offset_change.x + penetration
                            self.velocity.x = 0

                        ownHitBox.update()
        return new_change

    def collide_y(self, offset_change, parent_node):
        new_change = pygame.Vector2(offset_change)
        if not hasattr(parent_node, "children"):
            return new_change

        for node in parent_node.children:
            child_change = self.collide_y(new_change, node)
            if child_change != new_change:
                return child_change

            if not isinstance(node, nodes.CollisionArea):
                continue

            if node.physics_layer != self.physics_check:
                continue

            for ownHitArea in self.parentNode.collision:
                if not self.self_colide(ownHitArea.physics_layer):
                    continue

                for ownHitBox in ownHitArea.collision_blocks:
                    ownHitBox.update()
                    predicted_left = ownHitBox.position.x
                    predicted_top = ownHitBox.position.y + offset_change.y
                    predicted_right = predicted_left + ownHitBox.size.x
                    predicted_bottom = predicted_top + ownHitBox.size.y

                    for targetHB in node.collision_blocks:
                        targetHB.update()
                        target_left = targetHB.position.x
                        target_top = targetHB.position.y
                        target_right = target_left + targetHB.size.x
                        target_bottom = target_top + targetHB.size.y

                        if predicted_right <= target_left or predicted_left >= target_right:
                            continue
                        if predicted_bottom <= target_top or predicted_top >= target_bottom:
                            continue

                        overlap_x = min(predicted_right, target_right) - max(predicted_left, target_left)
                        overlap_y = min(predicted_bottom, target_bottom) - max(predicted_top, target_top)
                        if overlap_x <= 0 or overlap_y <= 0:
                            continue

                        if overlap_y >= overlap_x:
                            continue

                        if offset_change.y > 0: # Moving down
                            penetration = predicted_bottom - target_top
                            new_change.y = offset_change.y - penetration
                            self.velocity.y = 0
                            self.on_ground = True
                        elif offset_change.y < 0: # Moving up
                            penetration = target_bottom - predicted_top
                            new_change.y = offset_change.y + penetration
                            self.velocity.y = 0

                        ownHitBox.update()
        return new_change



class GameLevel:
    def __init__(self, scene, global_assets, finish_func, settings_node, scene_name, level_name, level_node, previous_scene):
        self.scene = scene
        self.global_assets = global_assets
        self.finish_func = finish_func

        self.level_name = level_name

        self.level_data = {
            "tile_count_x": 20,
            "tile_set": 0,
            "player_spawn": [1, 1],
            "finish": [2, 1],
            "possible": False,
            "finished": False,
            "spikes" : [],
            "ground" : [],
            "g_enemy" : [],
            "f_enemy" : []
        }

        # Physics layers:
        # 1: Player 
        # 2: Ground
        # 3: Death
        # 4: Finish

        self.background = nodes.SpriteBlock(self.scene, self.scene.size, self.global_assets["backgrounds"][0].image, offset = (0, 0), zindex = -5)

        self.label = nodes.Label(self.scene, "none", "main", "xl", offset_str = "top", offset = (0, 20),  zindex = 100)

        self.pause_menu = PauseMenu(self, self.scene, level_node, settings_node, scene_name, previous_scene)

        self.player = {
            "box" : nodes.BaseNode(self.scene, zindex = 100, offset = (400, 0))
        }
        self.player["sprite"] = nodes.AnimatedSpriteBlock(self.player["box"], (40, 40), self.global_assets["animations"][self.level_data["tile_set"]]["player"]["idle"]["right"].frames, fps = 3, offset = [0, 0])
        self.player["collision"] = nodes.CollisionArea(self.player["box"], 1)
        self.player["collision"].addCollisionBlock((40, 40), offset = [0, 0])
        self.player["move"] = PlayerMove(self.player["box"], colide_with = 2, die_layer = 3, gravity = 400, speed = 500, jump_power = 300)
        self.player["modifier"] = modifiers.OnCollideDo(self.player["box"], self.playerDeath, 3)
        self.player["dead"] = False
        self.player["init_offset"] = (0, 0)
        self.player["current_anim"] = "idle" 
        self.player["last_dir"] = "right" 

        self.last_pos = self.player["box"].offset
        self.new_pos = self.player["box"].offset


        self.finish = {
            "box" : nodes.BaseNode(self.scene, zindex = 100, offset = (1800, 200))
        }
        finish_tile = self.global_assets["tile_placement"]["finish"]
        self.finish["sprite"] = nodes.SpriteBlock(self.finish["box"], (40, 40), self.global_assets["tile_maps"][0].grid[finish_tile[0]][finish_tile[1]], offset = [0, 0])
        self.finish["collision"] = nodes.CollisionArea(self.finish["box"], 4)
        self.finish["collision"].addCollisionBlock((40, 40), offset = [0, 0])
        self.finish["timer"] = modifiers.Timer(self.finish["box"], 2.5, lambda: self.scene.game.scenes.changeScene(previous_scene))

        modifiers.OnCollideDo(self.finish["box"], self.finish_level, 1)

        self.finished = False

        self.enemys = []

        self.grid_encloser = nodes.BaseNode(self.scene, zindex = 10)
        self.reset_timer = modifiers.Timer(self.grid_encloser, 1.2, self.reset)
        self.grid = nodes.TileMap(self.grid_encloser, self.global_assets["tile_maps"][0], (200, 200))
        self.ground = nodes.TileMapLayer(self.grid, True, 2)

        self.cover = nodes.SpriteBlock(self.scene, self.scene.size, self.global_assets["backgrounds"][0].image, offset = (0, 0), zindex = 50)

        self.cover.change(active = False)
        self.transparency = 0 # 0 - 255, 0 being fully invisible, 255 being fully visible

        modifiers.ForeverDo(self.scene, self.coverSight)



    def load(self, directory, name):
        level_data = resources.ReadData(directory)

        self.level_name = name
        self.pause_menu.change(active = False)
        
        self.label.change(text = name.removesuffix(".txt").upper(), offset_str = "top", offset = (0, 20), zindex = 100)

        tile_size = self.scene.size[0] / (level_data["tile_count_x"] - 1)
        tile_for_y = int(tile_size)
        if tile_size - float(int(tile_size)) > 0.5:
            tile_size = int(tile_size) + 1
        else:
            tile_size = int(tile_size)


        self.grid_encloser.change(offset = (-tile_size // 2, (tile_for_y - (self.scene.size[1] % tile_for_y)) // -2))
        self.grid.change(tile_node = self.global_assets["tile_maps"][level_data["tile_set"]], one_tile_size = (tile_size, tile_size))

        self.background.change(image = self.global_assets["backgrounds"][level_data["tile_set"]].image)
        self.cover.change(image = self.global_assets["backgrounds"][level_data["tile_set"]].image)

        for block in list(self.ground.blocks.keys()):
            self.ground.killTile(block)
            self.ground.killCollision(block)

        for enemy in list(self.enemys):
            enemy.kill()
        
        self.enemys.clear()


        for block in level_data["ground"]:
            self.ground.addTile(block, self.global_assets["tile_placement"]["ground"])
            self.ground.addCollision(block)
            changeTileApearance(block, self.global_assets, level_data, self.ground)
            changeTileApearance([block[0] + 1, block[1]], self.global_assets, level_data, self.ground)
            changeTileApearance([block[0], block[1] + 1], self.global_assets, level_data, self.ground)
            changeTileApearance([block[0] - 1, block[1]], self.global_assets, level_data, self.ground)
            changeTileApearance([block[0], block[1] - 1], self.global_assets, level_data, self.ground)
        
        for spike in level_data["spikes"]:
            self.enemys.append(Spike(self.grid_encloser, self.global_assets, (tile_size, tile_size), spike, level_data["tile_set"]))

        for g_enemy in level_data.get("g_enemy", []):
            self.enemys.append(G_Enemy(self.grid_encloser, self.global_assets, (tile_size, tile_size), g_enemy, level_data["tile_set"], self.player["box"]))

        for f_enemy in level_data.get("f_enemy", []):
            self.enemys.append(F_Enemy(self.grid_encloser, self.global_assets, (tile_size, tile_size), f_enemy, level_data["tile_set"], self.player["box"]))

        self.player["init_offset"] = (level_data["player_spawn"][0] * tile_size + self.grid_encloser.offset[0], level_data["player_spawn"][1] * tile_size + self.grid_encloser.offset[1])
        self.player["box"].change(offset = self.player["init_offset"])
        self.player["sprite"].change(size = self.grid.tile_size)
        self.player["sprite"].change(frames_arr = self.global_assets["animations"][level_data["tile_set"]]["player"]["idle"]["right"].frames, fps = 3)

        self.player["collision"].collision_blocks[0].change(size = (self.grid.tile_size[0] * 0.7, self.grid.tile_size[1] * 0.8), offset = (self.grid.tile_size[0] * 0.15, self.grid.tile_size[1] * 0.2))
        self.player["move"].change(gravity = 600 * (self.grid.tile_size[1] / 40), speed = 200 * (self.grid.tile_size[0] / 40), jump_power = 320 * (self.grid.tile_size[1] / 40), active = True)

        self.player["move"].a_pressed = False
        self.player["move"].d_pressed = False
        self.player["move"].jump = False
        self.player["move"].direction = pygame.Vector2(0, 0)
        self.player["move"].velocity = pygame.Vector2(0, 0)

        self.finish["box"].change(offset = (level_data["finish"][0] * self.grid.tile_size[0] + self.grid_encloser.offset[0], level_data["finish"][1] * self.grid.tile_size[1] + self.grid_encloser.offset[1]))
        self.finish["sprite"].change(size = self.grid.tile_size)
        self.finish["collision"].collision_blocks[0].change(size = (self.grid.tile_size[0] * 0.8, self.grid.tile_size[1] * 0.8), offset = (self.grid.tile_size[0] * 0.1, self.grid.tile_size[1] * 0.1))
        self.finish["timer"].end()

        self.finished = False

        self.level_data = level_data

    def coverSight(self):
        if self.player["dead"] or self.finished:
            return
        
        self.new_pos = pygame.Vector2(int(self.player["box"].offset[0]), int(self.player["box"].offset[1]))

        if self.new_pos.x + self.player["sprite"].size[0] > self.scene.size[0] or self.new_pos.x < 0 or self.new_pos.y + self.player["sprite"].size[1] > self.scene.size[1]:
            self.playerDeath()
            return

        if self.new_pos.distance_to(self.last_pos) > 2 or not self.player["move"].on_ground:
            self.cover.change(active = True)
            #self.transparency = max(0, self.transparency - 40)
        else:
            self.cover.change(active = False)
            #self.transparency = min(255, self.transparency + 50)

        """#new_background = self.global_assets["backgrounds"][self.level_data["tile_set"]].image.copy()
        #self.cover.change(image = new_background.set_alpha(self.transparency))"""
        
        x_dif = self.new_pos.x - self.last_pos.x
        y_dif = self.new_pos.y - self.last_pos.y

        dir_changed = self.figurePlayerDirection(x_dif)
        self.managePlayerAnimation(x_dif, y_dif, dir_changed)
        self.last_pos = self.new_pos

    
    def figurePlayerDirection(self, x_dif):
        last_dir = self.player["last_dir"]
        if x_dif > 0:
            self.player["last_dir"] = "right"
        elif x_dif < 0:
            self.player["last_dir"] = "left"
        
        return last_dir != self.player["last_dir"]

    
    def managePlayerAnimation(self, x_dif, y_dif, dir_changed):
        if self.player["move"].on_ground:
            if abs(x_dif) < 0.5:
                if self.player["current_anim"] != "idle" or dir_changed:
                    self.player["sprite"].change(frames_arr = self.global_assets["animations"][self.level_data["tile_set"]]["player"]["idle"][self.player["last_dir"]].frames, fps = 5)
                    self.player["current_anim"] = "idle"
            else:
                if self.player["current_anim"] != "run" or dir_changed:
                    self.player["sprite"].change(frames_arr = self.global_assets["animations"][self.level_data["tile_set"]]["player"]["run"][self.player["last_dir"]].frames, fps = 20)
                    self.player["current_anim"] = "run"
        else:
            if y_dif < 0:
                if self.player["current_anim"] != "jump" or dir_changed:
                    self.player["sprite"].change(frames_arr = self.global_assets["animations"][self.level_data["tile_set"]]["player"]["jump"][self.player["last_dir"]].frames, fps = 1)
                    self.player["current_anim"] = "jump"
            else:
                if self.player["current_anim"] != "fall" or dir_changed:
                    self.player["sprite"].change(frames_arr = self.global_assets["animations"][self.level_data["tile_set"]]["player"]["fall"][self.player["last_dir"]].frames, fps = 20)
                    self.player["current_anim"] = "fall"


    def reset(self):
        self.finished = False
        
        for enemy in self.enemys:
            enemy.active = True
            enemy.box.change(offset = enemy.init_offset, active = True)
            if hasattr(enemy, "move"):
                enemy.move.change(active = True)

        
        self.player["box"].change(offset = self.player["init_offset"])
        self.player["move"].change(active = True)
        self.player["move"].a_pressed = False
        self.player["move"].d_pressed = False
        self.player["move"].jump = False
        self.player["move"].direction = pygame.Vector2(0, 0)
        self.player["move"].velocity = pygame.Vector2(0, 0)
        self.player["sprite"].change(frames_arr = self.global_assets["animations"][self.level_data["tile_set"]]["player"]["idle"]["right"].frames, fps = 5)
        self.player["collision"].change(active = True)
        self.player["dead"] = False
    
    def pause(self):
        if self.player["dead"] or self.finished:
            self.pause_menu.change(active = False)
            return
        
        self.player["move"].change(active = False)
        
        for enemy in self.enemys:
            enemy.active = False

            if hasattr(enemy, "move"):
                enemy.move.change(active = False)
    
    def unpause(self):
        self.player["move"].change(active = True)
        for enemy in self.enemys:
            enemy.active = True

            if hasattr(enemy, "move"):
                enemy.move.change(active = True)


    def playerDeath(self):
        self.player["dead"] = True
        self.cover.change(active = False)
        self.player["move"].change(active = False)
        self.player["move"].a_pressed = False
        self.player["move"].d_pressed = False
        self.player["sprite"].change(frames_arr = self.global_assets["animations"][self.level_data["tile_set"]]["player"]["fall"][self.player["last_dir"]].frames, fps = 40)
        self.player["collision"].change(active = False)
        self.player["current_anim"] = "fall"
        

        for enemy in self.enemys:
            enemy.active = False

            if hasattr(enemy, "move"):
                enemy.move.change(active = False)

        self.reset_timer.start()
    
    def finish_level(self):
        if self.finished:
            return

        self.finished = True

        self.finish_func()

        self.player["sprite"].change(frames_arr = self.global_assets["animations"][self.level_data["tile_set"]]["player"]["finish"].frames, fps = 20)
        self.player["move"].change(active = False)

        self.cover.change(active = False)

        for enemy in self.enemys:
            enemy.active = False

            if hasattr(enemy, "move"):
                enemy.move.change(active = False)

        self.finish["timer"].start()


class Spike:
    def __init__(self, parent, global_assets, size, coords, tile_set):
        self.parent = parent
        self.global_assets = global_assets

        self.init_offset = (coords[0] * size[0], coords[1] * size[1])

        self.active = True

        self.box = nodes.BaseNode(self.parent, zindex = 100, offset = self.init_offset)
        spikes = self.global_assets["tile_placement"]["spikes"]
        self.sprite = nodes.SpriteBlock(self.box, size, self.global_assets["tile_maps"][tile_set].grid[spikes[0]][spikes[1]], offset = [0, 0])
        self.collision = nodes.CollisionArea(self.box, 3)
        self.collision.addCollisionBlock([size[0] * 0.8, size[1] * 0.5], offset = [size[0] * 0.1, size[1] * 0.5])
    
    def kill(self):
        self.box.kill()

class G_Enemy:
    def __init__(self, scene, global_assets, size, coords, tile_set, player_box):
        self.scene = scene
        self.global_assets = global_assets

        self.tile_set = tile_set

        self.init_offset = (coords[0] * size[0], coords[1] * size[1])
        self.player_box = player_box
        self.chase_distance = size[0] * 5

        self.box = nodes.BaseNode(self.scene, zindex = 100, offset = self.init_offset)
        self.sprite = nodes.AnimatedSpriteBlock(self.box, size, self.global_assets["animations"][tile_set]["g_enemy"]["idle"]["right"].frames, fps = 1, offset = [0, 0])
        self.collision = nodes.CollisionArea(self.box, 3)
        self.collision.addCollisionBlock([size[0] * 0.8, size[1] * 0.6], offset = [size[0] * 0.1, size[1] * 0.4])
        self.move = EnemyMove(self.box, colide_with = 2, gravity = 240 * (size[1] / 40), speed = 40 * (size[0] / 40))

        self.current_anim = "idle"
        self.last_dir = "right"
        self.current_dir = "right"
        self.move_func = modifiers.ForeverDo(self.box, self.moveFunc)

    def moveFunc(self):
        if not self.box.active:
            return

        distance = self.box.position.distance_to(self.player_box.position)
        if distance < self.chase_distance:
            x_diff = self.player_box.position.x - self.box.position.x
            # Hysteresis deadzone to avoid rapid direction flipping when near player
            start_threshold = self.sprite.size.x * 0.6
            stop_threshold = self.sprite.size.x * 0.25

            if abs(x_diff) > start_threshold:
                # start moving toward player
                self.move.direction.x = 1 if x_diff > 0 else -1
            elif abs(x_diff) < stop_threshold:
                # close enough: stop
                self.move.direction.x = 0
            else:
                # between thresholds: keep current direction (hysteresis)
                pass
        else:
            self.move.direction.x = 0

        self.last_dir = self.current_dir
        # Update facing only when moving; preserve facing while idle
        if self.move.direction.x > 0:
            self.current_dir = "left"
        elif self.move.direction.x < 0:
            self.current_dir = "right"

        if self.move.direction.x != 0:
            if self.current_anim != "run" or self.last_dir != self.current_dir:
                self.sprite.change(frames_arr = self.global_assets["animations"][self.tile_set]["g_enemy"]["run"][self.current_dir].frames, fps = 10)
                self.current_anim = "run"
        else:
            if self.current_anim != "idle":
                self.sprite.change(frames_arr = self.global_assets["animations"][self.tile_set]["g_enemy"]["idle"][self.current_dir].frames, fps = 1)
                self.current_anim = "idle"

    def kill(self):
        self.box.kill()


class F_Enemy:
    def __init__(self, scene, global_assets, size, coords, tile_set, player_box):
        self.scene = scene
        self.global_assets = global_assets
        self.tile_set = tile_set

        self.init_offset = (coords[0] * size[0], coords[1] * size[1])
        self.player_box = player_box
        self.chase_distance = size[0] * 6

        self.box = nodes.BaseNode(self.scene, zindex = 100, offset = self.init_offset)
        self.sprite = nodes.AnimatedSpriteBlock(self.box, size, self.global_assets["animations"][tile_set]["f_enemy"]["idle"]["right"].frames, fps = 20, offset = [0, 0])
        self.collision = nodes.CollisionArea(self.box, 3)
        self.collision.addCollisionBlock([size[0] * 0.7, size[1] * 0.7], offset = [size[0] * 0.15, size[1] * 0.15])
        self.move = EnemyMove(self.box, colide_with = 2, gravity = 0, speed = 55 * (size[0] / 40))

        self.current_anim = "idle"
        self.last_dir = "right"
        self.current_dir = "right"
        self.move_func = modifiers.ForeverDo(self.box, self.moveFunc)

    def moveFunc(self):
        if not self.box.active:
            return

        distance = self.box.position.distance_to(self.player_box.position)
        if distance < self.chase_distance:
            diff = self.player_box.position - self.box.position
            if diff.length() > 0:
                self.move.direction = diff.normalize()
            else:
                self.move.direction = pygame.Vector2(0, 0)
        else:
            self.move.direction = pygame.Vector2(0, 0)

        self.last_dir = self.current_dir 
        self.current_dir = "right" if self.move.direction.x > 0 else "left"

        if self.last_dir != self.current_dir:
            self.sprite.change(frames_arr = self.global_assets["animations"][self.tile_set]["f_enemy"]["idle"][self.last_dir].frames, fps = 20)

    def kill(self):
        self.box.kill()

def changeTileApearance(coords, global_assets, level_data, ground):
    coords = tuple(coords)

    if not list(coords) in level_data["ground"] or not coords in ground.blocks.keys():
        return

    coord_check = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    checks = []

    states = {
        (False, False, False, False) : global_assets["tile_placement"]["ground"],
        (False, False, False, True) : global_assets["tile_placement"]["ground_L"],
        (False, False, True, False) : global_assets["tile_placement"]["ground_B"],
        (False, False, True, True) : global_assets["tile_placement"]["ground_BL"],
        (False, True, False, False) : global_assets["tile_placement"]["ground_R"],
        (False, True, False, True) : global_assets["tile_placement"]["ground_LR"],
        (False, True, True, False) : global_assets["tile_placement"]["ground_BR"],
        (False, True, True, True) : global_assets["tile_placement"]["ground_BLR"],
        (True, False, False, False) : global_assets["tile_placement"]["ground_T"],
        (True, False, False, True) : global_assets["tile_placement"]["ground_TL"],
        (True, False, True, False) : global_assets["tile_placement"]["ground_TB"],
        (True, False, True, True) : global_assets["tile_placement"]["ground_TBL"],
        (True, True, False, False) : global_assets["tile_placement"]["ground_TR"],
        (True, True, False, True) : global_assets["tile_placement"]["ground_TLR"],
        (True, True, True, False) : global_assets["tile_placement"]["ground_TBR"],
        (True, True, True, True) : global_assets["tile_placement"]["ground_TBLR"]
    }

    for checked in coord_check:
        temp = [coords[0] + checked[0], coords[1] + checked[1]]

        checks.append(temp in level_data["ground"])
    
    ground.changeTile(coords, states[tuple(checks)])