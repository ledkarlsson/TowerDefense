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
        if displayTower.stickyTarget == False:
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
        global money
        global displayTower
        if money >= displayTower.upgradeCost:
            money -= displayTower.upgradeCost
            displayTower.upgrade()
