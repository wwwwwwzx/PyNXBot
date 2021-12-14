from nxbot import BDSPBot

class BDSPIDsBot(BDSPBot):
    def __init__(self,ip,port = 6000):
        BDSPBot.__init__(self,ip,port)

    def refuseName(self):
        for i in range(4):
            self.click("A")
            self.pause(0.2)
        self.pause(1)
        for i in range(3):
            self.click("A")
            self.pause(0.2)
        self.pause(0.6)
        for i in range(4):
            self.click("PLUS")
            self.pause(0.2)
        self.pause(1)
        for i in range(5):
            self.click("B")
            self.pause(0.2)
