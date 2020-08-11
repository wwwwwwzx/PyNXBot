from structure.ByteStruct import ByteStruct

class WC8(ByteStruct):
    SIZE = 0x2D0
    LANG = ['JPN','ENG','FRE','ITA','GER','SPA','KOR','CHS','CHT']

    def isPokemon(self):
        return self.getbyte(0x11) == 1

    def fullID(self):
        return self.getuint(0x20)

    def isNicknamed(self,idx = 0):
        return self.nickname(idx) != ''

    def nickname(self,idx):
        return self.getstring(0x30 + (idx * 0x1C),0x1A)

    def hasOT(self, idx = 0):
        return self.ownername(idx) != ''

    def ownername(self,idx):
        return self.getstring(0x12C + (idx * 0x1C),0x1A)

    def metLocation(self):
        return self.getushort(0x22A)

    def ball(self):
        return self.getushort(0x22C)

    def heldItem(self):
        return self.getushort(0x22E)

    def move(self,ii):
        return self.getushort(0x230 + 2 * ii)

    def relearnmove(self,ii):
        return self.getushort(0x238 + 2 * ii)

    def species(self):
        return self.getushort(0x240)

    def forme(self):
        return self.getbyte(0x242)

    def gender(self):
        return self.getbyte(0x243)

    def level(self):
        return self.getbyte(0x244)

    def nature(self):
        return self.getbyte(0x246)

    def abilityType(self):
        return self.getbyte(0x247)

    def shinyType(self):
        return self.getbyte(0x248)

    def metLevel(self):
        return self.getbyte(0x249)

    def canGMax(self):
        return self.getbyte(0x24B) != 0

    def isShiny(self):
        return self.shinyType == 2 or self.shinyType == 3

    def ribbonflags(self):
        for ii in range(0x20):
            if self.data[0x24C + ii] != 0xFF:
                yield [ii, self.data[0x24C + ii]]

    def IV_HP(self):
        return self.getbyte(0x26C)
    def IV_Atk(self):
        return self.getbyte(0x26D)
    def IV_Def(self):
        return self.getbyte(0x26E)
    def IV_Spe(self):
        return self.getbyte(0x26F)
    def IV_SpA(self):
        return self.getbyte(0x270)
    def IV_SpD(self):
        return self.getbyte(0x271)

    def OTgender(self):
        return self.getbyte(0x272)

    def EV_HP(self):
        return self.getbyte(0x273)
    def EV_Atk(self):
        return self.getbyte(0x274)
    def EV_Def(self):
        return self.getbyte(0x275)
    def EV_Spe(self):
        return self.getbyte(0x276)
    def EV_SpA(self):
        return self.getbyte(0x277)
    def EV_SpD(self):
        return self.getbyte(0x278)
