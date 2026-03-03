import pygame
from pygame import Vector2



# ----- Resources ----- #

## ----- Visual ----- ##

class LoadImage:
    def __init__(self, path):
        self.path = path
        self.rawImage = pygame.image.load(path)

        self.image = pygame.Surface(self.rawImage.get_size(), pygame.SRCALPHA)
        self.image.blit(self.rawImage, Vector2(0, 0))

        self.rawImage = None

class LoadImageGrid:
    def __init__(self, path, oneFrameSize):
        self.path = path
        self.rawImage = pygame.image.load(path)

        self.grid = []
        self.tileCount = [self.rawImage.get_size()[0] // max(oneFrameSize[0], 1), self.rawImage.get_size()[1] // max(oneFrameSize[1], 1)]
        for x in range(int(self.tileCount[0])):
            self.grid.append([])
            for y in range(int(self.tileCount[1])):
                oneTile = pygame.Surface(oneFrameSize, pygame.SRCALPHA)
                oneTile.blit(self.rawImage, Vector2(0, 0), 
                    (oneFrameSize[0] * x, oneFrameSize[1] * y, oneFrameSize[0], oneFrameSize[1]))
                self.grid[x].append(oneTile)
        
        self.rawImage = None

class Animation:
    def __init__(self, framesArr, start, end):
        if start > end:
            temp = end
            end = start
            start = temp

        self.frames = []
        for i in range(end - start + 1):
            frame = i + start
            x = frame % max(len(framesArr), 1)
            y = frame // max(len(framesArr[0]), 1)
            self.frames.append(framesArr[int(x)][int(y)])

