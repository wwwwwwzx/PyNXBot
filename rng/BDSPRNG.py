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

class XOROSHIRO128PLUS(object):
    ulongmask = 2 ** 64 - 1
    uintmask = 2 ** 32 - 1

    def __init__(self, seed):
        _seed1 = (seed - 0x61C8864680B583EB) & XOROSHIRO128PLUS.ulongmask
        _seed2 = (seed + 0x3C6EF372FE94F82A) & XOROSHIRO128PLUS.ulongmask
        _seed1 = (0xBF58476D1CE4E5B9 * (_seed1 ^ (_seed1 >> 30))) & XOROSHIRO128PLUS.ulongmask
        _seed2 = (0xBF58476D1CE4E5B9 * (_seed2 ^ (_seed2 >> 30))) & XOROSHIRO128PLUS.ulongmask
        _seed1 = (0x94D049BB133111EB * (_seed1 ^ (_seed1 >> 27))) & XOROSHIRO128PLUS.ulongmask
        _seed2 = (0x94D049BB133111EB * (_seed2 ^ (_seed2 >> 27))) & XOROSHIRO128PLUS.ulongmask
        seed1 = _seed1 ^ (_seed1 >> 31)
        seed2 = _seed2 ^ (_seed2 >> 31)
        self.seed = [seed1, seed2]

    def state(self):
        return self.seed

    @staticmethod
    def rotl(x, k):
        return ((x << k) | (x >> (64 - k))) & XOROSHIRO128PLUS.ulongmask

    def next(self):
        s0, s1 = self.seed
        result = (s0 + s1) & XOROSHIRO128PLUS.ulongmask
        s1 ^= s0
        self.seed = [XOROSHIRO128PLUS.rotl(s0, 24) ^ s1 ^ ((s1 << 16) & XOROSHIRO128PLUS.ulongmask), XOROSHIRO128PLUS.rotl(s1, 37)]
        return result >> 32

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

class Generator(FrameGenerator):
    def __init__(self, seed, u32seed, TID, SID, encounter = "s", flawlessiv = 0, shinyLock = 0, ability = 4, gender = 0):
        self.seed = seed
        if encounter == "s":
            r = XORSHIFT(self.seed)
            self.EC = r.next()
        elif encounter == "r":
            r = XOROSHIRO128PLUS(u32seed)
            self.EC = u32seed            
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
        self.G8TID = self.SIDTID % 1000000
