from structure.ByteStruct import ByteStruct

class Screen(ByteStruct):
    DIALOGENDED1 = 0xFFFF5127
    DIALOGENDED2 = 0xFFFFFFFF
    BATTLEMENU = 0xFF000000

    def getScreenOffByte(self):
        return self.getbyte(0x0)

    def getScreenOffShort(self):
        return self.getushort(0x0)

    def getScreenOffInt(self):
        return self.getuint(0x0)

    def getScreenOffLong(self):
        return self.getulong(0x0)

    def isIntroAnimationSkippable(self):
        #print(f"{self.getScreenOffLong():0X}")
        return self.getScreenOffLong() >= 0xFFFF

    def overworldCheck(self):
        #print(f"{self.getScreenOffByte():0X}")
        return self.getScreenOffByte()

    def battleMenuAppeared(self):
        #print(f"{self.getScreenOffInt():0X}")
        return self.getScreenOffInt() == self.BATTLEMENU

    def endedDialogue(self):
        #print(f"{self.getScreenOffInt():0X}")
        return self.getScreenOffInt() == self.DIALOGENDED1 or self.getScreenOffInt() == self.DIALOGENDED2
