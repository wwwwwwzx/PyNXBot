from nxbot import BDSPBot
from structure import BDSPEgg

class BDSPEggBot(BDSPBot):
    def __init__(self,ip,port = 6000):
        BDSPBot.__init__(self,ip,port)

    def getEggData(self):
        eggBlockPointer = f"[[[[[[main+{self.playerPrefsProvider:X}]+18]+C0]+28]+B8]]+458"
        return BDSPEgg(self.read_pointer(eggBlockPointer, 17))
