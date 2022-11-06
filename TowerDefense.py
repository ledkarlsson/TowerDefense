import math
import random
import tkinter

from PIL import Image, ImageTk

import gameGlobal
from blocks import NormalBlock, PathBlock, WaterBlock
from map import Map
from mapglobals import blockGrid, blockSize, gridSize, mapSize
from mouse import Mouse
from towers import TargetingTower

thisstring = "Hej"
monsterDictionary = [
    "Monster1",
    "Monster2",
    "AlexMonster",
    "BenMonster",
    "LeoMonster",
    "MonsterBig"]

pathList = []
spawnx = 0
spawny = 0
health = 100
displayTower = None


class Game():  # the main class that we call "Game"
    def __init__(self):  # setting up the window for the game here
        self.root = tkinter.Tk()  # saying this window will use tkinter
        self.root.title("Tower Defense Ultra Mode")
        self.root.protocol("WM_DELETE_WINDOW", self.end)

        self.frame = tkinter.Frame(master=self.root)
        self.frame.grid(row=0, column=0)

        # actually creates a window and puts our frame on it
        self.canvas = tkinter.Canvas(
            master=self.frame,
            width=mapSize,
            height=mapSize,
            bg="white",
            highlightthickness=0)
        # makes the window called "canvas" complete
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=1)

        self.displayboard = Displayboard(self)

        self.infoboard = Infoboard(self)

        self.towerbox = Towerbox(self)

        self.mouse = Mouse(self)

        self.gameMap = Map()

        self.wavegenerator = Wavegenerator(self)

        self.run()  # calls the function 'def run(self):'

        self.root.mainloop()  # starts running the tkinter graphics loop

    def run(self):
        self.update()  # calls the function 'def update(self):'
        self.paint()  # calls the function 'def paint(self):'

        # does a run of the function every 50/1000 = 1/20 of a second
        self.root.after(50, self.run)

    def end(self):
        self.root.destroy()  # closes the game window and ends the program

    def update(self):
        self.mouse.update()
        self.wavegenerator.update()
        self.displayboard.update()
        for i in range(len(gameGlobal.projectiles)):
            try:
                gameGlobal.projectiles[i].update()
            except:
                pass
        for y in range(gridSize):
            for x in range(gridSize):
                # updates each block one by one by going to its 'def update():' command
                blockGrid[x][y].update()
        for i in range(len(gameGlobal.monsters)):
            try:
                gameGlobal.monsters[i].update()
            except:
                pass
        gameGlobal.monstersByHealth = sorted(
            gameGlobal.monsters, key=lambda x: x.health, reverse=True)
        gameGlobal.monstersByDistance = sorted(
            gameGlobal.monsters, key=lambda x: x.distanceTravelled, reverse=True)
        gameGlobal.monstersByHealthReversed = sorted(
            gameGlobal.monsters, key=lambda x: x.health, reverse=False)
        gameGlobal.monstersByDistanceReversed = sorted(
            gameGlobal.monsters, key=lambda x: x.distanceTravelled, reverse=False)
        gameGlobal.monstersListList = [gameGlobal.monstersByHealth, gameGlobal.monstersByHealthReversed,
                                       gameGlobal.monstersByDistance, gameGlobal.monstersByDistanceReversed]
        for y in range(gridSize):
            for x in range(gridSize):
                if gameGlobal.towerGrid[x][y]:
                    # updates each tower one by one by going to its 'def update():' command
                    gameGlobal.towerGrid[x][y].update()

    def paint(self):
        self.canvas.delete(tkinter.ALL)  # clear the screen
        self.gameMap.paint(self.canvas)
        # draw the mouse dot by going to its 'def paint(canvas):' command
        self.mouse.paint(self.canvas)
        for y in range(gridSize):
            for x in range(gridSize):
                if gameGlobal.towerGrid[x][y]:
                    gameGlobal.towerGrid[x][y].paint(self.canvas)
        for i in range(len(gameGlobal.monstersByDistanceReversed)):
            gameGlobal.monstersByDistanceReversed[i].paint(self.canvas)
        for i in range(len(gameGlobal.projectiles)):
            gameGlobal.projectiles[i].paint(self.canvas)
        if displayTower:
            displayTower.paintSelect(self.canvas)
        self.displayboard.paint()


class Wavegenerator():
    def __init__(self, game):
        self.game = game
        self.done = False
        self.currentWave = []
        self.currentMonster = 0
        self.direction = None
        self.gridx = 0
        self.gridy = 0
        self.findSpawn()
        self.decideMove()
        self.ticks = 1
        self.maxTicks = 2
        self.waveFile = open("texts/waveTexts/WaveGenerator2.txt", "r")

    def getWave(self):
        self.game.displayboard.nextWaveButton.canPress = False
        self.currentMonster = 1
        self.waveLine = self.waveFile.readline()
        if len(self.waveLine) == 0:
            self.done = True
        else:
            self.currentWave = self.waveLine.split()
            self.currentWave = list(map(int, self.currentWave))
            self.maxTicks = self.currentWave[0]

    def findSpawn(self):
        global spawnx
        global spawny
        for x in range(gridSize):
            if isinstance(blockGrid[x][0], PathBlock):
                self.gridx = x
                spawnx = x*blockSize + blockSize/2
                spawny = 0
                return
        for y in range(gridSize):
            if isinstance(blockGrid[0][y], PathBlock):
                self.gridy = y
                spawnx = 0
                spawny = y*blockSize + blockSize/2
                return

    def move(self):
        global pathList
        pathList.append(self.direction)
        if self.direction == 1:
            self.gridx += 1
        if self.direction == 2:
            self.gridx -= 1
        if self.direction == 3:
            self.gridy += 1
        if self.direction == 4:
            self.gridy -= 1
        self.decideMove()

    def decideMove(self):
        if self.direction != 2 and self.gridx < gridSize-1 and self.gridy >= 0 and self.gridy <= gridSize-1:
            if isinstance(blockGrid[self.gridx+1][self.gridy], PathBlock):
                self.direction = 1
                self.move()
                return

        if self.direction != 1 and self.gridx > 0 and self.gridy >= 0 and self.gridy <= gridSize-1:
            if isinstance(blockGrid[self.gridx-1][self.gridy], PathBlock):
                self.direction = 2
                self.move()
                return

        if self.direction != 4 and self.gridy < gridSize-1 and self.gridx >= 0 and self.gridx <= gridSize-1:
            if isinstance(blockGrid[self.gridx][self.gridy+1], PathBlock):
                self.direction = 3
                self.move()
                return

        if self.direction != 3 and self.gridy > 0 and self.gridx >= 0 and self.gridx <= gridSize-1:
            if isinstance(blockGrid[self.gridx][self.gridy-1], PathBlock):
                self.direction = 4
                self.move()
                return

        global pathList
        pathList.append(5)

    def spawnMonster(self):
        self.monsterType = globals(
        )[monsterDictionary[self.currentWave[self.currentMonster]]]
        gameGlobal.monsters.append(self.monsterType(0))
        self.currentMonster = self.currentMonster + 1

    def update(self):
        if not self.done:
            if self.currentMonster == len(self.currentWave):
                self.game.displayboard.nextWaveButton.canPress = True
            else:
                self.ticks = self.ticks+1
                if self.ticks == self.maxTicks:
                    self.ticks = 0
                    self.spawnMonster()


class NextWaveButton:
    def __init__(self, game):
        self.game = game
        self.x = 450
        self.y = 25
        self.xTwo = 550
        self.yTwo = 50
        self.canPress = True

    def checkPress(self, click, x, y):
        if x >= self.x and y >= self.y and x <= self.xTwo and y <= self.yTwo:
            if self.canPress and click and len(gameGlobal.monsters) == 0:
                self.game.wavegenerator.getWave()

    def paint(self, canvas):
        if self.canPress and len(gameGlobal.monsters) == 0:
            self.color = "blue"
        else:
            self.color = "red"
        # draws a rectangle where the pointer is
        canvas.create_rectangle(self.x, self.y, self.xTwo,
                                self.yTwo, fill=self.color, outline=self.color)
        canvas.create_text(500, 37, text="Next Wave")


class MyButton(object):
    def __init__(self, x, y, xTwo, yTwo):
        self.x = x
        self.y = y
        self.xTwo = xTwo
        self.yTwo = yTwo

    def checkPress(self, click, x, y):
        if x >= self.x and y >= self.y and x <= self.xTwo and y <= self.yTwo:
            self.pressed()
            return True
        return False

    def pressed(self):
        pass

    def paint(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.xTwo,
                                self.yTwo, fill="red", outline="black")


class TargetButton(MyButton):
    def __init__(self, x, y, xTwo, yTwo, myType):
        super(TargetButton, self).__init__(x, y, xTwo, yTwo)
        self.type = myType

    def pressed(self):
        global displayTower
        displayTower.targetList = self.type


class StickyButton(MyButton):
    def __init__(self, x, y, xTwo, yTwo):
        super(StickyButton, self).__init__(x, y, xTwo, yTwo)

    def pressed(self):
        global displayTower
        if not displayTower.stickyTarget:
            displayTower.stickyTarget = True
        else:
            displayTower.stickyTarget = False


class SellButton(MyButton):
    def __init__(self, x, y, xTwo, yTwo):
        super(SellButton, self).__init__(x, y, xTwo, yTwo)

    def pressed(self):
        global displayTower
        displayTower.sold()
        displayTower = None


class UpgradeButton(MyButton):
    def __init__(self, x, y, xTwo, yTwo):
        super(UpgradeButton, self).__init__(x, y, xTwo, yTwo)

    def pressed(self):
        global displayTower
        if gameGlobal.money >= displayTower.upgradeCost:
            gameGlobal.money -= displayTower.upgradeCost
            displayTower.upgrade()


class Infoboard:
    def __init__(self, game):
        self.canvas = tkinter.Canvas(
            master=game.frame,
            width=162,
            height=174,
            bg="gray",
            highlightthickness=0)
        self.canvas.grid(row=0, column=1)
        self.image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        self.currentButtons = []

    def buttonsCheck(self, click, x, y):
        if click:
            for i in range(len(self.currentButtons)):
                if self.currentButtons[i].checkPress(click, x, y):
                    self.displaySpecific()
                    return

    def displaySpecific(self):
        self.canvas.delete(tkinter.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        self.currentButtons = []
        if displayTower is None:
            return

        self.towerImage = ImageTk.PhotoImage(Image.open(
            "images/towerImages/"+displayTower.__class__.__name__+"/"+str(displayTower.level) + ".png"))
        self.canvas.create_text(
            80, 75, text=displayTower.name, font=("times", 20))
        self.canvas.create_image(
            5, 5, image=self.towerImage, anchor=tkinter.NW)

        if issubclass(displayTower.__class__, TargetingTower):

            self.currentButtons.append(TargetButton(26, 30, 35, 39, 0))
            self.canvas.create_text(37, 28, text="> Health", font=(
                "times", 12), fill="white", anchor=tkinter.NW)

            self.currentButtons.append(TargetButton(26, 50, 35, 59, 1))
            self.canvas.create_text(37, 48, text="< Health", font=(
                "times", 12), fill="white", anchor=tkinter.NW)

            self.currentButtons.append(TargetButton(92, 50, 101, 59, 2))
            self.canvas.create_text(103, 48, text="> Distance", font=(
                "times", 12), fill="white", anchor=tkinter.NW)

            self.currentButtons.append(TargetButton(92, 30, 101, 39, 3))
            self.canvas.create_text(103, 28, text="< Distance", font=(
                "times", 12), fill="white", anchor=tkinter.NW)

            self.currentButtons.append(StickyButton(10, 40, 19, 49))
            self.currentButtons.append(SellButton(5, 145, 78, 168))
            if displayTower.upgradeCost:
                self.currentButtons.append(UpgradeButton(82, 145, 155, 168))
                self.canvas.create_text(120, 157, text="Upgrade: " + str(
                    displayTower.upgradeCost), font=("times", 12), fill="light green", anchor=tkinter.CENTER)

            self.canvas.create_text(28, 146, text="Sell", font=(
                "times", 22), fill="light green", anchor=tkinter.NW)

            self.currentButtons[displayTower.targetList].paint(self.canvas)
            if displayTower.stickyTarget:
                self.currentButtons[4].paint(self.canvas)

    def displayGeneric(self):
        self.currentButtons = []
        if gameGlobal.selectedTower == "<None>":
            self.text = None
            self.towerImage = None
        else:
            self.text = gameGlobal.selectedTower + " cost: " + \
                str(gameGlobal.towerCost[gameGlobal.selectedTower])
            self.towerImage = ImageTk.PhotoImage(Image.open(
                "images/towerImages/"+gameGlobal.towerDictionary[gameGlobal.selectedTower]+"/1.png"))
        self.canvas.delete(tkinter.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)
        self.canvas.create_text(80, 75, text=self.text)
        self.canvas.create_image(
            5, 5, image=self.towerImage, anchor=tkinter.NW)


class Displayboard:
    def __init__(self, game):
        self.canvas = tkinter.Canvas(
            master=game.frame,
            width=600,
            height=80,
            bg="gray",
            highlightthickness=0)
        self.canvas.grid(row=2, column=0)
        self.healthbar = Healthbar()
        self.moneybar = Moneybar()
        self.nextWaveButton = NextWaveButton(game)
        self.paint()

    def update(self):
        self.healthbar.update()
        self.moneybar.update()

    def paint(self):
        self.canvas.delete(tkinter.ALL)  # clear the screen
        self.healthbar.paint(self.canvas)
        self.moneybar.paint(self.canvas)
        self.nextWaveButton.paint(self.canvas)


class Towerbox:
    def __init__(self, game):
        self.game = game
        self.box = tkinter.Listbox(master=game.frame, selectmode="SINGLE", font=(
            "times", 18), height=18, width=13, bg="gray", fg="dark blue", bd=1, highlightthickness=0)
        self.box.insert(tkinter.END, "<None>")
        for i in gameGlobal.towerDictionary:
            self.box.insert(tkinter.END, i)
        for i in range(50):
            self.box.insert(tkinter.END, "<None>")
        self.box.grid(row=1, column=1, rowspan=2)
        self.box.bind("<<ListboxSelect>>", self.onselect)

    def onselect(self, event):
        global displayTower
        gameGlobal.selectedTower = str(self.box.get(self.box.curselection()))
        displayTower = None
        self.game.infoboard.displayGeneric()


class Healthbar():
    def __init__(self):
        self.text = str(health)

    def update(self):
        self.text = str(health)

    def paint(self, canvas):
        canvas.create_text(40, 40, text="Health: " + self.text, fill="black")


class Moneybar():
    def __init__(self):
        self.text = str(gameGlobal.money)

    def update(self):
        self.text = str(gameGlobal.money)

    def paint(self, canvas):
        canvas.create_text(240, 40, text="Money: " + self.text, fill="black")


class Monster(object):
    def __init__(self, distance):
        self.alive = True
        self.image = None
        self.health = 0
        self.maxHealth = 0
        self.speed = 0.0
        self.movement = 0.0
        self.tick = 0
        self.maxTick = 1
        self.distanceTravelled = distance
        if self.distanceTravelled <= 0:
            self.distanceTravelled = 0
        self.x, self.y = self.positionFormula(self.distanceTravelled)
        self.armor = 0
        self.magicresist = 0
        self.value = 0
        self.image = Image.open(
            "images/monsterImages/"+self.__class__.__name__ + ".png")
        self.image = ImageTk.PhotoImage(self.image)

    def update(self):
        if self.health <= 0:
            self.killed()
        self.move()

    def move(self):
        if self.tick >= self.maxTick:
            self.distanceTravelled += self.movement
            self.x, self.y = self.positionFormula(self.distanceTravelled)

            self.movement = self.speed
            self.tick = 0
            self.maxTick = 1
        self.tick += 1

    def positionFormula(self, distance):
        self.xPos = spawnx
        self.yPos = spawny + blockSize/2
        self.blocks = int((distance-(distance % blockSize))/blockSize)
        if self.blocks != 0:
            for i in range(self.blocks):
                if pathList[i] == 1:
                    self.xPos += blockSize
                elif pathList[i] == 2:
                    self.xPos -= blockSize
                elif pathList[i] == 3:
                    self.yPos += blockSize
                else:
                    self.yPos -= blockSize
        if distance % blockSize != 0:
            if pathList[self.blocks] == 1:
                self.xPos += (distance % blockSize)
            elif pathList[self.blocks] == 2:
                self.xPos -= (distance % blockSize)
            elif pathList[self.blocks] == 3:
                self.yPos += (distance % blockSize)
            else:
                self.yPos -= (distance % blockSize)
        if pathList[self.blocks] == 5:
            self.gotThrough()
        return self.xPos, self.yPos

    def killed(self):
        gameGlobal.money += self.value
        self.die()

    def gotThrough(self):
        global health
        health -= 1
        self.die()

    def die(self):
        self.alive = False
        gameGlobal.monsters.remove(self)

    def paint(self, canvas):
        canvas.create_rectangle(self.x-self.axis, self.y-3*self.axis/2,
                                self.x+self.axis-1, self.y-self.axis-1, fill="red", outline="black")
        canvas.create_rectangle(self.x-self.axis+1, self.y-3*self.axis/2 + 1, self.x-self.axis+(
            self.axis*2-2)*self.health/self.maxHealth, self.y-self.axis-2, fill="green", outline="green")
        canvas.create_image(self.x, self.y, image=self.image,
                            anchor=tkinter.CENTER)


class Monster1(Monster):
    def __init__(self, distance):
        super(Monster1, self).__init__(distance)
        self.maxHealth = 30
        self.health = self.maxHealth
        self.value = 5
        self.speed = float(blockSize)/2
        self.movement = blockSize/3
        self.axis = blockSize/2


class Monster2(Monster):
    def __init__(self, distance):
        super(Monster2, self).__init__(distance)
        self.maxHealth = 50
        self.health = self.maxHealth
        self.value = 10
        self.speed = float(blockSize)/4
        self.movement = float(blockSize)/4
        self.axis = blockSize/2

    def killed(self):
        gameGlobal.money += self.value
        gameGlobal.monsters.append(Monster1(self.distanceTravelled +
                                            blockSize*(.5-random.random())))
        self.die()


class AlexMonster(Monster):
    def __init__(self, distance):
        super(AlexMonster, self).__init__(distance)
        self.maxHealth = 500
        self.health = self.maxHealth
        self.value = 100
        self.speed = float(blockSize)/5
        self.movement = float(blockSize)/5
        self.axis = blockSize

    def killed(self):
        gameGlobal.money += self.value
        for i in range(5):
            gameGlobal.monsters.append(Monster2(
                self.distanceTravelled + blockSize*(.5-random.random())))
        self.die()


class BenMonster(Monster):
    def __init__(self, distance):
        super(BenMonster, self).__init__(distance)
        self.maxHealth = 200
        self.health = self.maxHealth
        self.value = 30
        self.speed = float(blockSize)/4
        self.movement = float(blockSize)/4
        self.axis = blockSize/2

    def killed(self):
        gameGlobal.money += self.value
        for i in range(2):
            gameGlobal.monsters.append(LeoMonster(
                self.distanceTravelled + blockSize*(.5-random.random())))
        self.die()


class LeoMonster(Monster):
    def __init__(self, distance):
        super(LeoMonster, self).__init__(distance)
        self.maxHealth = 20
        self.health = self.maxHealth
        self.value = 2
        self.speed = float(blockSize)/2
        self.movement = float(blockSize)/2
        self.axis = blockSize/4


class MonsterBig(Monster):
    def __init__(self, distance):
        super(MonsterBig, self).__init__(distance)
        self.maxHealth = 1000
        self.health = self.maxHealth
        self.value = 10
        self.speed = float(blockSize)/6
        self.movement = float(blockSize)/6
        self.axis = 3*blockSize/2


game = Game()  # start the application at Class Game()
