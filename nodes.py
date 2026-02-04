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

class parentNode:
    def __init__(self, _screen, _screen_size, physics_layer = 0 ,position_str = None, position = [0, 0]):
        self.size = [0, 0]
        self.screen = _screen
        self.screen_size = _screen_size

        self.physics_layer = physics_layer

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

    def draw(self):
        self.rect.topleft = (self.parentNode.position[0] + self.offset[0], 
        self.parentNode.position[1] + self.offset[1])

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

    def draw(self):
        self.parentNode.position[0] = max(0, 
        min(self.parentNode.screen_size[0] - self.parentNode.size[0], 
        self.parentNode.position[0] + self.move[0]))

        self.parentNode.position[1] = max(0,
        min(self.parentNode.screen_size[1] - self.parentNode.size[1],
        self.parentNode.position[1] + self.move[1]))
    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move[0] += -10
            elif event.key == pygame.K_RIGHT:
                self.move[0] += 10
            elif event.key == pygame.K_UP:
                self.move[1] += -10
            elif event.key == pygame.K_DOWN:
                self.move[1] += 10
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move[0] -= -10
            elif event.key == pygame.K_RIGHT:
                self.move[0] -= 10
            elif event.key == pygame.K_UP:
                self.move[1] -= -10
            elif event.key == pygame.K_DOWN:
                self.move[1] -= 10