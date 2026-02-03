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


class parentNode:
    def __init__(self, _screen, _screen_size, position = None, x = 0, y = 0,):
        self.size = [0, 0]
        self.screen = _screen
        self.screen_size = _screen_size

        self.childern = []

        if (position):
            position = position.lower()
            if (position in possible_positions):
                self.x, self.y  = positionFromStr(position, self.size, self.screen_size)
            else:
                self.x = x
                self.y = y
        else:
            self.x = x
            self.y = y
        
        self.rect = pygame.Rect((self.x, self.y), self.size)
    
    def draw(self):
        for child in self.childern:
            if hasattr(child, 'draw'):
                child.draw()

    def event(self, event):
        for child in self.childern:
            if hasattr(child, 'event'):
                child.event(event)    

class hitBox:
    def __init__(self, parentNode, width, height, position=None, offset_x = 0, offset_y = 0):
        self.parentNode = parentNode
        self.parentNode.childern.append(self)

        self.size = [width, height]
        self.offset_x = offset_x
        self.offset_y = offset_y
        if (position and position in possible_positions):
            position = position.lower()
            self.offset_x, self.offset_y = positionFromStr(position, self.size, parentNode.size)

        self.parentNode.rect = pygame.Rect((self.parentNode.x + self.offset_x, self.parentNode.y + self.offset_y), self.size)

    def draw(self):
        self.parentNode.rect = pygame.Rect((self.parentNode.x + self.offset_x, self.parentNode.y + self.offset_y), self.size)
        if self.size[0] == 0 or self.size[1] == 0:
            self.surface = pygame.Surface(self.size)
            self.surface.fill((255, 0, 0))
            self.parentNode.screen.blit(self.surface, (self.parentNode.x + self.offset_x, self.parentNode.y + self.offset_y))

class label:
    def __init__(self, parentNode, text, font, padding = 0, position=None, offset_x = 0, offset_y = 0, fg = [255, 255, 255], bg = [0, 0, 0]):
        self.parentNode = parentNode
        self.parentNode.childern.append(self)

        self.text = text
        self.color = fg
        self.background = bg
        self.font = font
        self.message = self.font.render(self.text, True, self.color)
        self.surface = pygame.Surface((self.message.get_size()[0] + padding * 2, self.message.get_size()[1] + padding * 2))

        self.size = self.surface.get_size()

        self.offset_x = offset_x
        self.offset_y = offset_y
        if (position and position in possible_positions):
            position = position.lower()
            self.offset_x, self.offset_y = positionFromStr(position, self.size, parentNode.size)

    def draw(self):
        self.surface.fill(self.background)
        self.surface.blit(self.message, ((self.surface.get_width() - self.message.get_width()) // 2, (self.surface.get_height() - self.message.get_height()) // 2))
        self.parentNode.screen.blit(self.surface, (self.parentNode.x + self.offset_x, self.parentNode.y + self.offset_y))


class clickMouse:
    def __init__(self, parentNode):
        self.parentNode = parentNode

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.parentNode.x, self.parentNode.y = pygame.mouse.get_pos()
            print(self.parentNode.childern)

class moveMouse:
    def __init__(self, parentNode):
        self.parentNode = parentNode
        self.parentNode.childern.append(self)

        self.clicked = False
    
    def draw(self):
        if self.clicked:
            self.parentNode.x -= (self.mouse_pos_last[0] - pygame.mouse.get_pos()[0])
            self.parentNode.y -= (self.mouse_pos_last[1] - pygame.mouse.get_pos()[1])
            self.mouse_pos_last = pygame.mouse.get_pos()
    
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.parentNode.rect.collidepoint(event.pos):
                self.mouse_pos_last = event.pos
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

class moveInput:
    def __init__(self, parentNode):
        self.parentNode = parentNode
        self.parentNode.childern.append(self)

        self.move_x = 0
        self.move_y = 0

    def draw(self):
        self.parentNode.x = max(0, min(self.parentNode.screen_size[0] - self.parentNode.size[0], self.parentNode.x + self.move_x))
        self.parentNode.y = max(0, min(self.parentNode.screen_size[1] - self.parentNode.size[1], self.parentNode.y + self.move_y))
    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_x += -10
            elif event.key == pygame.K_RIGHT:
                self.move_x += 10
            elif event.key == pygame.K_UP:
                self.move_y += -10
            elif event.key == pygame.K_DOWN:
                self.move_y += 10
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_x -= -10
            elif event.key == pygame.K_RIGHT:
                self.move_x -= 10
            elif event.key == pygame.K_UP:
                self.move_y -= -10
            elif event.key == pygame.K_DOWN:
                self.move_y -= 10