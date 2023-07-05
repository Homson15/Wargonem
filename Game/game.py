import pygame

import Logs.logs as log
from Game.chat import getChat
from settings.fileLoad import getMap, getTiles, getColors
from Game.player import getPlayer, getEnemy

import os

"""
Second UI file
---------------
Classes in this file are responsable for game mechanicks and everything in middle part of window


"""

game = None

def getGame():

    global game

    if game is None:
        game = Game(900, 800, getColors())
    return game


class Game(pygame.Surface):

    def __init__(self, width, height, colors):

        """
        :param name: width - width of middle part of window
        :param name: height - height of middle part of window
        :param name: colors - clolor palette loaded from a file
        """

        super().__init__((width,height))

        self.resolution = (width, height)

        self.colors = colors

        self.fill(colors["pale_green"])

        self.player = getPlayer()
        self.player.hitbox.x, self.player.hitbox.y = (width / 2, height/2)

        self.MAP_READY = False

        self.enemy = getEnemy()

        self.setMap("map1")

        self.enemy.generate(self.map.hitbox)


    def setMap(self, path):

        map = getMap(path)

        if map != "404" and len(map) > 0:
            self.map = Map((len(max(map)), len(map)), map, self.colors["pale_green"])
            self.enemy.loadSpaces((len(max(map)), len(map)))
            self.MAP_READY = True
        else:
            log.println("Invalid Map properties")
            self.MAP_READY = False

    def update(self):

        if self.MAP_READY:

            self.map.update()
            self.blit(self.map, self.map.hitbox)

            if not self.map.MOVEMENT_MODE_X and (self.player.hitbox.x+64 < 900 or  self.player.shiftX <= 0) and (self.player.hitbox.x > 0 or  self.player.shiftX >= 0):
                self.player.updatePos(bX=True)

            if not self.map.MOVEMENT_MODE_Y and (self.player.hitbox.y+64 < 800 or  self.player.shiftY <= 0) and (self.player.hitbox.y > 0 or  self.player.shiftY >= 0):
                self.player.updatePos(bY=True)

            self.blit(self.enemy.image, self.enemy.hitbox)
            self.blit(self.player.image, self.player.hitbox)


    def handleMovement(self, key='', reset=False):
        #print("handleMovement()")
        if not reset:
            if key == 'a':
                self.map.move(8, 0)
                self.enemy.move(8, 0)
                self.player.move(-8,0)
                self.player.image = pygame.image.load(os.path.join("assets", "map", "heroL.png"))

            if key == 'd':
                self.map.move(-8, 0)
                self.enemy.move(-8, 0)
                self.player.move(8, 0)
                self.player.image = pygame.image.load(os.path.join("assets", "map", "heroR.png"))

            if key == 'w':
                self.map.move(0, 8)
                self.enemy.move(0, 8)
                self.player.move(0, -8)
                self.player.image = pygame.image.load(os.path.join("assets", "map", "heroB.png"))

            if key == 's':
                self.map.move(0, -8)
                self.enemy.move(0, -8)
                self.player.move(0, 8)
                self.player.image = pygame.image.load(os.path.join("assets", "map", "heroF.png"))
        else:
            self.map.move(0, 0)
            self.enemy.move(0, 0)
            self.player.move(0,0)


    def battle(self):

        L = (f"{getPlayer().name} encountered {getEnemy().name} : {getEnemy().attack} , {getEnemy().maxHP}")

        log.println(L)
        getChat().chatBox.push(L)

        while(getPlayer().HP > 0):

            getEnemy().HP -= getPlayer().attack + getPlayer().attackItems
            L=(f"{getPlayer().name} did {getPlayer().attack + getPlayer().attackItems} damage to {getEnemy().name} {getEnemy().HP}/{getEnemy().maxHP}")

            log.println(L)
            getChat().chatBox.push(L)

            if getEnemy().HP <= 0:
                L=(f"{getEnemy().name} has beed defeated!")

                log.println(L)
                getChat().chatBox.push(L)

                return True

            getPlayer().HP -= max(0, int(getEnemy().attack - (getPlayer().defeance + getPlayer().defeanceItems)*0.2))

            L=(f"{getEnemy().name} did {max(0, int(getEnemy().attack- (getPlayer().defeance + getPlayer().defeanceItems)*0.2))} damage to {getPlayer().name} {getPlayer().HP}/{getPlayer().maxHP}")

            log.println(L)
            getChat().chatBox.push(L)

        return False


class Map(pygame.Surface):

    def __init__(self, res, bitMap, color):

        super().__init__((res[0]*64,res[1]*64))

        self.hitbox = self.get_rect()
        self.fill(color)

        self.hitbox.x = 0
        self.hitbox.y = 0

        self.shiftX = 0
        self.shiftY = 0

        self.MOVEMENT_MODE_X = True
        self.MOVEMENT_MODE_Y = True


        self.bitMap = bitMap

        self.tileInfo = getTiles()

        self.tiles = []


        for i in range(res[0]):
            for j in range(res[1]):
                try:
                    tile = self.tileInfo[self.bitMap[j][i]]
                    pos = (i, j)
                    temp = Tile(tile, pos)
                    self.blit(temp, temp.hitbox)
                except (KeyError, IndexError):
                    pos = (64 * i, 64 * j)
                    temp = Tile(self.tileInfo["blank"], pos)
                    self.blit(temp, temp.hitbox)




    def update(self):

        player = getPlayer()
        enemy = getEnemy()

        if (self.shiftX <= 0 and self.hitbox.x + self.hitbox.width - 8 > 900 and player.hitbox.x+32 >= 900/2) or (self.shiftX >= 0 and self.hitbox.x + 8 < 0 and player.hitbox.x-32 <= 900/2):
            self.MOVEMENT_MODE_X = True
            self.hitbox.x += self.shiftX
            enemy.updatePos(bX=True)
        else:
            self.MOVEMENT_MODE_X = False #if False, Hero will move on X axis


        if (self.shiftY <= 0 and self.hitbox.y + self.hitbox.height - 8 > 800 and player.hitbox.y+32 >= 800/2) or (self.shiftY >= 0 and self.hitbox.y + 8 < 0 and player.hitbox.y-32 <= 800/2):
            self.MOVEMENT_MODE_Y = True
            self.hitbox.y += self.shiftY
            enemy.updatePos(bY=True)
        else:
            self.MOVEMENT_MODE_Y = False #if False, Hero will move on Y axis




    def move(self, x, y):
        #print(f"x: {x} y: {y}")
        self.shiftX = x
        self.shiftY = y




class Tile(pygame.Surface):

    def __init__(self, tile, pos):
        self.tile = tile

        super().__init__(self.tile["res"])

        self.hitbox = self.get_rect()

        self.hitbox.x = pos[0]*self.tile["res"][0]
        self.hitbox.y = pos[1]*self.tile["res"][1]

        if self.tile["image"] == "blank.png":
            self.set_alpha(0)
        self.image = pygame.image.load(os.path.join("assets", "map", self.tile["image"]))

        self.blit(self.image, (0, 0))


