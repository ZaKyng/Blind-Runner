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

class ButtonMove:
    def __init__(self, screen, screen_size, text, command, font, padding = 0, position = None, pos_x = 0, pos_y = 0, fg = [255, 255, 255], bg = [0, 0, 0]):
        self.screen = screen
        self.screen_size = screen_size
        self.text = text
        self.color = fg
        self.background = bg
        self.font = font
        self.padding = padding
        self.command = command
        self.clicked = False
        self.message = self.font.render(self.text, True, self.color)
        self.surface = pygame.Surface((self.message.get_size()[0] + self.padding, self.message.get_size()[1] + self.padding))
        self.size = self.surface.get_size()
        
        if (position):
            position = position.lower()
            if (position in possible_positions):
                self.x, self.y  = positionFromStr(position, self.size, self.screen_size)
            else:
                self.x = pos_x
                self.y = pos_y
        else:
            self.x = pos_x
            self.y = pos_y
        self.rect = pygame.Rect((self.x, self.y), self.size)

    def colideCheck(self, other):
        return pygame.Rect.colliderect(self.rect, other.rect)

    def draw(self):
        if self.clicked:
            self.surface.fill(((self.background[0] - 50) % 256, (self.background[1] - 50) % 256, (self.background[2] - 50) % 256))
            self.x = min(self.screen_size[0] - self.size[0], max(0, self.x - (self.mouse_pos_last[0] - pygame.mouse.get_pos()[0])))
            self.y = min(self.screen_size[1] - self.size[1], max(0, self.y - (self.mouse_pos_last[1] - pygame.mouse.get_pos()[1])))
            self.mouse_pos_last = pygame.mouse.get_pos()
            self.rect = pygame.Rect((self.x, self.y), self.size)
        else:
            self.surface.fill(self.background)
        self.surface.blit(self.message, ((self.surface.get_width() - self.message.get_width()) // 2, (self.surface.get_height() - self.message.get_height()) // 2))
        self.screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.command(event)
                self.mouse_pos_last = event.pos
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False


class ButtonFix:
    def __init__(self, screen, screen_size, text, command, font, padding = 0, position = None, pos_x = 0, pos_y = 0, fg = [255, 255, 255], bg = [0, 0, 0]):
        self.screen = screen
        self.screen_size = screen_size
        self.text = text
        self.color = fg
        self.background = bg
        self.font = font
        self.padding = padding
        self.command = command
        self.clicked = False
        self.message = self.font.render(self.text, True, self.color)
        self.surface = pygame.Surface((self.message.get_size()[0] + self.padding, self.message.get_size()[1] + self.padding))
        self.size = self.surface.get_size()
        if (position):
            position = position.lower()
            if (position in possible_positions):
                self.x, self.y  = positionFromStr(position, self.size, self.screen_size)
            else:
                self.x = pos_x
                self.y = pos_y
        else:
            self.x = pos_x
            self.y = pos_y
        self.rect = pygame.Rect((self.x, self.y), self.size)

    def draw(self):
        if self.clicked:
            self.surface.fill(((self.background[0] - 50) % 256, (self.background[1] - 50) % 256, (self.background[2] - 50) % 256))
        else:
            self.surface.fill(self.background)
        self.surface.blit(self.message, ((self.surface.get_width() - self.message.get_width()) // 2, (self.surface.get_height() - self.message.get_height()) // 2))
        self.screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.command(event)
                # print("Clicked on button")
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

class Label:
    def __init__(self, screen, screen_size, text, font, padding = 0, position = None, pos_x = 0, pos_y = 0, fg = [255, 255, 255], bg = [0, 0, 0]):
        #self.rect = pygame.Rect()
        self.screen = screen
        self.screen_size = screen_size
        self.text = text
        self.color = fg
        self.background = bg
        self.font = font
        self.padding = padding
        self.x = pos_x
        self.y = pos_y
        self.message = self.font.render(self.text, True, self.color)
        self.surface = pygame.Surface((self.message.get_size()[0] + self.padding, self.message.get_size()[1] + self.padding))
        self.surface.fill(self.background)
        self.size = self.surface.get_size()
        if (position):
            position = position.lower()
            if (position in possible_positions):
                self.x, self.y  = positionFromStr(position, self.size, self.screen_size)
            else:
                self.x = pos_x
                self.y = pos_y
        else:
            self.x = pos_x
            self.y = pos_y
        self.rect = pygame.Rect((self.x, self.y), self.size)
    
    def draw(self):
        self.surface.blit(self.message, ((self.surface.get_width() - self.message.get_width()) // 2, (self.surface.get_height() - self.message.get_height()) // 2))
        self.screen.blit(self.surface, (self.x, self.y))