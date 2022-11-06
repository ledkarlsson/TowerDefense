from PIL import Image

import gameGlobal
from mapglobals import blockSize
from towers import ArrowShooterTower, BulletShooterTower, PowerTower, TackTower


class Block(object):
    # when i define a "Block", this is what happens
    def __init__(self, x, y, blockNumber, gridx, gridy):
        self.x = x  # sets Block x to the given 'x'
        self.y = y  # sets Block y to the given 'y'
        self.canPlace = True
        self.blockNumber = blockNumber
        self.gridx = gridx
        self.gridy = gridy
        self.image = None
        self.axis = blockSize/2

    def hoveredOver(self, click, game):
        if click:
            if gameGlobal.towerGrid[self.gridx][self.gridy]:
                if gameGlobal.selectedTower == "<None>":
                    gameGlobal.towerGrid[self.gridx][self.gridy].clicked = True
                    global displayTower
                    displayTower = gameGlobal.towerGrid[self.gridx][self.gridy]
                    game.infoboard.displaySpecific()
            elif gameGlobal.selectedTower != "<None>" and self.canPlace and gameGlobal.money >= gameGlobal.towerCost[gameGlobal.selectedTower]:
                self.towerType = self.str_to_tower(
                    [gameGlobal.towerDictionary[gameGlobal.selectedTower]][0])
                gameGlobal.towerGrid[self.gridx][self.gridy] = self.towerType(
                    self.x, self.y, self.gridx, self.gridy)
                gameGlobal.money -= gameGlobal.towerCost[gameGlobal.selectedTower]

    def update(self):
        pass

    def paint(self, draw):
        self.image = Image.open(
            "images/blockImages/" + self.__class__.__name__+".png")
        self.offset = (int(self.x - self.axis), int(self.y - self.axis))
        draw.paste(self.image, self.offset)
        self.image = None

    @staticmethod
    def str_to_object(string):
        if string == "NormalBlock":
            return NormalBlock
        elif string == "PathBlock":
            return PathBlock
        elif string == "WaterBlock":
            return WaterBlock
        else:
            return None

    @staticmethod
    def str_to_tower(string):
        if string == "ArrowShooterTower":
            return ArrowShooterTower
        elif string == "BulletShooterTower":
            return BulletShooterTower
        elif string == "TackTower":
            return TackTower
        elif string == "PowerTower":
            return PowerTower
        else:
            return None


class NormalBlock(Block):
    def __init__(self, x, y, blockNumber, gridx, gridy):
        super(NormalBlock, self).__init__(x, y, blockNumber, gridx, gridy)


class PathBlock(Block):
    def __init__(self, x, y, blockNumber, gridx, gridy):
        super(PathBlock, self).__init__(x, y, blockNumber, gridx, gridy)
        self.canPlace = False


class WaterBlock(Block):
    def __init__(self, x, y, blockNumber, gridx, gridy):
        super(WaterBlock, self).__init__(x, y, blockNumber, gridx, gridy)
        self.canPlace = False
