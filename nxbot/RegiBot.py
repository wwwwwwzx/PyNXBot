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
           closeGame()
           skipIntroAnimation()
           enterGame()
