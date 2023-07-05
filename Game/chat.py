import pygame

import Logs.logs as log
import os

from settings.fileLoad import  getColors

chat = None

def getChat():

    global chat
    if chat is None:
        chat = Chat(300, 800, getColors())
    return chat


class Chat(pygame.Surface):

    def __init__(self, width, height, colors):

        super().__init__((width,height))

        self.colors = colors

        self.resolution = (width, height)

        self.fill(colors["dark_green"])

        self.input = ChatInput((width-10, 45), colors["pale_green"])

        self.blit(self.input, self.input.hitbox)


        self.chatBox = ChatLogs((width-10, height-60), colors["dark_green"])

        self.blit(self.chatBox, self.chatBox.hitbox)

        self.commandQueue = []


    def handle_input(self, event, source):
        self.input.handle(event)

        while len(self.input.queue) > 0:
            if self.input.queue[0].startswith("/"):
                self.commandQueue.append(self.input.queue[0])
            else:
                self.chatBox.push(f"{source}: {self.input.queue[0]}")
            self.input.queue.pop(0)



    def update(self):
        self.blit(self.input, self.input.hitbox)
        self.blit(self.input.txt_surface, (self.input.hitbox.x+5, self.input.hitbox.y+18))


        self.blit(self.chatBox, self.chatBox.hitbox)
        for msg in self.chatBox.messages:
            self.blit(msg.txt_surface, (msg.hitbox.x, msg.hitbox.y))


class ChatInput(pygame.Surface):

    def __init__(self, res, color):

        super().__init__(res)

        self.color = color

        self.hitbox = self.get_rect()

        self.fill(color)

        self.hitbox.y = 750
        self.hitbox.x = 5

        self.background = pygame.image.load(os.path.join("assets", "borders", "input.png"))
        self.blit(self.background, (0,0))

        self.font =  pygame.font.Font(None, 26)
        self.txt_surface = self.font.render("", True, color)

        self.active = False
        self.value = ""

        self.queue = []

    def handle(self, event):

        if event.key == pygame.K_RETURN:
            log.println(self.value)
            self.queue.append(self.value)
            self.value = ""
        elif event.key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]
        elif len(self.value) < 30:
            self.value += event.unicode

        #wypisuje litery na inpucie przy pisaniu

        self.txt_surface = self.font.render(self.value, True, (255,255,255))

        self.blit(self.txt_surface, (self.hitbox.x, self.hitbox.y))

        #pygame.draw.rect(self, self.color, self.hitbox, 2)


class ChatLogs(pygame.Surface):

    def __init__(self, res, color):
        super().__init__(res)

        self.hitbox = self.get_rect()

        self.color = color
        self.fill(color)

        self.hitbox.y = 5
        self.hitbox.x = 5

        self.messages = []

    def push(self, message):

        #zapełnianie kwadratu z logami chatu

        cut = []

        while len(message)>30:

            cut.insert(0,Message((self.hitbox.width, 25), message[-int(len(message)%30):], (5+2, 740-25), self.color))

            message = message[:-int(len(message)%30)]

        for each in self.messages:
            each.push()

        msg = Message((self.hitbox.width, 25), message, (5 + 2, 740 - 25), self.color)

        self.messages.append(msg)

        for element in cut:

            for each in self.messages:
                each.push()

            self.messages.append(element)

        while self.messages[0].hitbox.y < 5:
            self.messages.pop(0)







class Message(pygame.Surface):

    def __init__(self, res, message, pos, color):

        super().__init__(res)

        self.value = message


        self.font = pygame.font.Font(None, 26)
        self.txt_surface = self.font.render("", True, (255,255,255))

        self.hitbox = self.get_rect()
        self.fill(color)

        self.hitbox.x = pos[0]
        self.hitbox.y = pos[1]

        self.txt_surface = self.font.render(self.value, True, (255, 255, 255))

        #self.blit(self.txt_surface, (self.hitbox.x, self.hitbox.y))


    def push(self):
        self.hitbox.y = self.hitbox.y - self.hitbox.height


