from mapglobals import gridSize

monsters = []
monstersByHealth = []
monstersByHealthReversed = []
monstersByDistance = []
monstersByDistanceReversed = []
monstersListList = [
    monstersByHealth,
    monstersByHealthReversed,
    monstersByDistance,
    monstersByDistanceReversed]

projectiles = []
blockDictionary = ["NormalBlock", "PathBlock", "WaterBlock"]

money = 5000000000
towerGrid = [[None for y in range(
    gridSize)] for x in range(gridSize)]

towerCost = {
    "Arrow Shooter": 150,
    "Bullet Shooter": 150,
    "Tack Tower": 150,
    "Power Tower": 200}

towerDictionary = {
    "Arrow Shooter": "ArrowShooterTower",
    "Bullet Shooter": "BulletShooterTower",
    "Tack Tower": "TackTower",
    "Power Tower": "PowerTower"}

selectedTower = "<None>"
