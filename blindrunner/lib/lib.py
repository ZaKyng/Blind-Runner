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
    def __init__(self, parentNode, level_node, name, settings_node, scene_name, parent_scene_name):
        self.level_node = level_node

        self.pause_menu = nodes.ColorBlock(parentNode, parentNode.size, color = (0, 0, 0, 200), zindex = 100, alpha_channel = True)

        nodes.Label(self.pause_menu, "Paused", "main", "xl", offset_str = "center", offset = (0, -300))
        ButtonText(self.pause_menu, "Return", "main", lambda: self.change(active = self.pause_menu.active == False), white_txt = False, offset_str = "center", offset = (-330, 0))
        self.reset_button = ButtonText(self.pause_menu, "Reset", "main", lambda: self.level_node.load(name), white_txt = False, offset_str = "center", offset = (-130, 0))
        ButtonText(self.pause_menu, "Settings", "main", lambda: settings_node.open(scene_name), white_txt = False, offset_str = "center", offset = (105, 0))
        ButtonText(self.pause_menu, "Leave", "main", lambda: parentNode.game.scenes.changeScene(parent_scene_name), white_txt = False, offset_str = "center", offset = (330, 0))

        self.pause_menu.change(active = False)

        modifiers.PressKey(parentNode, pygame.K_ESCAPE, lambda: self.change(active = self.pause_menu.active == False))
    
    def change(self, active = False):
        self.pause_menu.change(active = active)
    
    def update(self, name):
        self.reset_button.click_mod.change(func = lambda: self.level_node.load(name))


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



class GameLevel:
    def __init__(self, scene, global_assets, finish_func):
        self.scene = scene
        self.global_assets = global_assets
        self.finish_func = finish_func

        # Physics layers:
        # 1: Player 
        # 2: Ground
        # 3: Death
        # 4: Finish

        self.background = nodes.SpriteBlock(self.scene, self.scene.size, self.global_assets["backgrounds"][0].image, offset = (0, 0), zindex = -5)

        self.player = {
            "box" : nodes.BaseNode(self.scene, zindex = 100, offset = (400, 0))
        }
        self.player["sprite"] = nodes.AnimatedSpriteBlock(self.player["box"], (40, 40), self.global_assets["animations"]["player"]["idle_r"].frames, fps = 3, offset = [0, 0])
        self.player["collision"] = nodes.CollisionArea(self.player["box"], 1)
        self.player["collision"].addCollisionBlock((40, 40), offset = [0, 0])
        self.player["move"] = PlayerMove(self.player["box"], colide_with = 2, die_layer = 3, gravity = 400, speed = 500, jump_power = 300)

        self.last_pos = self.player["box"].offset
        self.new_pos = self.player["box"].offset


        self.finish = {
            "box" : nodes.BaseNode(self.scene, zindex = 100, offset = (1800, 200))
        }
        self.finish["sprite"] = nodes.SpriteBlock(self.finish["box"], (40, 40), self.global_assets["tile_maps"][0].grid[4][3], offset = [0, 0])
        self.finish["collision"] = nodes.CollisionArea(self.finish["box"], 4)
        self.finish["collision"].addCollisionBlock((40, 40), offset = [0, 0])

        modifiers.OnCollideDo(self.finish["box"], self.finish_func, 1)

        self.grid_encloser = nodes.BaseNode(self.scene, zindex = 10)
        self.grid = nodes.TileMap(self.grid_encloser, self.global_assets["tile_maps"][0], (200, 200))
        self.ground = nodes.TileMapLayer(self.grid, True, 2)

        self.cover = nodes.SpriteBlock(self.scene, self.scene.size, self.global_assets["backgrounds"][0].image, offset = (0, 0), zindex = 50)
        #self.cover.change(active = False)

        modifiers.ForeverDo(self.scene, self.coverSight)



    def load(self, directory):
        level_data = resources.ReadData(directory)

        tile_size = self.scene.size[0] / (level_data["tile_count_x"] - 1)
        tile_for_y = int(tile_size)
        if tile_size - int(tile_size) > 0.5:
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

        for block in level_data["ground"]:
            self.ground.addTile(block, self.global_assets["tile_placement"]["ground"])
            self.ground.addCollision(block)
            changeTileApearance(block, self.global_assets, level_data, self.ground)
            changeTileApearance([block[0] + 1, block[1]], self.global_assets, level_data, self.ground)
            changeTileApearance([block[0], block[1] + 1], self.global_assets, level_data, self.ground)
            changeTileApearance([block[0] - 1, block[1]], self.global_assets, level_data, self.ground)
            changeTileApearance([block[0], block[1] - 1], self.global_assets, level_data, self.ground)
        
        self.player["box"].change(offset = (level_data["player_spawn"][0] * self.grid.tile_size[0] + self.grid_encloser.offset[0], level_data["player_spawn"][1] * self.grid.tile_size[1] + self.grid_encloser.offset[1]))
        self.player["sprite"].change(size = self.grid.tile_size)
        self.player["collision"].collision_blocks[0].change(size = (self.grid.tile_size[0] * 0.7, self.grid.tile_size[1] * 0.8), offset = (self.grid.tile_size[0] * 0.15, self.grid.tile_size[1] * 0.2))

        self.finish["box"].change(offset = (level_data["finish"][0] * self.grid.tile_size[0] + self.grid_encloser.offset[0], level_data["finish"][1] * self.grid.tile_size[1] + self.grid_encloser.offset[1]))
        self.finish["sprite"].change(size = self.grid.tile_size)
        self.finish["collision"].collision_blocks[0].change(size = (self.grid.tile_size[0] * 0.8, self.grid.tile_size[1] * 0.8), offset = (self.grid.tile_size[0] * 0.1, self.grid.tile_size[1] * 0.1))
    

    def coverSight(self):
        self.new_pos = [int(self.player["box"].offset[0]) // 3, int(self.player["box"].offset[1]) // 3]
        if self.new_pos != self.last_pos or not self.player["move"].on_ground:
            self.cover.change(active = True)
        else:
            self.cover.change(active = False)
        
        self.last_pos = list(self.new_pos)
        



        
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