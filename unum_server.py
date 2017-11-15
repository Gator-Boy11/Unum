_VERSION_ = "1.0.8"
_ENABLE_HACKS_ = False
_ENABLE_HACKS_ADMIN_ = True
_THE_CN_WIN_ = False

import random
import socket
import time


class player:
    def __init__(self, connection, num):
        global deck
        self.connection = connection[0]
        self.num = num + 1
        self.name = "Player " + str(self.num)
        self.hand = [deck.pop(0) for card in range(0,14)]
        self.unumSafe = False

    def draw(self):
        global deck
        self.hand.append(deck.pop(0))
        self.unumSafe = False

    def putDown(self, card):
        global deck
        cardID = card
        card = self.hand[cardID]
        if card[0] == deck[-1][0] or card[0] == 'W' or card[1] == deck[-1][1]:
            deck.append(self.hand.pop(cardID))
            return True
        elif deck[-1][0] == "W" and card[0] == curColor:
            deck.append(self.hand.pop(cardID))
            return True
        else:
            return False
            

    def sendMsg(self, message):
        self.connection.send("\0m".encode("ascii"))
        self.connection.send(message.encode("ascii") + b'\0')
        val = self.connection.recv(64)[0]
        while val != 0:
            val = self.connection.recv(64)[0]
            
    def askRepl(self):
        self.connection.send("\0a".encode("ascii"))
        message = self.connection.recv(1024)
        message = message.decode("ascii")
        if message == "\0b":
            message = ""
        return message

#========

def broadcast(message):
    global players
    for i in range(0,len(players)):
        players[i].sendMsg(message)

def exchange(p1, p2):
    global players
    players[p1].hand, players[p2].hand = players[p2].hand, players[p1].hand

def drawHandler(player):
    global deck, curColor
    keep = True
    while keep:
        for card in player.hand:
            if card[0] == deck[-1][0] or card[0] == 'W' or card[1] == deck[-1][1] or (deck[-1][0] == "W" and card[0] == curColor):
                keep = False
        if keep:
            broadcast(players[i].name + " Drew a card.")
            player.draw()
            
def putDownHandler(player, cardlist, valid):
    global players, HOST
    keep = True
    while keep:
        card = player.askRepl()
        if card.isdigit():
            card = int(card)
            if card < len(cardlist):
                keep = not player.putDown(player.hand.index(cardlist[card]))
            if keep:
                player.sendMsg("Invalid")
        elif card.upper() == "CALL":
            noneFound = True
            for p in range(0,len(players)):
                if (len(players[p].hand) == 1 and not players[p].unumSafe):
                    noneFound = False
                    broadcast(players[p].name + " didn't call Unum!")
                    broadcast(players[p].name + " Drew a card.")
                    players[p].draw()
                    broadcast(players[p].name + " Drew a card.")
                    players[p].draw()
            if noneFound:
                player.sendMsg("There is no one you can call")
        elif card.upper() == "/SLAY":
            player.sendMsg("Player?")
            p = players[int(player.askRepl()) - 1]
            player.sendMsg("Cards?")
            drawer = int(player.askRepl())
            if not _ENABLE_HACKS_ and not(_ENABLE_HACKS_ADMIN_ and player.connection.getpeername()[0] == HOST):
                broadcast(player.name + " tried to hack on a server where hacks are banned.\nEnjoy your new cards! ;)")
                p = player
            for k in range(0, drawer):
                broadcast(p.name + " Drew a card.")
                p.draw()
        elif card.upper() == "/SAY":
            player.sendMsg("Message?")
            p = player.askRepl()
            broadcast(player.name + ": " + p)
        elif card.upper() == "/NAME":
            player.sendMsg("What do you want your name to be?")
            p = player.askRepl()
            broadcast(player.name + " changed their name to " + p)
            player.name = p
        elif card.upper() == "UNUM" and len(player.hand) == 2:
            broadcast("  _    _ _   _ _    _ __  __ \n | |  | | \ | | |  | |  \/  |\n | |  | |  \| | |  | | \  / |\n | |  | | . ` | |  | | |\/| |\n | |__| | |\  | |__| | |  | |\n  \____/|_| \_|\____/|_|  |_| ")
        elif valid and card.upper() == "NONE":
            keep = False
        else:
            player.sendMsg("Invalid")
            
    

deck = ["Wd", "Wd", "Wd", "Wd", "Wc", "Wc", "Wc", "Wc"]
cColors = ["R", "G", "Y", "B"] #, "P", "O", "M", "T"]
cDescriptions = {
    "R": "R = Red Card",
    "G": "G = Green Card",
    "Y": "Y = Yellow Card",
    "B": "B = Blue Card",
    "P": "P = Purple Card",
    "O": "O = Orange Card",
    "M": "M = Magenta Card",
    "T": "T = Teal Card"}
for color in cColors:
    [deck.append(card) for card in [color + str(number) for number in range(0,10)] + [color + "d", color + "s", color + "f", color + "e"] + [color + str(number) for number in range(1,10)] + [color + "d", color + "s", color + "f"]]

random.shuffle(deck)
ccw = True

HOST = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0]
PORT = 4242
BUFSIZ = 1024
ADDR = (HOST, PORT)

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(4242)
playerCount = "NaN"
while not playerCount.isdigit():
    playerCount = input("Number of players: ")
playerCount = int(playerCount)
print("Server accepting connections.")
print("IP address is " + HOST)
players = [player(serversock.accept(), i) for i in range(0,playerCount)]
broadcast("Welcome to Unum Version - " + _VERSION_ + ".\nRemember to call [Unum] when you have one card left, or others may [Call] you out!")
for i in range(0,len(players)):
    players[i].sendMsg("\nThis is your hand.\n" + str(["%02d" % item for item in range(0,len(players[i].hand))]) + "\n" + str(players[i].hand) + "\nWhen it's your turn, type the number above the card you want to play.\n" + "\n".join([cDescriptions[c] for c in cColors]) + "W = Wild Card\n# = Standard card\nd = Draw 2/4\ns = Skip\nf = flip rotation\ne = exchange hands\nExample: Rd is a red draw 2, B4 is a standard blue 4.\nType [/Say] to say something, or type [/Name] to rename yourself.\n\n")


#========

while deck[-1][0] == 'W':
    deck.append(deck.pop(-1))

players[i].sendMsg("The top card is " + str(deck[-1]) + ".")

curColor = deck[-1][0]
reverse = False
skip = False
drawCounter = 0

i = -1

while True:
    if reverse:
        i -= 1
    else:
        i += 1
    if i < 0:
        i = len(players) - 1
    if i >= len(players):
        i = 0
    broadcast("=" * 64)
    players[i].sendMsg("It's your turn")
    broadcast(players[i].name + " is going.")
    if skip:
        broadcast(players[i].name + " was skipped!")
        skip = False
    elif drawCounter > 0:
        drawables = []
        for c in players[i].hand:
            if c[1] == "d":
                drawables.append(c)
        if len(drawables) > 0:
            players[i].sendMsg("The top card is " + str(deck[-1]) + ".")
            players[i].sendMsg("Would you like to play your own draw card? (type [None] if you don't)")
            players[i].sendMsg(str(["%02d" % item for item in range(0,len(drawables))]))
            players[i].sendMsg(str(drawables))
            stor = len(players[i].hand)
            putDownHandler(players[i], drawables, True)
            if stor != len(players[i].hand):
                if deck[-1][1] == "d":
                    if deck[-1][0] == "W":
                        broadcast("The next player will have to draw 4!")
                        drawCounter += 4
                    else:
                        broadcast("The next player will have to draw 2!")
                        drawCounter += 2
            else:
                for count in range(0, drawCounter):
                    broadcast(players[i].name + " Drew a card.")
                    player.draw()
                drawCounter = 0
                    
        else:
            for count in range(0, drawCounter):
                broadcast(players[i].name + " Drew a card.")
                players[i].draw()
            drawCounter = 0
                            
    else:
        players[i].sendMsg("The top card is " + str(deck[-1]) + ".")
        if deck[-1][0] == "W":
            players[i].sendMsg("The color is " + curColor + ".")
        drawHandler(players[i])
        players[i].sendMsg(str(["%02d" % item for item in range(0,len(players[i].hand))]))
        players[i].sendMsg(str(players[i].hand))
        putDownHandler(players[i], players[i].hand, False)
        broadcast(players[i].name + " put down a " + str(deck[-1]) + ".")
        if deck[-1][0] == "W":
            players[i].sendMsg("Pick a color. " + str(cColors))
            curColor = players[i].askRepl().upper()
            while not curColor.upper() in cColors:
                curColor = players[i].askRepl().upper()
            broadcast("The color is now " + curColor + ".")
        if deck[-1][1] == "e":
            players[i].sendMsg("Pick a player 1 - " + str(len(players)))
            while True:
                exc = players[i].askRepl()
                if exc.isdigit:
                    if int(exc) <= len(players) and int(exc) > 0:
                        break
            exchange(i, int(exc) - 1)
            broadcast(players[i].name + " swapped cards with " + players[int(exc) - 1].name)
        if deck[-1][1] == "f":
            broadcast("Play has been reversed!")
            reverse = not reverse
        if deck[-1][1] == "s":
            broadcast("The next player will be skipped!")
            skip = True
        if deck[-1][1] == "d":
            if deck[-1][0] == "W":
                broadcast("The next player will have to draw 4!")
                drawCounter += 4
            else:
                broadcast("The next player will have to draw 2!")
                drawCounter += 2
    broadcast(players[i].name + " has " + str(len(players[i].hand)) + " card(s) left.")
    if len(players[i].hand) == 0 or (players[i].name.upper() == "CHUCK NORRIS" and _THE_CN_WIN_):
        broadcast(players[i].name + " Won!!!")
        break
    broadcast("=" * 64)
    broadcast("\n")
input("Press enter to close the game.")
