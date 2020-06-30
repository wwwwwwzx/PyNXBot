import sys
from nxbot import SWSHBot
from structure import Screen

class Cram_o_Matic(SWSHBot):
    def __init__(self,ip,port = 6000):
        SWSHBot.__init__(self,ip,port)

    def endApricornsCheck(self, apricorns = False):
        self.currScreen = Screen(self.readScreenOff())
        if self.currScreen.endedDialogue() and apricorns:
            print("Apricorns endend!")
        elif self.currScreen.endedDialogue():
            print("Dialogue ended!")
        return self.currScreen.endedDialogue()
