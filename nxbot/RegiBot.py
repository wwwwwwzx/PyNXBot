from nxbot import SWSHBot
from structure import PK8

class RegiBot(SWSHBot):
    def __init__(self,ip,port = 6000):
        SWSHBot.__init__(self,ip,port)

    def regiTrigger(self):
            self.click("A")
            self.pause(1)
            self.click("A")
            self.pause(1)
            print("Regi Triggered...")
           
    def Reset(self):
            self.click("HOME") #Home
            print("HOME clicked")
            self.pause(0.5)
            self.click("A")
            self.click("A")
            self.pause(3)
            self.click("A")
            self.click("A")
            self.pause(1)
