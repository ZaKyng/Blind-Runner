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

# ---- Nodes ----- #
class scene:
    def __init__(self):
        self.rootNodes = []

    def draw(self):
        for node in self.rootNodes:
            node.draw()

    def event(self, event):
        for node in self.rootNodes:
            node.event(event)
    
    def update(self):
        for node in self.rootNodes:
            node.update()

class parentNode:
    def __init__(self, scene, _screen, _screen_size, physics_layer = 0, position_str = None, position = [0, 0]):
        self.size = [0, 0]
        self.scene = scene
        self.scene.rootNodes.append(self)
        self.screen = _screen
        self.screen_size = _screen_size

        self.physics_layer = physics_layer
        self.onGround = False

        self.velocity = [0, 0]

        self.children = []
        self.hitBoxes = []

        self.position = position
        if (position_str):
            position_str = position_str.lower()
            if (position_str in possible_positions):
                self.position = positionFromStr(position_str, self.size, 
                                                self.screen_size)
        
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
                padding = 0, position=None, offset = (0, 0),
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
        if (position and position in possible_positions):
            position = position.lower()
            self.offset = positionFromStr(position, self.size, 
                                        parentNode.size)

    def draw(self):
        self.surface.fill(self.background)

        self.surface.blit(self.message, (
        (self.surface.get_width() - self.message.get_width()) // 2, 
        (self.surface.get_height() - self.message.get_height()) // 2))

        self.parentNode.screen.blit(self.surface, (
        self.parentNode.x + self.offset_x, self.parentNode.y + self.offset_y))

class block:
    def __init__(self, parentNode, size, 
                color = [0, 255, 0], position=None, offset = (0, 0)):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.size = size
        self.color = color

        self.offset = offset
        if (position and position in possible_positions):
            position = position.lower()
            self.offset = positionFromStr(position, self.size,
                                        parentNode.size)

    def draw(self):
        pygame.draw.rect(self.parentNode.screen, self.color, 
        (self.parentNode.position[0] + self.offset[0], 
        self.parentNode.position[1] + self.offset[1], self.size[0], self.size[1]))

class hitBox:
    def __init__(self, parentNode, size, position=None, offset = (0, 0)):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.size = size

        self.offset = offset
        if (position):
            position = position.lower()
            if (position in possible_positions):
                self.offset = positionFromStr(position, size, 
                                            parentNode.size)
        
        self.rect = pygame.Rect((self.parentNode.position[0] + self.offset[0], 
        self.parentNode.position[1] + self.offset[1]), size)
        
        parentNode.hitBoxes.append(self)

    def update(self):
        self.rect.topleft = (self.parentNode.position[0] + self.offset[0], 
        self.parentNode.position[1] + self.offset[1])
    
    """def event(self, event):
        for node in self.parentNode.scene.rootNodes:
            if node.physics_layer != self.parentNode.physics_layer:
                for hitBox in node.hitBoxes:
                    if self.rect.colliderect(hitBox.rect):
                        print([hitBox.parentNode.physics_layer, hitBox])
        return None"""
    
    def draw(self):
        pygame.draw.rect(self.parentNode.screen, [0, 255, 0], self.rect, 2)


# ----- Modifiers ----- #

class clickMouse:
    def __init__(self, parentNode):
        self.parentNode = parentNode

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.parentNode.position = pygame.mouse.get_pos()
            print(self.parentNode.children)

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
        min(self.parentNode.screen_size[0] - self.parentNode.size[0], 
        self.parentNode.position[0] + self.move[0]))

        self.parentNode.position[1] = max(0,
        min(self.parentNode.screen_size[1] - self.parentNode.size[1],
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




class collideWith:
    def __init__(self, parentNode, targetLayer):
        self.parentNode = parentNode
        self.parentNode.children.append(self)
        self.targetLayer = targetLayer

    def update(self):
        for node in self.parentNode.scene.rootNodes:
            if node.physics_layer != self.targetLayer:
                continue
            for ownHitBox in self.parentNode.hitBoxes:
                for targetHB in node.hitBoxes:

                    if ownHitBox.rect.colliderect(targetHB.rect):
                        offset_x = min(ownHitBox.rect.right - targetHB.rect.left,
                                       targetHB.rect.right - ownHitBox.rect.left)
                        
                        if self.parentNode.velocity[0] > 0:
                            self.parentNode.position[0] -= offset_x
                        elif self.parentNode.velocity[0] < 0:
                            self.parentNode.position[0] += offset_x
                        ownHitBox.update()

                    if ownHitBox.rect.colliderect(targetHB.rect):
                        offset_y = min(ownHitBox.rect.bottom - targetHB.rect.top,
                                       targetHB.rect.bottom - ownHitBox.rect.top)
                        
                        if self.parentNode.velocity[1] > 0:
                            self.parentNode.position[1] -= offset_y
                            self.parentNode.onGround = True
                        elif self.parentNode.velocity[1] < 0:
                            self.parentNode.position[1] += offset_y
                        ownHitBox.update()
                ownHitBox.update()

class moveGravity:
    def __init__(self, parentNode, gravity = 0.5, speed = 8, jump_strength = 12):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.gravity = gravity
        self.speed = speed
        self.jump_strength = jump_strength

        self.left_key, self.right_key = False, False

    def update(self):
        if self.left_key and not self.right_key:
            self.parentNode.velocity[0] = -self.speed
        elif self.right_key and not self.left_key:
            self.parentNode.velocity[0] = self.speed
        else:
            self.parentNode.velocity[0] = 0
        
        if not self.parentNode.onGround:
            self.parentNode.velocity[1] += self.gravity
        else:
            self.parentNode.velocity[1] = 0

    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left_key = True
            elif event.key == pygame.K_RIGHT:
                self.right_key = True
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP and self.parentNode.onGround:
                self.parentNode.velocity[1] = -self.jump_strength

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left_key = False
            elif event.key == pygame.K_RIGHT:
                self.right_key = False












"""
class colideWith:
    def __init__(self, parentNode, targetLayer):
        self.parentNode = parentNode
        self.parentNode.children.append(self)
        self.targetLayer = targetLayer

    def update(self):
        # We assume movement is stored in self.parentNode.velocity or similar
        # Move X
        self.parentNode.position[0] += self.parentNode.velocity[0]
        self.check_collisions(axis='x')

        # Move Y
        self.parentNode.position[1] += self.parentNode.velocity[1]
        self.check_collisions(axis='y')

    def check_collisions(self, axis):
        for node in self.parentNode.scene.rootNodes:
            if node.physics_layer == self.targetLayer:
                for myHB in self.parentNode.hitBoxes:
                    myHB.update() # Sync rect with parent position
                    for targetHB in node.hitBoxes:
                        targetHB.update()
                        if myHB.rect.colliderect(targetHB.rect):
                            if axis == 'x':
                                if self.parentNode.velocity[0] > 0: # Moving right
                                    self.parentNode.position[0] = targetHB.rect.left - myHB.size[0] - myHB.offset[0]
                                if self.parentNode.velocity[0] < 0: # Moving left
                                    self.parentNode.position[0] = targetHB.rect.right - myHB.offset[0]
                            
                            if axis == 'y':
                                if self.parentNode.velocity[1] > 0: # Falling/Down
                                    self.parentNode.position[1] = targetHB.rect.top - myHB.size[1] - myHB.offset[1]
                                    self.parentNode.velocity[1] = 0
                                if self.parentNode.velocity[1] < 0: # Jumping/Up
                                    self.parentNode.position[1] = targetHB.rect.bottom - myHB.offset[1]
                                    self.parentNode.velocity[1] = 0

                    
                    


class moveGravity:
    def __init__(self, parentNode, gravity = 0.5, speed = 8):
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.gravity = gravity
        self.speed = speed

        self.left_key, self.right_key = False, False

    def update(self):
        if self.left_key and not self.right_key:
            self.parentNode.velocity[0] = -self.speed
        elif self.right_key and not self.left_key:
            self.parentNode.velocity[0] = self.speed
        else:
            self.parentNode.velocity[0] = 0
        
        if not self.parentNode.onGround:
            self.parentNode.velocity[1] += self.gravity
        else:
            self.parentNode.velocity[1] = 0

    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left_key = True
            elif event.key == pygame.K_RIGHT:
                self.right_key = True
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP and self.parentNode.onGround:
                self.parentNode.velocity[1] = -12

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left_key = False
            elif event.key == pygame.K_RIGHT:
                self.right_key = False
"""