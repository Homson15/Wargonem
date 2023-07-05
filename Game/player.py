import os.path
from random import randint

import pygame

player = None

def getPlayer():

    global player
    if player is None:
        player = Player()
    return player


class Player:

    def __init__(self):

        self.name = "Player"
        self.hero = pygame.Surface((64,64))
        self.image = pygame.image.load(os.path.join("assets", "map", "hero.png"))

        self.hitbox = self.hero.get_rect()

        self.shiftX = 0
        self.shiftY = 0

        self.HP = 20
        self.maxHP = 20

        self.EXP = 0
        self.NEXT_LVL = 20

        self.attack = 5
        self.defeance = 0

        self.attackItems = 0
        self.defeanceItems = 0

        self.LVL = 1

    def move(self, x, y,):
        #print(f"{(x,y)}")
        self.shiftX=x
        self.shiftY=y

    def updatePos(self, bX=False, bY=False): #boolean X, boolean Y


        if bX:
            self.hitbox.x += self.shiftX

        if bY:
            self.hitbox.y += self.shiftY


    def setName(self, name):

        self.name = name


enemy = None

def getEnemy():

    global enemy

    if enemy == None:
        enemy = Enemy()

    return enemy


class Enemy:

    def __init__(self):

        self.surface = pygame.Surface((64, 64))

        self.hitbox = self.surface.get_rect()

        self.image = pygame.image.load(os.path.join("assets", "map", "krolik.png"))

        self.name = "Rabbit"

        self.HP = 0
        self.maxHP = 0
        self.attack = 0

        self.shiftX = 0
        self.shiftY = 0

    def loadSpaces(self, pos):

        self.maxX = pos[0]*64
        self.maxY = pos[1]*64


    def generate(self, pos):

        self.hitbox.x = randint(pos.x, self.maxX - 64 + pos.x)
        self.hitbox.y = randint(pos.y, self.maxY - 64 + pos.y)


        #print(f"Generated at {(self.hitbox.x, self.hitbox.y)}")
        #print(f"MAX = {(self.maxX, self.maxY)}")

        player = getPlayer()

        self.HP = int(abs(50/(player.LVL+5)-10)) * 10
        self.maxHP = self.HP
        self.attack = int(player.LVL * 2)

    def move(self, x, y, ):
        # print(f"{(x,y)}")
        self.shiftX = x
        self.shiftY = y

    def updatePos(self, bX=False, bY=False):  # boolean X, boolean Y

        if bX:
            self.hitbox.x += self.shiftX

        if bY:
            self.hitbox.y += self.shiftY




