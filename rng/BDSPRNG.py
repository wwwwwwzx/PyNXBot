class XORSHIFT(object):
    def __init__(self, seed):
            self.seed = seed

    def state(self):
        return self.seed

    def next(self):
        t = self.seed[0]
        s = self.seed[3]

        t ^= (t << 11) & 0xFFFFFFFF
        t ^= t >> 8
        t ^= s ^ (s >> 19)

        self.seed = [self.seed[1], self.seed[2], self.seed[3], t]

        return ((t % 0xFFFFFFFF) + 0x80000000) & 0xFFFFFFFF

    def quickrand1(self,mask):
        return self.next() % mask

    def quickrand2(self,mask):
        return self.next() & mask

class FrameGenerator(object):
    def print(self):
        from lookups import Util
        print(f"S[0]: {self.seed[0]:08X} S[1]: {self.seed[1]:08X}\nS[2]: {self.seed[2]:08X} S[3]: {self.seed[3]:08X}\n")
        print(f"ShinyType: {self.ShinyType}    EC: {self.EC:08X}    PID: {self.PID:08X}")
        print(f"Ability: {self.Ability}    Nature: {Util.STRINGS.natures[self.Nature]}    IVs: {self.IVs}")

    def printTrainerInfo(self):
        from lookups import Util
        print(f"S[0]: {self.seed[0]:08X} S[1]: {self.seed[1]:08X}\nS[2]: {self.seed[2]:08X} S[3]: {self.seed[3]:08X}\n")
        print(f"G8TID: {self.G8TID}    TID: {self.TID}    SID: {self.SID}")

class Stationary(FrameGenerator):
    def __init__(self, seed, TID, SID, flawlessiv = 0, shinyLock = 0, ability = 4, gender = 0):
        self.seed = seed
        r = XORSHIFT(self.seed)
        self.EC = r.next()
        self.OTID = r.next()
        self.PID = r.next()
        fakeXor = (self.OTID >> 16) ^ (self.OTID & 0xFFFF) ^ (self.PID >> 16) ^ (self.PID & 0xFFFF)
        PSV = ((self.PID >> 16) ^ (self.PID & 0xFFFF)) >> 4
        realXor = (self.PID >> 16) ^ (self.PID & 0xFFFF) ^ TID ^ SID
        TSV = (TID ^ SID) >> 4
        if fakeXor < 16: #Force shiny
            self.ShinyType = 2 if fakeXor == 0 else 1
            if fakeXor != realXor:
                high = (self.PID & 0xFFFF) ^ TID ^ SID ^ (2 - self.ShinyType)
                self.PID = (high << 16) | (self.PID & 0xFFFF)
            self.ShinyType = "Square" if fakeXor == 0 else "Star"
        else: #Force non shiny
            self.ShinyType = 'None'
            if PSV == TSV:
                self.PID ^= 0x10000000
        i = 0
        self.IVs = [0,0,0,0,0,0]
        while i < flawlessiv:
            stat = r.quickrand1(0x6)
            if self.IVs[stat] == 0:
                self.IVs[stat] = 31
                i += 1
        for i in range(6):
            if self.IVs[i] == 0:
                self.IVs[i] = r.quickrand2(0x1F)
        self.Ability = r.quickrand2(0x1)
        self.Nature = r.quickrand1(25)

class IDs(FrameGenerator):
    def __init__(self, seed):
        self.seed = seed
        r = XORSHIFT(self.seed)
        self.SIDTID = r.next()
        self.TID = self.SIDTID & 0xFFFF
        self.SID = self.SIDTID >> 16
        self.G8TID = (((self.SID << 16) & 0xFFFFFFFF) | self.TID) % 1000000
