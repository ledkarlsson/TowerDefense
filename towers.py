import math
import tkinter

from PIL import Image, ImageTk

import gameGlobal
from mapglobals import blockSize
from projectiles import AngledProjectile, PowerShot, TrackingBullet


class Tower(object):
    def __init__(self, x, y, gridx, gridy):
        self.upgradeCost = None
        self.level = 1
        self.range = 0
        self.clicked = False
        self.x = x
        self.y = y
        self.gridx = gridx
        self.gridy = gridy
        self.image = Image.open(
            "images/towerImages/" + self.__class__.__name__+"/1.png")
        self.image = ImageTk.PhotoImage(self.image)

    def update(self):
        pass

    def upgrade(self):
        self.level = self.level+1
        self.image = Image.open(
            "images/towerImages/"+self.__class__.__name__+"/"+str(self.level)+".png")
        self.image = ImageTk.PhotoImage(self.image)
        self.nextLevel()

    def sold(self):
        gameGlobal.towerGrid[self.gridx][self.gridy] = None

    def paintSelect(self, canvas):
        canvas.create_oval(self.x-self.range, self.y-self.range, self.x +
                           self.range, self.y + self.range, fill=None, outline="white")

    def paint(self, canvas):
        canvas.create_image(self.x, self.y, image=self.image,
                            anchor=tkinter.CENTER)


class ShootingTower(Tower):
    def __init__(self, x, y, gridx, gridy):
        super(ShootingTower, self).__init__(x, y, gridx, gridy)
        self.bulletsPerSecond = None
        self.ticks = 0
        self.damage = 0
        self.speed = None

    def update(self):
        self.prepareShot()


class TargetingTower(ShootingTower):
    def __init__(self, x, y, gridx, gridy):
        super(TargetingTower, self).__init__(x, y, gridx, gridy)
        self.target = None
        self.targetList = 0
        self.stickyTarget = False

    def prepareShot(self):
        self.checkList = gameGlobal.monstersListList[self.targetList]
        if self.ticks != 20/self.bulletsPerSecond:
            self.ticks += 1
        if not self.stickyTarget:
            for i in range(len(self.checkList)):
                if (self.range+blockSize/2)**2 >= (self.x-self.checkList[i].x)**2 + (self.y-self.checkList[i].y)**2:
                    self.target = self.checkList[i]
        if self.target:
            if self.target.alive and (self.range + blockSize/2) >= ((self.x-self.target.x)**2 + (self.y-self.target.y)**2)**0.5:
                if self.ticks >= 20/self.bulletsPerSecond:
                    self.shoot()
                    self.ticks = 0
            else:
                self.target = None
        elif self.stickyTarget:
            for i in range(len(self.checkList)):
                if (self.range+blockSize/2)**2 >= (self.x-self.checkList[i].x)**2 + (self.y-self.checkList[i].y)**2:
                    self.target = self.checkList[i]


class ArrowShooterTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super(ArrowShooterTower, self).__init__(x, y, gridx, gridy)
        self.name = "Arrow Shooter"
        self.infotext = "ArrowShooterTower at [" + \
            str(gridx) + "," + str(gridy) + "]."
        self.range = blockSize*10
        self.bulletsPerSecond = 1
        self.damage = 10
        self.speed = blockSize
        self.upgradeCost = 50

    def nextLevel(self):
        if self.level == 2:
            self.upgradeCost = 100
            self.range = blockSize*11
            self.damage = 12
        elif self.level == 3:
            self.upgradeCost = None
            self.bulletsPerSecond = 2

    def shoot(self):
        self.angle = math.atan2(self.y - self.target.y, self.target.x-self.x)
        gameGlobal.projectiles.append(AngledProjectile(
            self.x, self.y, self.damage, self.speed, self.angle, self.range+blockSize/2))


class BulletShooterTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super(BulletShooterTower, self).__init__(x, y, gridx, gridy)
        self.name = "Bullet Shooter"
        self.infotext = "BulletShooterTower at [" + \
            str(gridx) + "," + str(gridy) + "]."
        self.range = blockSize*6
        self.bulletsPerSecond = 4
        self.damage = 5
        self.speed = blockSize/2

    def shoot(self):
        gameGlobal.projectiles.append(TrackingBullet(
            self.x, self.y, self.damage, self.speed, self.target))


class PowerTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super(PowerTower, self).__init__(x, y, gridx, gridy)
        self.name = "Power Tower"
        self.infotext = "PowerTower at [" + \
            str(gridx) + "," + str(gridy) + "]."
        self.range = blockSize*8
        self.bulletsPerSecond = 10
        self.damage = 1
        self.speed = blockSize
        self.slow = 3

    def shoot(self):
        gameGlobal.projectiles.append(
            PowerShot(self.x, self.y, self.damage, self.speed, self.target, self.slow))


class TackTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super(TackTower, self).__init__(x, y, gridx, gridy)
        self.name = "Tack Tower"
        self.infotext = "TackTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = blockSize*5
        self.bulletsPerSecond = 1
        self.damage = 10
        self.speed = blockSize

    def shoot(self):
        for i in range(8):
            self.angle = math.radians(i*45)
            gameGlobal.projectiles.append(AngledProjectile(
                self.x, self.y, self.damage, self.speed, self.angle, self.range))
