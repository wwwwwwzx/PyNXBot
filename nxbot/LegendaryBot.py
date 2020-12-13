from nxbot import SWSHBot
from structure import PK8,Screen

class BerryBot(SWSHBot):
    def __init__(self,ip,port = 6000):
        SWSHBot.__init__(self,ip,port)

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
        while menu is not True and i <= 40:
            self.currScreen = Screen(self.readBattleStart())
            if self.currScreen.battleMenuAppeared():
                menu = True
            else:
                self.click("B")
                self.pause(0.5)
            i += 1
        self.pause(0.5)
        print("Running from battle...")
        self.click("DUP")
        self.pause(0.5)
        self.click("A")

    def battleCheck(self):
        if PK8(self.readWild()).isValid():
                print("Wild battle started!")
                self.battleRun()
                return True
        return False

    def continueShaking(self,shakes = 0):
        battle = False
        for i in range(shakes):
            self.click("A")
            print("Shaking...")
            self.pause(3.2)
            #print("Battle check")
            if self.battleCheck():
                self.pause(5.2)
                battle = True
                print("Picking what's left...")
                break
            self.click("A")
            self.pause(1.3)
        self.click("B")
        if battle is not True:
            print("Picking everything...")

    def pickEverything(self):
        picked = False
        i = 0
        while picked is not True and i <= 30:
            self.currScreen = Screen(self.readOverworldCheck())
            if self.currScreen.overworldCheck():
                picked = True
            else:
                self.click("B")
                self.pause(0.5)
            i += 1

    def pickBeforeLeaving(self):
        pick = input("Picking before exiting? (y/n): ")
        if pick == 'y' or pick == 'Y':
            self.pickEverything()
        print()
        self.close()
