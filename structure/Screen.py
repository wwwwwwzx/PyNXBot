from structure.ByteStruct import ByteStruct

class Screen(ByteStruct):
    OVERWORLD = 0x5127
    BATTLE = 0x0
    BATTLEMENU = 0xFFFFFFFFFFFFFFFF

    def getScreenOffShort(self):
        return self.getushort(0x0)

    def getScreenOff(self):
        return self.getulong(0x0)

    def isIntroAnimationSkippable(self):
        return self.getScreenOffByte() != 0x0

    def isOverworldScreen(self):
        return self.getScreenOffByte() == self.OVERWORLD

    def overworldCheck(self):
        return self.getbyte(0x0)

    def battleStarted(self):
        return self.getScreenOff() == self.BATTLE

    def battleMenuAppeared(self):
        return self.getScreenOff() == self.BATTLEMENU
