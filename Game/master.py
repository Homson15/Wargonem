import pygame
import os

from Game.chat import getChat
from Game.game import getGame
from Game.eq import getEQ
from Game.player import getPlayer, getEnemy

import Logs.logs as log
import settings.fileLoad as load

class Master:

    def __init__(self):

        log.println("Begin creating game...")

        self.running = True
        self.pause = True
        self.DRAW_PICKED_ITEM = False

        pygame.init()

        self.FPS = pygame.time.Clock()




            # Load Files Values

        self.colors = load.getColors()
        if self.colors == "404":
            self.running = False
            return



        log.println("File status: Exists")


        #Variable Setup


        #print(self.settings)
        self.resolution = (1500, 800)

        log.println("All variables set")

        # Setup every element


        self.player = getPlayer()

        self.setScreen()
        self.setGameParts()


        log.println("Everything loaded Correctly!")


    def setScreen(self):


        pygame.display.set_caption("Wargonem")
        icon = pygame.image.load(os.path.join("assets", "icon", "icon.png"))
        pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode(self.resolution)

    def setGameParts(self):

        #Setting up UI

        getChat()

        getGame()

        getEQ()

        #Showing UI

        self.updateParts()

        pygame.display.update()




    def gameLoop(self):
        while self.running:

            M_POS = pygame.mouse.get_pos()
            #print(M_POS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    getEQ().saveEQ()
                    self.running = False
                    log.println("EXIT")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for slot in getEQ().slot:
                        #self.UI[2].changeColor(slot, self.colors["pale_green"])
                        if slot.hitbox.collidepoint(M_POS[0] - 1200, M_POS[1]):
                            #self.UI[2].changeColor(slot, self.colors["blue"])
                            getEQ().pickedSlot = slot
                            self.DRAW_PICKED_ITEM = True

                    if getChat().input.hitbox.collidepoint(M_POS[0], M_POS[1]):
                        getChat().input.active = True
                    else:
                        getChat().input.active = False

                    log.println((M_POS[0]-300, M_POS[1]))
                    log.println((getEnemy().hitbox.x, getEnemy().hitbox.y))


                    if getEnemy().hitbox.collidepoint(M_POS[0]-300, M_POS[1]):
                        if -64 < getEnemy().hitbox.x < 900 and -64 < getEnemy().hitbox.y < 800:
                            if getGame().battle():

                                getEQ().changeEXP(value=int(getPlayer().NEXT_LVL * 0.4 / getPlayer().LVL))
                                getEQ().drop()


                                getEnemy().generate(getGame().map.hitbox)
                            else:
                                getPlayer().HP = 1
                                getChat().chatBox.push(f"You have been defeated but managed escaped with 1HP")
                                getChat().chatBox.push(f"Some EXP has been lost")
                                getEQ().changeEXP(value=-(getPlayer().EXP/5))

                if event.type == pygame.MOUSEBUTTONUP:
                    for slot in getEQ().slot:
                        if slot.hitbox.collidepoint(M_POS[0] - 1200, M_POS[1]):
                            getEQ().swapItems(slot)

                    if getEQ().trash.hitbox.collidepoint(M_POS[0]-1200, M_POS[1]):
                        getEQ().deleteItem()

                    if getEQ().stats.hitbox.collidepoint(M_POS[0]-1200, M_POS[1]):
                        getEQ().heal()

                    self.DRAW_PICKED_ITEM = False



                if event.type == pygame.KEYDOWN:
                    if getChat().input.active:
                        getChat().handle_input(event, self.player.name)
                    else:
                        getGame().handleMovement(key = event.unicode)


                if event.type == pygame.KEYUP:
                    getGame().handleMovement(reset = True)

            self.executeCommands()
            self.updateParts()

            if self.DRAW_PICKED_ITEM:
                self.screen.blit(getEQ().getPickedImage(), M_POS)

            pygame.display.flip()

            self.FPS.tick(60)

    def updateParts(self):


        self.screen.blit(getGame(), (300, 0))
        getGame().update()
        getChat().update()
        getEQ().update()


        self.screen.blit(getChat(), (0, 0))
        self.screen.blit(getEQ(), (1200, 0))



    def executeCommands(self):

        while len(getChat().commandQueue) > 0:

            command = getChat().commandQueue[0][1:]

            getChat().chatBox.push(f"Executing '{command}'")

            try:

                log.println(f"Executing {command}")

                if command.startswith("change-main-color"):
                    command = command[18:]
                    getEQ().fill(self.colors[command])

                if command.startswith("add"):
                    command = command[4:]
                    getEQ().addItem(command)

                if command.startswith("hp"):
                    command = command[3:]
                    getEQ().changeHP(str=command)

                if command.startswith("exp"):
                    command = command[4:]
                    getEQ().changeEXP(str=command)

                if command.startswith("clear"):
                    getEQ().clearEQ()

            except KeyError:
                getChat().chatBox.push(f"Console: Unable to execute command")


            getChat().commandQueue.pop(0)





