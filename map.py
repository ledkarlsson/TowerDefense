import tkinter

from PIL import Image, ImageTk

import gameGlobal
from blocks import NormalBlock, PathBlock, WaterBlock
from mapglobals import blockGrid, blockSize, gridSize, mapSize


class Map():
    def __init__(self):
        self.image = None
        self.loadMap("LeoMap")

    def loadMap(self, mapName):
        self.drawnMap = Image.new(
            "RGBA", (mapSize, mapSize), (255, 255, 255, 255))
        self.mapFile = open("texts/mapTexts/"+mapName+".txt", "r")
        self.gridValues = list(map(int, (self.mapFile.read()).split()))
        for y in range(gridSize):
            for x in range(gridSize):
                global blockGrid
                self.blockNumber = self.gridValues[gridSize*y + x]
                self.blockType = self.str_to_block(
                    gameGlobal.blockDictionary[self.blockNumber])
                blockGrid[x][y] = self.blockType(
                    x*blockSize+blockSize/2, y*blockSize+blockSize/2, self.blockNumber, x, y)  # creates a grid of Blocks
                blockGrid[x][y].paint(self.drawnMap)
        self.drawnMap.save("images/mapImages/"+mapName+".png")
        self.image = Image.open("images/mapImages/"+mapName+".png")
        self.image = ImageTk.PhotoImage(self.image)

    def saveMap(self):
        self.mapFile = open("firstMap.txt", "w")
        for y in range(gridSize):
            for x in range(gridSize):
                self.mapFile.write(blockGrid[x][y].blockType + " ")
        self.mapFile.close()

    def paint(self, canvas):
        canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)

    @staticmethod
    def str_to_block(string):
        if string == "NormalBlock":
            return NormalBlock
        elif string == "PathBlock":
            return PathBlock
        elif string == "WaterBlock":
            return WaterBlock
        else:
            return None
