import math

from PIL import Image, ImageTk

import gameGlobal
from mapglobals import blockSize


class Projectile(object):
    def __init__(self, x, y, damage, speed):
        self.hit = False
        self.x = x
        self.y = y
        self.speed = blockSize/2
        self.damage = damage
        self.speed = speed

    def update(self):
        try:
            if not target.alive:
                gameGlobal.projectiles.remove(self)
                return
        except:
            if self.hit:
                self.gotMonster()
            self.move()
            self.checkHit()

    def gotMonster(self):
        self.target.health -= self.damage
        gameGlobal.projectiles.remove(self)

    def paint(self, canvas):
        canvas.create_image(self.x, self.y, image=self.image)


class TrackingBullet(Projectile):
    def __init__(self, x, y, damage, speed, target):
        super(TrackingBullet, self).__init__(x, y, damage, speed)
        self.target = target
        self.image = Image.open("images/projectileImages/bullet.png")
        self.image = ImageTk.PhotoImage(self.image)

    def move(self):
        self.length = ((self.x-(self.target.x))**2 +
                       (self.y-(self.target.y))**2)**0.5
        self.x += self.speed*((self.target.x)-self.x)/self.length
        self.y += self.speed*((self.target.y)-self.y)/self.length

    def checkHit(self):
        if self.speed**2 > (self.x-(self.target.x))**2 + (self.y-(self.target.y))**2:
            self.hit = True


class PowerShot(TrackingBullet):
    def __init__(self, x, y, damage, speed, target, slow):
        super(PowerShot, self).__init__(x, y, damage, speed, target)
        self.slow = slow
        self.image = Image.open("images/projectileImages/powerShot.png")
        self.image = ImageTk.PhotoImage(self.image)

    def gotMonster(self):
        self.target.health -= self.damage
        if self.target.movement > (self.target.speed)/self.slow:
            self.target.movement = (self.target.speed)/self.slow
        gameGlobal.projectiles.remove(self)


class AngledProjectile(Projectile):
    def __init__(self, x, y, damage, speed, angle, givenRange):
        super(AngledProjectile, self).__init__(x, y, damage, speed)
        self.xChange = speed*math.cos(angle)
        self.yChange = speed*math.sin(-angle)
        self.range = givenRange
        self.image = Image.open("images/projectileImages/arrow.png")
        self.image = ImageTk.PhotoImage(self.image.rotate(math.degrees(angle)))
        self.target = None
        self.speed = speed
        self.distance = 0

    def checkHit(self):
        for i in range(len(gameGlobal.monsters)):
            if (gameGlobal.monsters[i].x-self.x)**2+(gameGlobal.monsters[i].y-self.y)**2 <= (blockSize)**2:
                self.hit = True
                self.target = gameGlobal.monsters[i]
                return

    def gotMonster(self):
        self.target.health -= self.damage
        self.target.tick = 0
        self.target.maxTick = 5
        gameGlobal.projectiles.remove(self)

    def move(self):
        self.x += self.xChange
        self.y += self.yChange
        self.distance += self.speed
        if self.distance >= self.range:
            gameGlobal.projectiles.remove(self)
