import math
import pygame
from pygame import Vector2

def positionFromStr(string, size, screen_size):
    sw, sh = Vector2(size)
    w, h = Vector2(screen_size)
    
    max_x, max_y = w - sw, h - sh
    mid_x, mid_y = max_x / 2, max_y / 2

    pos = {
        "top-left":     Vector2(0, 0),
        "left":         Vector2(0, mid_y),
        "bottom-left":  Vector2(0, max_y),
        "top-right":    Vector2(max_x, 0),
        "right":        Vector2(max_x, mid_y),
        "bottom-right": Vector2(max_x, max_y),
        "top":          Vector2(mid_x, 0),
        "bottom":       Vector2(mid_x, max_y),
        "center":       Vector2(mid_x, mid_y)
    }
    
    return pos.get(string)


class node:
    def __init__(self, parentNode, size = [0, 0], offset_str = None, offset = [0, 0]):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.screen = self.parentNode.screen
        self.screen_size = self.parentNode.screen_size

        self.size = Vector2(size)

        self.offset = Vector2(offset)
        if (offset_str):
            self.offset = positionFromStr(offset_str.lower(), self.size, self.scene.screen_size)

        self.position = self.parentNode.position + self.offset

class scene:
    def __init__(self, screen, screen_size):
        self.children = [] # Seznam root nodů
        self.screen = screen
        self.screen_size = Vector2(screen_size)
        self.position = Vector2(0, 0)

    def draw(self):
        for node in self.rootNodes:
            node.draw()

    def event(self, event):
        for node in self.rootNodes:
            node.event(event)
    
    def update(self):
        for node in self.rootNodes:
            node.update()

class levelGrid:
    def __init__(self, scene, num_cells):
        self.scene = scene

        self.children = []

        self.physics_layer = 0
        
        num_cells += 1
        changer = -1
        while self.scene.screen_size[0] % num_cells != 0:
            num_cells += changer

            changer *= -1
            changer += 1
            if changer < 0:
                changer += -2
        
        #print(num_cells - 1)
                
        self.num_cells = num_cells
        self.cell_size = [self.scene.screen_size[0] // num_cells, 
                          self.scene.screen_size[0] // num_cells]
        self.position = -pygame.Vector2(self.cell_size) // 2

    def groundInit(self, color = [0, 0, 255], physics_layer = 0):
        level = parentNode(self.scene, physics_layer = physics_layer, position = self.position)

        self.children.append(level)

        for i in range((self.num_cells + 1) * 2):
            level.collisionBlock(self.cell_size, color = color, offset = [i // 2 * self.cell_size[0], self.scene.screen_size[1] * (i % 2)], can_leave_window = True)
        
        for i in range((self.scene.screen_size[1] // self.cell_size[0] + 1) * 2):
            level.collisionBlock(self.cell_size, color = color, offset = [self.scene.screen_size[0] * (i % 2), i // 2 * self.cell_size[0]], can_leave_window = True)
        
        return level

    def addGround(self, parentNode, coords, color = [0, 0, 255]):
        for oneCoord in coords:
            parentNode.collisionBlock(self.cell_size, color = color, offset = [(oneCoord[0] + 1) * self.cell_size[0], (oneCoord[1] + 1) * self.cell_size[0]], can_leave_window = True)
    
    def removeGround(self, parentNode, coords):
        for oneCoord in coords:
            parentNode.removeCollisionBlock([(oneCoord[0] + 1) * self.cell_size[0], (oneCoord[1] + 1) * self.cell_size[0]])

    def player(self, color = [140, 0, 0], position = [0, 0], physics_layer = 5, physics_check = 0):
        player = parentNode(self.scene, physics_layer = physics_layer, position = [position[0] * self.cell_size[0] - self.position[0], position[1] * self.cell_size[1] - self.position[1]])
        self.children.append(player)

        player.collisionBlock(self.cell_size, color = color)

        playerMove(player, physics_check, 
                    speed = self.cell_size[0] / 14,      
                    jump_strength = self.cell_size[1] / 6, 
                    gravity = self.cell_size[1] / 300)

        return player
    
    def gridCoordinates(self, relative_position = [0, 0]):
        new_coordinate = [(self.cell_size[0] * relative_position[0]) - (self.position[0]), (self.cell_size[1] * relative_position[1]) - (self.position[1])]
        return new_coordinate


# ---- Nodes ----- #

class parentNode:
    def __init__(self, _scene, physics_layer = 0, position_str = None, position = [0, 0]):
        self.size = [0, 0]
        self.scene = _scene

        self.physics_layer = physics_layer

        self.velocity = [0, 0]

        self.children = []
        self.hitBoxes = []

        self.position = list(position)
        
        if (position_str):
            self.position = positionFromStr(position_str.lower(), self.size, self.scene.screen_size)
        
        for otherNode in self.scene.rootNodes:
            change_x = 0
            change_y = 1
            while otherNode.position == self.position:
                self.position[0] += change_x
                self.position[1] += change_y
                if self.position[1] < 0:
                    self.position[1] = 0
                    change_x = -1
                    change_y = 0
                if self.position[0] < 0:
                    self.position[0] = 0
                    change_x = 0
                    change_y = 1
                if self.position[1] > self.scene.screen_size[1]:
                    self.position[1] = self.scene.screen_size[1]
                    change_x = 1
                    change_y = 0
                if self.position[0] > self.scene.screen_size[0]:
                    print("Too many nodes at the same position, could not find a free spot")
                    pygame.quit()
                    exit()
        
        self.scene.rootNodes.append(self)
    
    def collisionBlock(self, size, color = [0, 0, 0], position_str = None, offset = [0, 0], can_leave_window = False):
        newBlock = block(self, size, color, position_str = position_str, offset = offset)
        newHitBox = hitBox(self, size, position_str = position_str, offset = offset, can_leave_window = can_leave_window, show = True)
        return newBlock, newHitBox

    def removeCollisionBlock(self, offset):
        for child in self.children[:]:
            if hasattr(child, 'offset') and child.offset == offset:
                if hasattr(child, 'remove'):
                    child.remove()

    

    def event(self, event):
        for child in self.children:
            if hasattr(child, 'event'):
                child.event(event)    

    def update(self):
        for child in self.children:
            if hasattr(child, 'update'):
                child.update()

    def draw(self):
        for child in self.children:
            if hasattr(child, 'draw'):
                child.draw()



class label:
    def __init__(self, parentNode, text, font, 
                padding = 0, position_str = None, offset = (0, 0),
                fg = [255, 255, 255], bg = None, changable = False):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.text = text
        self.color = fg
        self.background = bg
        self.font = font

        self.changable = changable
        self.message = self.font.render(self.text, True, self.color)
        
        self.padding = padding
        # KLÍČOVÁ ZMĚNA: Přidání pygame.SRCALPHA pro podporu průhlednosti
        self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                       self.message.get_size()[1] + self.padding * 2), 
                                       pygame.SRCALPHA)

        self.size = self.surface.get_size()
        self.offset = offset
        if (position_str ):
            self.offset = positionFromStr(position_str.lower(), self.size, parentNode.size)

    def draw(self):
        # Pokud bg není definováno, surface vyčistíme úplnou průhledností
        if self.background:
            self.surface.fill(self.background)
        else:
            self.surface.fill((0, 0, 0, 0)) # Transparentní černá
        
        if self.changable:
            self.message = self.font.render(self.text, True, self.color)
            self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                       self.message.get_size()[1] + self.padding * 2), 
                                       pygame.SRCALPHA)
            self.size = self.surface.get_size()

        self.surface.blit(self.message, (
            (self.surface.get_width() - self.message.get_width()) // 2, 
            (self.surface.get_height() - self.message.get_height()) // 2))

        self.parentNode.scene.screen.blit(self.surface, (
            self.parentNode.position[0] + self.offset[0], 
            self.parentNode.position[1] + self.offset[1]))
    
    def remove(self):
        self.parentNode.children.remove(self)

class block:
    def __init__(self, parentNode, size, 
                color = [0, 255, 0], position_str = None, offset = (0, 0)):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.size = size
        self.color = color

        self.offset = offset
        if (position_str):
            self.offset = positionFromStr(position_str.lower(), self.size,parentNode.size)

    def draw(self):
        pygame.draw.rect(self.parentNode.scene.screen, self.color, 
        (self.parentNode.position[0] + self.offset[0], 
        self.parentNode.position[1] + self.offset[1], self.size[0], self.size[1]))

    def remove(self):
        self.parentNode.children.remove(self)

class hitBox:
    def __init__(self, parentNode, size, position_str = None, offset = (0, 0), can_leave_window = False, show = False):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.size = size

        self.show = show

        self.can_leave_window = can_leave_window

        self.offset = offset
        if (position_str):
            self.offset = positionFromStr(position_str.lower(), self.size, parentNode.size)
        
        self.rect = pygame.Rect((self.parentNode.position[0] + self.offset[0], 
        self.parentNode.position[1] + self.offset[1]), size)
        
        parentNode.hitBoxes.append(self)

        self.parentNode.update()

    def update(self):
        if not self.can_leave_window:
            if self.parentNode.position[0] < 0:
                self.parentNode.position[0] = 0
            elif self.parentNode.position[0] + self.size[0] > self.parentNode.scene.screen_size[0]:
                self.parentNode.position[0] = self.parentNode.scene.screen_size[0] - self.size[0]

            if self.parentNode.position[1] < 0:
                self.parentNode.position[1] = 0
                self.parentNode.velocity[1] = 0
            elif self.parentNode.position[1] + self.size[1] > self.parentNode.scene.screen_size[1]:
                self.parentNode.position[1] = self.parentNode.scene.screen_size[1] - self.size[1]
                self.parentNode.onGround = True
        
        self.rect.topleft = (self.parentNode.position[0] + self.offset[0], 
        self.parentNode.position[1] + self.offset[1])


    def draw(self):
        if self.show:
            pygame.draw.rect(self.parentNode.scene.screen, [0, 255, 0], self.rect, 2)
    
    def remove(self):
        self.parentNode.children.remove(self)
        self.parentNode.hitBoxes.remove(self)


# ----- Modifiers ----- #

# --- User Input --- #

class clickMouse:
    def __init__(self, parentNode):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.parentNode.position = pygame.mouse.get_pos()

class moveMouse:
    def __init__(self, parentNode):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.clicked = False
    
    def update(self):
        if self.clicked:
            self.parentNode.velocity[1] = 0
            self.parentNode.position[0] -= (self.mouse_pos_last[0] - pygame.mouse.get_pos()[0])
            self.parentNode.position[1] -= (self.mouse_pos_last[1] - pygame.mouse.get_pos()[1])
            self.mouse_pos_last = pygame.mouse.get_pos()
    
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for hitBox in self.parentNode.hitBoxes:
                if hitBox.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked = True
                    self.mouse_pos_last = pygame.mouse.get_pos()
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

class moveInput:
    def __init__(self, parentNode):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.move = [0, 0]
        self.speed = 5

    def draw(self):
        self.parentNode.position[0] = max(0, 
        min(self.parentNode.scene.screen_size[0], 
        self.parentNode.position[0] + self.move[0]))

        self.parentNode.position[1] = max(0,
        min(self.parentNode.scene.screen_size[1],
        self.parentNode.position[1] + self.move[1]))
    
    def event(self, event):
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            i = 1 if event.type == pygame.KEYDOWN else -1
            speed = self.speed * i
            if event.key == pygame.K_LEFT:
                self.move[0] += -speed
            elif event.key == pygame.K_RIGHT:
                self.move[0] += speed
            elif event.key == pygame.K_UP:
                self.move[1] += -speed
            elif event.key == pygame.K_DOWN:
                self.move[1] += speed


class playerMove:
    def __init__(self, parentNode, physics_check, speed = 5, jump_strength = 11.5 , gravity = 0.5):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.physics_check = physics_check

        self.left, self.right = False, False

        self.speed = speed
        self.jump_strength = jump_strength
        self.gravity = gravity

        self.parentNode.onGround = False

    def collision_x(self):
        for node in self.parentNode.scene.rootNodes:
            if node.physics_layer == self.physics_check:
                for ownHitBox in self.parentNode.hitBoxes:
                    for targetHB in node.hitBoxes:
                        targetHB.update()
                        if ownHitBox.rect.colliderect(targetHB.rect):
                            if self.parentNode.velocity[0] > 0: # Moving right
                                self.parentNode.position[0] = targetHB.rect.left - ownHitBox.size[0] - ownHitBox.offset[0]
                                self.parentNode.velocity[0] = 0
                            elif self.parentNode.velocity[0] < 0: # Moving left
                                self.parentNode.position[0] = targetHB.rect.right - ownHitBox.offset[0]
                                self.parentNode.velocity[0] = 0
                                self.parentNode.velocity[0] = 0
                        ownHitBox.update()
    
    def collision_y(self):
        for node in self.parentNode.scene.rootNodes:
            if node.physics_layer == self.physics_check:
                for ownHitBox in self.parentNode.hitBoxes:
                    for targetHB in node.hitBoxes:
                        targetHB.update()
                        if ownHitBox.rect.colliderect(targetHB.rect):
                            if self.parentNode.velocity[1] > 0: # Moving down
                                self.parentNode.position[1] = targetHB.rect.top - ownHitBox.size[1] - ownHitBox.offset[1]
                                self.parentNode.velocity[1] = 0
                                self.parentNode.onGround = True
                                self.parentNode.velocity
                            elif self.parentNode.velocity[1] < 0: # Moving up
                                self.parentNode.position[1] = targetHB.rect.bottom - ownHitBox.offset[1]
                                self.parentNode.velocity[1] = 0
                        ownHitBox.update()
    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
            elif event.key == pygame.K_RIGHT:
                self.right = True
            elif event.key == pygame.K_UP:
                if self.parentNode.onGround:
                    self.parentNode.velocity[1] += -self.jump_strength
                    self.parentNode.onGround = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left = False
            elif event.key == pygame.K_RIGHT:
                self.right = False
    
    def update(self):
        # 1. Horizontální pohyb
        if self.left and not self.right:
            self.parentNode.velocity[0] = -self.speed
        elif self.right and not self.left:
            self.parentNode.velocity[0] = self.speed
        else:
            self.parentNode.velocity[0] = 0

        # 2. Aplikace gravitace
        self.parentNode.velocity[1] += self.gravity

        # 3. Vertikální pohyb a kolize
        self.parentNode.position[1] += self.parentNode.velocity[1]
        
        # Reset onGround před kontrolou, ale s "bufferem"
        self.parentNode.onGround = False
        self.collision_y()

        # FIX: Dodatečná kontrola pro stabilitu (pohled 1 pixel pod sebe)
        # Pokud postava právě nepadá/neskáče, zkontrolujeme, zda je stále na zemi
        if not self.parentNode.onGround:
            for node in self.parentNode.scene.rootNodes:
                if node is self.parentNode or node.physics_layer != self.physics_check:
                    continue
                for ownHB in self.parentNode.hitBoxes:
                    # Vytvoříme testovací obdélník posunutý o 1px dolů
                    test_rect = ownHB.rect.move(0, 1)
                    for targetHB in node.hitBoxes:
                        if test_rect.colliderect(targetHB.rect):
                            self.parentNode.onGround = True
                            # Volitelně: vynulovat drobný nárůst gravitace
                            if self.parentNode.velocity[1] > 0:
                                self.parentNode.velocity[1] = 0
                            break

        # 4. Horizontální pohyb a kolize
        self.parentNode.position[0] += self.parentNode.velocity[0]
        self.collision_x()



# --- Interactive --- #

class enterCheck:
    def __init__(self, parentNode, physics_check, entry_func = None, colide_func = None):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.physics_check = physics_check

        self.entry_func = entry_func
        self.colide_func = colide_func

        self.colide_last_frame = False
    
    def update(self):
        for node in self.parentNode.scene.rootNodes:
            if node.physics_layer == self.physics_check:
                for ownHitBox in self.parentNode.hitBoxes:
                    for targetHB in node.hitBoxes:
                        if ownHitBox.rect.colliderect(targetHB.rect):
                            if (self.colide_func):
                                self.colide_func()
                            if not self.colide_last_frame:
                                self.colide_last_frame = True
                                if (self.entry_func):
                                    self.entry_func()
                            return ""
        self.colide_last_frame = False
    
    def none(self):
        return ""



# --- Looping --- #

axis_to_num = {
    "x": 0,
    "y": 1
}

class translateLinear:
    def __init__(self, parentNode, axis, end, velocity, start = None, mode = "linear"):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        if axis.lower() in ["x", "y"]:
            self.axis = axis.lower()
        else:
            self.axis = "x"
        
        self.velocity = velocity
        
        if start is not None:
            self.start = start
        else:
            self.start = self.parentNode.position[axis_to_num[self.axis]]

        self.end = end

        if self.start > self.end:
            start = self.start
            self.start = self.end
            self.end = start

        if mode.lower() == "linear":
            self.mode = self.linear
        else:
            self.mode = self.linear

        self.parentNode.velocity[axis_to_num[self.axis]] += self.velocity
        
    def linear(self):
        self.parentNode.position[axis_to_num[self.axis]] += self.parentNode.velocity[axis_to_num[self.axis]]
        if self.parentNode.position[axis_to_num[self.axis]] > self.end:
            self.parentNode.position[axis_to_num[self.axis]] = self.end
            self.velocity *= -1
            self.parentNode.velocity[axis_to_num[self.axis]] += 2 * self.velocity
        elif self.parentNode.position[axis_to_num[self.axis]] < self.start:
            self.parentNode.position[axis_to_num[self.axis]] = self.start
            self.velocity *= -1
            self.parentNode.velocity[axis_to_num[self.axis]] += 2 * self.velocity
    
    def update(self):
        self.mode()

class translateGlobal:
    def __init__(self, parentNode, start_pos, end_pos, velocity, mode = "linear"):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.start = list(start_pos)
        self.end = list(end_pos)
        
        self.parentNode.position = list(self.start)

        self.velocity = velocity

        self.diff = [self.end[0] - self.start[0], self.end[1] - self.start[1]]
        self.path_len = math.sqrt(self.diff[0] ** 2 + self.diff[1] ** 2)

        # Ošetření dělení nulou, pokud start == end
        if self.path_len > 0:
            self.step = [self.diff[0] / self.path_len, self.diff[1] / self.path_len]
        else:
            self.step = [0, 0]

        self.mode = self.linear

    def linear(self):
        # Pohyb
        self.parentNode.position[0] += self.step[0] * self.velocity
        self.parentNode.position[1] += self.step[1] * self.velocity

        hit_boundary = False
        
        for i in [0, 1]:
            # Nyní jsou self.start a self.end fixní hodnoty
            low, high = min(self.start[i], self.end[i]), max(self.start[i], self.end[i])
            
            if self.parentNode.position[i] > high:
                self.parentNode.position[i] = high
                hit_boundary = True
            elif self.parentNode.position[i] < low:
                self.parentNode.position[i] = low
                hit_boundary = True
                
        if hit_boundary:
            self.velocity *= -1
    
    def update(self):
        self.mode()

 