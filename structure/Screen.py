from structure.ByteStruct import ByteStruct

class Screen(ByteStruct):
    OVERWORLD = 0x5127

    def getScreenOff(self):
        return self.getushort(0x0)

    def isIntroAnimationSkippable(self):
        return self.getScreenOff() != 0x0

    def isOverworldScreen(self):
        return self.getScreenOff() == self.OVERWORLD

    def overworldCheck(self):
        return self.getbyte(0x0)
