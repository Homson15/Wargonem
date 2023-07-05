import math
import os.path
from random import randint

import pygame

import Logs.logs as log
from Game.chat import getChat
from settings.fileLoad import getItems, getColors
from settings.DB import dataBase
from Game.player import getPlayer

eq = None

def getEQ():

    global eq
    if eq is None:
        eq = EQ(300,800,getColors())
    return eq

class EQ(pygame.Surface):

    def __init__(self, width, height, colors):
        res=(width,height)
        super().__init__(res)

        self.colors = colors


        self.resolution = (width, height)

        self.fill(colors["dark_green"])

        self.slot = []
        self.space = 5

        self.stats = Stats((290, 220), (5, 69))

        self.createSlots()

        self.itemList = getItems()
        self.pickedSlot = ""

        self.getEQ()

        self.trash = Trash((290, 80))


    def createSlots(self):

        res = width, height = [54, 54]

        for i in range(5):
            self.slot.append(Slot(res, i, 0, self.colors["pale_green"]))
            self.blit(self.slot[i], self.slot[i].hitbox)

        self.slot[0].belongs = "Weapon"
        self.slot[0].background = pygame.image.load(os.path.join("assets", "borders", "weaponslot.png"))

        self.slot[1].belongs = "Headgear"
        self.slot[1].background = pygame.image.load(os.path.join("assets","borders", "headgearslot.png"))
        self.slot[2].belongs = "Chestplate"
        self.slot[2].background = pygame.image.load(os.path.join("assets", "borders", "chestplateslot.png"))
        self.slot[3].belongs = "Gloves"
        self.slot[3].background = pygame.image.load(os.path.join("assets", "borders", "glovesslot.png"))
        self.slot[4].belongs = "Shoes"
        self.slot[4].background = pygame.image.load(os.path.join("assets", "borders", "shoesslot.png"))

        for j in range(5,12):
            for i in range(5):
                self.slot.append(Slot(res, i, j, self.colors["pale_green"]))
                self.slot[len(self.slot)-1].belongs = "Item"
                #print(len(self.slot))
                #print(f"{i} {j}")
                self.blit(self.slot[len(self.slot)-1], self.slot[len(self.slot)-1].hitbox)



    def changeColor(self, slot, color):
        slot.fill(color)
        slot.current_color = color
        self.blit(slot, slot.hitbox)

        #print("Zmiana koloru")

    def update(self):

        for each in self.slot:
            each.update()
            self.blit(each, each.hitbox)

        self.blit(self.trash.image, self.trash.hitbox)

        self.blit(self.stats, self.stats.hitbox)
        self.stats.updateStats()



    def addItem(self, item):
        for slot in self.slot:
            if slot.hitbox.y > 100:
                if slot.item["image"] == "blank.png":

                    try:
                        slot.add(self.itemList[item])
                        log.println(f"{self.itemList[item]['name']} added to inventory")
                        getChat().chatBox.push(f"{self.itemList[item]['name']} added to inventory")
                        return
                    except KeyError:
                        slot.add(self.itemList["0"])
                        return

    def getPickedImage(self):
        return pygame.image.load(os.path.join("assets", "items", self.pickedSlot.item["image"]))

    def swapItems(self, slot):

        try:
            temp = self.pickedSlot.item
            self.pickedSlot.item = slot.item
            slot.item = temp

        except AttributeError:

            log.println(f"Error while swaping items")

        self.pickedSlot = ""

        self.loadStats()

    def deleteItem(self):

        try:

            log.println(f"{self.pickedSlot.item['name']} deleted")
            self.pickedSlot.item = self.itemList["0"]

        except (KeyError, AttributeError):

            log.println(f"Error while deleting Item: {self.pickedSlot}")

        self.pickedSlot = ""


    def saveEQ(self):

        if os.path.exists(os.path.join("settings", "EQSave.db")):
            os.remove(os.path.join("settings", "EQSave.db"))

        dataBase().save(self.slot)

    def getEQ(self):


        table = dataBase().getData()

        for each in table:
            if each[1] == "Item":
                self.addItem(each[0])
            if each[1] == "Weapon":
                self.slot[0].add(self.itemList[each[0]])
            if each[1] == "Headgear":
                self.slot[1].add(self.itemList[each[0]])
            if each[1] == "Chestplate":
                self.slot[2].add(self.itemList[each[0]])
            if each[1] == "Gloves":
                self.slot[3].add(self.itemList[each[0]])
            if each[1] == "Shoes":
                self.slot[4].add(self.itemList[each[0]])

        self.loadStats()

    def clearEQ(self):

        for each in self.slot:

            each.item = self.itemList["0"]

    def heal(self):

        try:
            if self.pickedSlot.item["type"] == "usable":
                self.changeHP(value=self.pickedSlot.item["restoreHP"])
                self.deleteItem()
        except (AttributeError, KeyError):

            log.println(f"Error while using healing item: {self.pickedSlot}")



    def changeHP(self, value=0, str=""):

        player = getPlayer()

        try:

            if str != "":
                value = int(str)

            player.HP += value

            if player.HP > player.maxHP:
                player.HP = player.maxHP

            elif player.HP < 0:
                player.HP = 0

            self.stats.updateBars()

        except ValueError:
            log.println(f"Errror while changing HP points")

    def changeEXP(self, value=0, str=""):

        player = getPlayer()

        try:

            if str != "":
                value = int(str)

            player.EXP += value

            if player.EXP >= player.NEXT_LVL:
                player.EXP = 0
                player.LVL += 1

                player.NEXT_LVL += int((abs(75/(player.LVL+9) - 10)))

                player.attack += int(abs(500/(player.LVL+55) - 10))

                player.maxHP += int(abs(50/(player.LVL+5)-10) * 7)

                player.HP = player.maxHP

            self.stats.updateBars()

        except ValueError:
            log.println(f"Errror while changing HP points")


    def loadStats(self):

        getPlayer().defeanceItems = 0
        getPlayer().attackItems = 0


        for i in range(5):
            try:
                if self.slot[i].belongs == self.slot[i].item["type"]:
                    getPlayer().attackItems += self.slot[i].item["attack"]
                    getPlayer().defeanceItems += self.slot[i].item["def"]
            except KeyError:
                log.println(f"Error while counting stats")

    def drop(self):

        x = randint(1,100)

        if x < 50:
            return
        elif x < 75:
            x=randint(1,5)
            if x == 5:
                self.addItem("2") #Big HP Potion
            else:
                self.addItem("1") #Small HP Potion
        elif x < 90:
            x=randint(0,4)
            self.addItem(str(3+x*3))
        elif x <  98:
            x=randint(0,4)
            self.addItem(str(4+x*3))
        else:
            x=randint(0,4)
            self.addItem(str(5+x*3))

class Slot(pygame.Surface):

    belongs = ""

    def __init__(self, res, column, row, color):
        super().__init__(res)

        self.background = pygame.image.load(os.path.join("assets", "borders", "slot.png"))


        self.item = {"image": "blank.png"}
        self.image = pygame.image.load(os.path.join("assets", "items", "blank.png"))


        self.hitbox = self.get_rect()

        self.hitbox.x = 5 + res[0]*column + 5*column
        self.hitbox.y = 5 + res[1]*row + 5*row


        self.fill(color)

        self.current_color = color

    def add(self, item):

        self.item = item
        self.update()


    def update(self):

        self.blit(self.background, (0,0))
        self.image = pygame.image.load(os.path.join("assets", "items", self.item["image"]))
        self.blit(self.image, (2,2))



class Stats(pygame.Surface):

    class Bar(pygame.Surface):

        def __init__(self, res, pos, color):

            super().__init__(res)

            self.hitbox = self.get_rect()

            self.hitbox.x = pos[0]
            self.hitbox.y = pos[1]



            self.fill(color)



    def __init__(self, res, pos):

        self.colors = getColors()

        super().__init__(res)

        self.hitbox = self.get_rect()

        self.hitbox.x = pos[0]
        self.hitbox.y = pos[1]

        self.fill((0,0,0))

        self.image =  pygame.image.load(os.path.join("assets", "borders", "stats.png"))


        self.HP = self.Bar((10, 188-74),(36,74), self.colors["full_red"])
        self.EXP = self.Bar((10, 188-74),(58,74), self.colors["yellow"])

        self.updateBars()


    def updateBars(self):

        self.fill((0,0,0))

        player = getPlayer()

        ratio = player.HP/player.maxHP

        self.HP = self.Bar((10, ratio*(188-74)), (36, (1-ratio)*(188-74)+74), self.colors["full_red"])

        ratio = player.EXP/player.NEXT_LVL

        self.EXP = self.Bar((10, ratio*(188-74)), (58, (1-ratio)*(188-74)+74), self.colors["yellow"])

        self.blit(self.HP, self.HP.hitbox)
        self.blit(self.EXP, self.EXP.hitbox)

        self.blit(self.image, (0,0))

    def updateStats(self):

        statBox = StatBox()
        self.blit(statBox, statBox.hitbox)



class StatBox(pygame.Surface):

    def __init__(self):

        super().__init__((100,220))

        self.hitbox = self.get_rect()

        self.hitbox.x = 190

        font = pygame.font.Font(None, 26)

        colors = getColors()

        self.fill(colors["dark_green"])

        LVL= font.render("LVL:", True, colors["white"])
        LVL_V = font.render( str(getPlayer().LVL), True, colors["white"])

        attack = font.render("Attack:", True, colors["white"])
        attack_V = font.render( str(getPlayer().attack + getPlayer().attackItems), True, colors["white"])

        defeance = font.render("Defence:" , True, colors["white"])
        defeance_V = font.render( str(getPlayer().defeance + getPlayer().defeanceItems), True, colors["white"])


        self.blit(LVL, (0, 20))
        self.blit(LVL_V, (0, 40))
        self.blit(attack, (0, 80))
        self.blit(attack_V, (0, 100))
        self.blit(defeance, (0, 140))
        self.blit(defeance_V, (0, 160))


class Trash(pygame.Surface):

    def __init__(self, res):

        super().__init__(res)

        self.hitbox = self.get_rect()

        self.hitbox.x = 5
        self.hitbox.y = 715

        self.image = pygame.image.load(os.path.join("assets", "borders", "trash.png"))

