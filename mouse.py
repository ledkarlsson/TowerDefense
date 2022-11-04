from tkinter import NW
from PIL import Image
from PIL import ImageTk
from mapGlobal import mapSize, blockGrid, blockSize, gridSize


class Mouse():
    def __init__(self, game):  # when i define a "Mouse", this is what happens
        self.game = game
        self.x = 0
        self.y = 0
        self.gridx = 0
        self.gridy = 0
        self.xoffset = 0
        self.yoffset = 0
        self.pressed = False
        # whenever left mouse button is pressed, go to def released(event)
        game.root.bind("<Button-1>", self.clicked)
        # whenever left mouse button is released, go to def released(event)
        game.root.bind("<ButtonRelease-1>", self.released)
        # whenever left mouse button is dragged, go to def released(event)
        game.root.bind("<Motion>", self.motion)
        self.image = Image.open("images/mouseImages/HoveringCanPress.png")
        self.image = ImageTk.PhotoImage(self.image)
        self.canNotPressImage = Image.open(
            "images/mouseImages/HoveringCanNotPress.png")
        self.canNotPressImage = ImageTk.PhotoImage(self.canNotPressImage)

    def clicked(self, event):
        self.pressed = True  # sets a variable
        self.image = Image.open("images/mouseImages/Pressed.png")
        self.image = ImageTk.PhotoImage(self.image)

    def released(self, event):
        self.pressed = False
        self.image = Image.open("images/mouseImages/HoveringCanPress.png")
        self.image = ImageTk.PhotoImage(self.image)

    def motion(self, event):
        if event.widget == self.game.canvas:
            self.xoffset = 0
            self.yoffset = 0
        elif event.widget == self.game.infoboard.canvas:
            self.xoffset = mapSize
            self.yoffset = 0
        elif event.widget == self.game.towerbox.box:
            self.xoffset = mapSize
            self.yoffset = 174
        elif event.widget == self.game.displayboard.canvas:
            self.yoffset = mapSize
            self.xoffset = 0
        self.x = event.x + self.xoffset  # sets the "Mouse" x to the real mouse's x
        self.y = event.y + self.yoffset  # sets the "Mouse" y to the real mouse's y
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        self.gridx = int((self.x - (self.x % blockSize)) / blockSize)
        self.gridy = int((self.y - (self.y % blockSize)) / blockSize)

    def update(self):
        if self.gridx >= 0 and self.gridx <= gridSize - 1 and self.gridy >= 0 and self.gridy <= gridSize - 1:
            blockGrid[self.gridx][self.gridy].hoveredOver(
                self.pressed, self.game)
        else:
            self.game.displayboard.nextWaveButton.checkPress(
                self.pressed, self.x - self.xoffset, self.y - self.yoffset)
            self.game.infoboard.buttonsCheck(
                self.pressed, self.x - self.xoffset, self.y - self.yoffset)

    def paint(self, canvas):
        if self.gridx >= 0 and self.gridx <= gridSize - 1 and self.gridy >= 0 and self.gridy <= gridSize - 1:
            if blockGrid[self.gridx][self.gridy].canPlace:
                canvas.create_image(
                    self.gridx * blockSize, self.gridy * blockSize, image=self.image, anchor=NW)
            else:
                canvas.create_image(
                    self.gridx * blockSize, self.gridy * blockSize, image=self.canNotPressImage, anchor=NW)
