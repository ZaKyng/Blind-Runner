import pygame
from pygame import Vector2

__all__ = ["Parent", "Modifier", "Node"]


def positionFromStr(string: str, size, parentNode_size, offset):
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

    output = pos.get(string, offset)
    
    return Vector2(output)


# ----- Base of nodes ----- #


class Parent:
    def __init__(self, parentNode):
        self.children = []
        self.collision = []
        self.game = parentNode.game
    
    def event(self, event):
        for node in self.children:
            node.event(event)
    
    def update(self):
        for node in self.children:
            node.update()

    def draw(self):
        for node in self.children:
            node.draw()
    
    def addChild(self, newChild):
        for i in range(len(self.children)):
            if self.children[i].zindex >= newChild.zindex:
                self.children.insert(i, newChild)
                return
        self.children.append(newChild)
    
    def addCollision(self, newCollision):
        self.collision.append(newCollision)
    
    def child(self, parentNode, zindex):
        self.zindex = zindex

        self.parentNode = parentNode
        self.parentNode.addChild(self)

        self.game = self.parentNode.game
    
    def kill(self):
        """Remove self from its parent children list."""
        if hasattr(self, "children"):
            for child in self.children[:]:
                child.kill()

            self.children.clear()
            self.collision.clear()

        if self in self.parentNode.children:
            self.parentNode.children.remove(self)



class Modifier(Parent):
    def __init__(self, parentNode, zindex = -10):
        super().child(parentNode, zindex)
        self.game = parentNode.game
    
    def event(self, event):
        pass
    
    def update(self):
        pass

    def draw(self):
        pass
    
    def kill(self) -> None:
        super().kill()
        

class Node(Parent):
    def __init__(self, parentNode, size = Vector2(0, 0), zindex = 0, offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode)
        super().child(parentNode, zindex)

        self.size = Vector2(size)

        if (offset_str):
            self.offset = positionFromStr(offset_str.lower(), self.size, self.parentNode.size, offset)
        else:
            self.offset = Vector2(offset)

        self.position = self.parentNode.position + self.offset

        for otherNode in self.parentNode.children:
            """if otherNode.position == self.position and otherNode is not self:
                print("Too many nodes at the same position, could not find a free spot")
                pygame.quit()
                exit()"""
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        self.position = self.parentNode.position + self.offset
        super().update()

    def draw(self):
        super().draw()
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def addCollision(self, newCollision):
        super().addCollision(newCollision)
    
    def kill(self):
        super().kill()

