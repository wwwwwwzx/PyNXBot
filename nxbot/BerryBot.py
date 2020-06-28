import sys
from nxbot import SWSHBot
from structure import Screen

class BerryBot(SWSHBot):
    def __init__(self,ip,port = 6000):
        SWSHBot.__init__(self,ip,port)
        self.resets = 0

    def increaseResets(self):
                self.resets += 1

    def shakeTree(self):
        for i in range(3):
            self.click("A")
            self.pause(1)
        print("Shaking...")
        self.pause(3.2)
        self.click("A")
        self.pause(1.3)

    def battleRun(self):
        menu = False
        i = 0
        while menu is not True and i <= 20:
            self.currScreen = Screen(self.readBattleMenuAppear())
            if self.currScreen.battleMenuAppeared():
                menu = True
            else:
                self.click("B")
                self.pause(0.5)
            i += 1
        self.pause(0.3)
        print("Running from battle...")
        self.click("DUP")
        self.pause(0.7)
        self.click("A")

    def battleCheck(self):
        j = 0
        for i in range(10):
            self.currScreen = Screen(self.readBattleStart())
            if self.currScreen.battleStarted():
                j += 1
            self.pause(0.2)
            if j > 3:
                print("Battle started!")
                self.battleRun()
                return True
        return False

    def continueShaking(self,shakes = 0):
        for i in range(shakes):
            self.click("A")
            print("Shaking...")
            self.pause(1.6)
            print("Battle check")
            self.pause(1.6)
            if self.battleCheck():
                self.pause(4.8)
                print("Picking what's left...")
                break
            self.click("A")
            self.pause(1.3)
        self.click("B")

    def pickEverything(self):
        picked = False
        while picked == False:
            self.currScreen = Screen(self.readOverworldCheck())
            if self.currScreen.overworldCheck():
                picked = True
            else:
                self.click("B")
                self.pause(0.5)

    def stopBot(self):
        print("Exiting...")
        self.pause(0.5)
        self.close()
