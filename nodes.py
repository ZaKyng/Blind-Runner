import pygame

def positionFromStr(string, size, screen_size):
    width, height = screen_size

    if (string == "left"):
        return [0, height // 2 - (size[1] // 2)]
    elif (string == "right"):
        return [width - size[0], height // 2 - (size[1] // 2)]
    elif (string == "top"):
        return [width // 2 - (size[0] // 2), 0]
    elif (string == "bottom"):
        return [width // 2 - (size[0] // 2), height - size[1]]
    elif (string == "center"):
        return [width // 2 - (size[0] // 2), height // 2 - (size[1] // 2)]

possible_positions = [
    "left", "right", "top", "bottom", "center"
]




class scene:
    def __init__(self, screen, screen_size):
        self.rootNodes = []
        self.screen = screen
        self.screen_size = screen_size

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
    def __init__(self, scene, num_cells_width):
        self.scene = scene

        self.children = []

        self.physics_layer = 0
        
        self.num_cells_width = num_cells_width
        self.cell_size = [self.scene.screen_size[0] // num_cells_width, 
                          self.scene.screen_size[0] // num_cells_width]
        self.position = [-self.cell_size[0] // 2, -self.cell_size[1] // 2]

        print(self.position)

    def ground(self, color = [0, 0, 255], physics_layer = 0):
        self.level = parentNode(self.scene, physics_layer = physics_layer, position = self.position)

        self.children.append(self.level)

        for i in range((self.num_cells_width + 1) * 2):
            self.level.collisionBlock(self.cell_size, color = color, offset = [i // 2 * self.cell_size[0], self.scene.screen_size[1] * (i % 2)], can_leave_window = True)
        
        for i in range((self.scene.screen_size[1] // self.cell_size[0] + 1) * 2):
            self.level.collisionBlock(self.cell_size, color = color, offset = [self.scene.screen_size[0] * (i % 2), i // 2 * self.cell_size[0]], can_leave_window = True)

        """block(self.level, self.cell_size, color = [0, 0, 255])
        hitBox(self.level, self.cell_size, can_leave_window = True)
        block(self.level, self.cell_size, color = [0, 0, 255], offset=(self.cell_size[0], self.cell_size[1]))
        hitBox(self.level, self.cell_size, offset=(self.cell_size[0], self.cell_size[1]), can_leave_window = True)"""

        
    
    def draw(self):
        for child in self.children:
            if hasattr(child, 'draw'):
                child.draw()

    def event(self, event):
        for child in self.children:
            if hasattr(child, 'event'):
                child.event(event)    

    def update(self):
        for child in self.children:
            if hasattr(child, 'update'):
                child.update()

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
            position_str = position_str.lower()
            if (position_str in possible_positions):
                self.position = positionFromStr(position_str, self.size, 
                                                self.scene.screen_size)
        
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
        block(self, size, color, position_str = position_str, offset = offset)
        hitBox(self, size, position_str = position_str, offset = offset, can_leave_window = can_leave_window)

        
    def draw(self):
        for child in self.children:
            if hasattr(child, 'draw'):
                child.draw()

    def event(self, event):
        for child in self.children:
            if hasattr(child, 'event'):
                child.event(event)    

    def update(self):
        for child in self.children:
            if hasattr(child, 'update'):
                child.update()

class label:
    def __init__(self, parentNode, text, font, 
                padding = 0, position_str = None, offset = (0, 0),
                fg = [255, 255, 255], bg = [0, 0, 0]):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.text = text
        self.color = fg
        self.background = bg
        self.font = font
        self.message = self.font.render(self.text, True, self.color)
        self.surface = pygame.Surface((self.message.get_size()[0] + padding * 2, 
                                       self.message.get_size()[1] + padding * 2))

        self.size = self.surface.get_size()

        self.offset = offset
        if (position_str and position_str in possible_positions):
            position_str = position_str.lower()
            self.offset = positionFromStr(position_str, self.size,
                                        parentNode.size)

    def draw(self):
        self.surface.fill(self.background)

        self.surface.blit(self.message, (
        (self.surface.get_width() - self.message.get_width()) // 2, 
        (self.surface.get_height() - self.message.get_height()) // 2))

        self.parentNode.scene.screen.blit(self.surface, (
        self.parentNode.position[0] + self.offset[0], self.parentNode.position[1] + self.offset[1]))

class block:
    def __init__(self, parentNode, size, 
                color = [0, 255, 0], position_str = None, offset = (0, 0)):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.size = size
        self.color = color

        self.offset = offset
        if (position_str and position_str in possible_positions):
            position_str = position_str.lower()
            self.offset = positionFromStr(position_str, self.size,
                                        parentNode.size)

    def draw(self):
        pygame.draw.rect(self.parentNode.scene.screen, self.color, 
        (self.parentNode.position[0] + self.offset[0], 
        self.parentNode.position[1] + self.offset[1], self.size[0], self.size[1]))

class hitBox:
    def __init__(self, parentNode, size, position_str = None, offset = (0, 0), can_leave_window = False):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.size = size

        self.can_leave_window = can_leave_window

        self.offset = offset
        if (position_str and position_str in possible_positions):
            position_str = position_str.lower()
            self.offset = positionFromStr(position_str, self.size,
                                        parentNode.size)
        
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

        
    
    
    
    #def draw(self):
    #    pygame.draw.rect(self.parentNode.scene.screen, [0, 255, 0], self.rect, 2)


# ----- Modifiers ----- #

class clickMouse:
    def __init__(self, parentNode):
        self.parentNode = parentNode

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.parentNode.position = pygame.mouse.get_pos()

class moveMouse:
    def __init__(self, parentNode):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.clicked = False
    
    def draw(self):
        if self.clicked:
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
        if self.parentNode.velocity[1] > 0:
            self.parentNode.onGround = False

        if self.left and not self.right:
            self.parentNode.velocity[0] = -self.speed
        elif self.right and not self.left:
            self.parentNode.velocity[0] = self.speed
        else:
            self.parentNode.velocity[0] = 0


        self.parentNode.velocity[1] += self.gravity

        # Move X
        self.parentNode.position[0] += self.parentNode.velocity[0]
        self.collision_x()

        # Move Y
        self.parentNode.position[1] += self.parentNode.velocity[1]
        self.collision_y()
    