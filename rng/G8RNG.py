import z3
import sys,os
from enum import Enum
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from lookups import PKMString

class XOROSHIRO(object):
    ulongmask = 2 ** 64 - 1
    uintmask = 2 ** 32 - 1

    def __init__(self, seed, seed2 = 0x82A2B175229D6A5B):
            self.seed = [seed, seed2]

    def state(self):
        s0, s1 = self.seed
        return s0 | (s1 << 64)

    @staticmethod
    def rotl(x, k):
        return ((x << k) | (x >> (64 - k))) & XOROSHIRO.ulongmask

    def next(self):
        s0, s1 = self.seed
        result = (s0 + s1) & XOROSHIRO.ulongmask
        s1 ^= s0
        self.seed = [XOROSHIRO.rotl(s0, 24) ^ s1 ^ ((s1 << 16) & XOROSHIRO.ulongmask), XOROSHIRO.rotl(s1, 37)]
        return result

    def nextuint(self):
        return self.next() & XOROSHIRO.uintmask

    @staticmethod
    def getMask(x):
        x -= 1
        for i in range(6):
            x |= x >> (1 << i)
        return x
    
    def rand(self, N = uintmask):
        mask = XOROSHIRO.getMask(N)
        res = self.next() & mask
        while res >= N:
            res = self.next() & mask
        return res

    def quickrand1(self,mask): # 0~mask rand(mask + 1)
        return self.next() & mask

    def quickrand2(self,max,mask): # 0~max-1 rand(max)
        res = self.next() & mask
        while res >= max:
            res = self.next() & mask
        return res

    @staticmethod
    def find_seeds(ec,pid):
        solver = z3.Solver()
        start_s0 = z3.BitVecs('start_s0', 64)[0]

        sym_s0 = start_s0
        sym_s1 = 0x82A2B175229D6A5B

        # EC call
        result = ec
        sym_s0, sym_s1, condition = sym_xoroshiro128plus(sym_s0, sym_s1, result)
        solver.add(condition)

        # Blank call
        sym_s0, sym_s1 = sym_xoroshiro128plusadvance(sym_s0, sym_s1)

        # PID call
        result = pid
        sym_s0, sym_s1, condition = sym_xoroshiro128plus(sym_s0, sym_s1, result)
        solver.add(condition)
        
        models = get_models(solver)
        return [ model[start_s0].as_long() for model in models ]

class FrameGenerator(object):
    GenderSymbol = ['♂','♀','-']
    from structure import PersonalTable
    PT = PersonalTable(bytearray(open('../resources/bytes/personal_swsh','rb').read()))
    pmstring = PKMString()

class Egg(FrameGenerator):
    pass

class Raid(FrameGenerator):
    toxtricityAmpedNatures = [3, 4, 2, 8, 9, 19, 22, 11, 13, 14, 0, 6, 24]
    toxtricityLowKeyNatures = [1, 5, 7, 10, 12, 15, 16, 17, 18, 20, 21, 23]

    def __init__(self,seed,flawlessiv, ability = 4, gender = 0, species = 25, altform = 0):
        pi = FrameGenerator.PT.getFormeEntry(species,altform)
        self.seed = seed
        r = XOROSHIRO(seed)
        self.EC = r.nextuint()
        OTID = r.nextuint()
        self.PID = r.nextuint()

        self.XOR = (self.PID >> 16) ^ (self.PID & 0xFFFF) ^ (OTID >> 16) ^ (OTID & 0xFFFF)
        if self.XOR >= 16:
            self.ShinyType = 'None'
        else:
            self.ShinyType = 'Star' if self.XOR else 'Square'

        i = 0
        self.IVs = [0,0,0,0,0,0]
        while i < flawlessiv:
            stat = r.rand(6)
            if self.IVs[stat] == 0:
                self.IVs[stat] = 31
                i += 1
        for i in range(6):
            if self.IVs[i] == 0:
                self.IVs[i] = r.quickrand1(0x1F)

        if ability == 4:
            self.Ability = r.quickrand2(3,3) + 1
        elif ability == 3:
            self.Ability = r.quickrand1(0x1) + 1
        else:
            self.Ability = ability + 1
        if self.Ability == 3:
            self.Ability = 'H'

        if gender == 0:
            ratio = pi.Gender()
            if ratio == 255:
                self.Gender = 2
            elif ratio == 254:
                self.Gender = 1
            elif ratio == 0:
                self.Gender = 0
            self.Gender = 1 if r.quickrand2(253,0xFF) + 1 < ratio else 0

        if species != 849:
            self.Nature = r.quickrand2(25,0x1F)
        elif altform == 0:
            self.Nature = Raid.toxtricityAmpedNatures[r.quickrand2(13,0xF)]
        else:
            self.Nature = Raid.toxtricityLowKeyNatures[r.quickrand2(12,0xF)]

    def print(self):
        print(f"Seed:{self.seed:016X}\tShinyType:{self.ShinyType}\tEC:{self.EC:08X}\tPID:{self.PID:08X}\tAbility:{self.Ability}\tGender:{FrameGenerator.GenderSymbol[self.Gender]}\tNature:{FrameGenerator.pmstring.natures[self.Nature]}\tIVs:{self.IVs}")

    @staticmethod
    def getNextShinyFrame(seed):
        for ii in range(99999):
            r = XOROSHIRO(seed)
            seed = r.next()
            OTID = r.nextuint()
            PID = r.nextuint()
            XOR = (PID >> 16) ^ (PID & 0xFFFF) ^ (OTID >> 16) ^ (OTID & 0xFFFF)
            if XOR < 16:
                return ii

    @staticmethod
    def getseeds(EC,PID,IVs):
        result = []
        seeds = XOROSHIRO.find_seeds(EC, PID)    
        if len(seeds) > 0:
            for iv_count in range(IVs.count(31) + 1):
                for seed in seeds:
                    r = Raid(seed,iv_count)
                    if IVs == r.IVs:
                        result.append([seed,iv_count])

        if len(result) > 0:
            return result

        seedsXor = XOROSHIRO.find_seeds(EC, PID ^ 0x10000000) # Check for shiny lock
        if len(seedsXor) > 0:
            for iv_count in range(IVs.count(31) + 1):
                for seed in seeds:
                    r = Raid(seed,iv_count)
                    if IVs == r.IVs:
                        result.append([seed,-iv_count])
        return result

def sym_xoroshiro128plus(sym_s0, sym_s1, result):
    sym_r = (sym_s0 + sym_s1) & 0xFFFFFFFFFFFFFFFF  
    condition = (sym_r & 0xFFFFFFFF) == result

    sym_s0, sym_s1 = sym_xoroshiro128plusadvance(sym_s0, sym_s1)

    return sym_s0, sym_s1, condition

def sym_xoroshiro128plusadvance(sym_s0, sym_s1):
    s0 = sym_s0
    s1 = sym_s1
    
    s1 ^= s0
    sym_s0 = z3.RotateLeft(s0, 24) ^ s1 ^ (s1 << 16)
    sym_s1 = z3.RotateLeft(s1, 37)

    return sym_s0, sym_s1

def get_models(s):
    result = []
    while s.check() == z3.sat:
        m = s.model()
        result.append(m)
        
        # Constraint that makes current answer invalid
        d = m[0]
        c = d()
        s.add(c != m[d])

    return result