import pygame
from pygame import Vector2

__all__ = ["Backbone", "Modifier", "Node"]

def positionFromStr(string, size, parentNode_size):
    sw, sh = Vector2(size)
    w, h = Vector2(parentNode_size)
    
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

    output = pos.get(string)
    
    if output:
        return [output, string]
    return [output, None]


# ----- Base of nodes ----- #


class Backbone:
    def __init__(self):
        self.children = []
    
    def event(self, event):
        for node in self.children:
            node.event(event)
    
    def update(self):
        for node in self.children:
            node.update()

    def draw(self):
        for node in self.children:
            node.draw()

class Modifier(Backbone):
    def __init__(self, parentNode):
        super().__init__()
        self.parentNode = parentNode
        self.parentNode.children.append(self)

        self.scene = self.parentNode.scene
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self):
        super().draw()

class Node(Modifier):
    def __init__(self, parentNode, size = Vector2(0, 0), offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode)

        self.size = Vector2(size)

        
        if (offset_str):
            self.offset, offset_str = positionFromStr(offset_str.lower(), self.size, self.parentNode.size)
        
        if offset_str is None:
            self.offset = Vector2(offset)

        self.position = self.parentNode.position + self.offset

        for otherNode in self.parentNode.children:
            if otherNode.position == self.position and otherNode is not self:
                print("Too many nodes at the same position, could not find a free spot")
                pygame.quit()
                exit()
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        self.position = self.parentNode.position + self.offset
        super().update()

    def draw(self):
        super().draw()
    
    def kill(self):
        self.parentNode.children.remove(self)

