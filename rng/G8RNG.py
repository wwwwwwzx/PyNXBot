import z3
import sys,os
from enum import Enum

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
    def print(self):
        from lookups import Util
        print(f"Seed:{self.seed:016X}\tShinyType:{self.ShinyType}\tEC:{self.EC:08X}\tPID:{self.PID:08X}\tAbility:{self.Ability}\tGender:{Util.GenderSymbol[self.Gender]}\tNature:{Util.STRINGS.natures[self.Nature]}\tIVs:{self.IVs}")

class Egg(FrameGenerator):
    EVERSTONE = 229
    DESTINYKNOT = 280
    POWERITEM = 289

    @staticmethod
    def getAbilityNum(baseAbility,randroll):
        if baseAbility == 4:
            if randroll < 20:
                return 1
            if randroll < 40:
                return 2
            return 'H'
        elif baseAbility == 1:
            return 1 if randroll < 80 else 2
        elif baseAbility == 2:
            return 1 if randroll < 20 else 2

    @staticmethod
    def getPowerItem(itemID):
        if POWERITEM <= itemID and itemID <= POWERITEM + 5:
            return itemID - POWERITEM
        return -1

    def __init__(self, seed, parent1, parent2, shinycharm, tid = 0, sid = 0):
        # slow generator
        self.seed = seed
        r = XOROSHIRO(seed)

        if parent1.gender() == 0 or parent2.gender() == 1 or (parent1.species() == 132 and parent2.gender() != 0):
            Male = parent1
            Female = parent2
        else:
            Female = parent1
            Male = parent2
        base = Male if Female.species() == 132 else Female
        from lookups import Util
        parentpi = Util.PT.getFormeEntry(base.species(),base.altForm())
        self.species = parentpi.BaseSpecies()

        # Gender
        self.NidoType = False
        if base.species() in [29,32]:
            self.species = 29 if r.quickrand1(0x1) else 32
            self.NidoType = True
        if base.species() in [313,314]:
            self.species = 314 if r.quickrand1(0x1) else 313
            self.NidoType = True
        if base.species() == 490:
            self.species = 489
        self.forme = parentpi.BaseSpeciesForm()
        childpi = Util.PT.getFormeEntry(self.species,self.forme)
        self.GenderRatio = childpi.Gender()
        if self.GenderRatio == 255:
            self.Gender = 2
        elif self.GenderRatio == 254:
            self.Gender = 1
        elif self.GenderRatio == 0:
            self.Gender = 0
        else:
            self.RandomGender = True
            self.Gender = 1 if r.quickrand2(252,0xFF) + 1 < self.GenderRatio else 0

        # Nature
        self.Nature = r.quickrand2(25,0x1F)
        self.BOTH_EVERSTONE = Male.helditem() == EVERSTONE and Female.helditem() == EVERSTONE
        self.FEMALE_STONE = Female.helditem() == EVERSTONE
        self.HAS_STONE = Male.helditem() == EVERSTONE or self.FEMALE_STONE
        if self.HAS_STONE:
            self.MALE_NATURE = Male.nature()
            self.FEMALE_NATURE = Female.nature()
            if self.BOTH_EVERSTONE:
                self.Nature = self.FEMALE_NATURE if r.quickrand1(0x1) else self.MALE_NATURE
            else :
                self.Nature = self.FEMALE_NATURE if self.FEMALE_STONE else self.MALE_NATURE

        # Ability
        self.baseAbility = base.abilityNum()
        self.Ability = Egg.getAbilityNum(self.baseAbility, r.quickrand2(100,0x7F))

        # IVs
        self.InheritIVsCnt = 5 if Male.helditem() == DESTINYKNOT or Female.helditem() == DESTINYKNOT else 3

        ## Power Item
        self.InheritIVs = [-1, -1, -1, -1, -1, -1]
        self.FEMALE_POWER = Egg.getPowerItem(Female.helditem())
        self.MALE_POWER = Egg.getPowerItem(Male.helditem())
        self.BOTH_POWER = self.MALE_POWER >= 0 and self.FEMALE_POWER >= 0
        if self.BOTH_POWER:
            if r.quickrand1(0x1):
                self.InheritIVs[self.FEMALE_POWER] = 1
            else:
                self.InheritIVs[self.MALE_POWER] = 0
        elif self.MALE_POWER >= 0:
            self.InheritIVs[self.MALE_POWER] = 0
        elif self.FEMALE_POWER >= 0:
            self.InheritIVs[self.FEMALE_POWER] = 1

        ## Find Inherit IV slots
        if self.MALE_POWER >= 0 or self.FEMALE_POWER >= 0:
            self.InheritIVsCnt -= 1
        for ii in range(self.InheritIVsCnt):
            tmp = r.quickrand2(6,0x7)
            while self.InheritIVs[tmp] < -1:
                tmp = r.quickrand2(6,0x7)
            self.InheritIVs[tmp] = r.quickrand1(1)

        ## Random IV
        self.MaleIVs = Male.ivs
        self.FemaleIVs = Female.ivs
        self.IVs = [-1, -1, -1, -1, -1, -1]
        for j in range(6):
            self.IVs[j] = r.quickrand1(0x1F)
            if self.InheritIVs[j] == 0:
                self.IVs[j] = self.MaleIVs[j]
            elif self.InheritIVs[j] == 1:
                self.IVs[j] = self.FemaleIVs[j]

        # EC
        self.EC = r.nextuint()

        # PID and shiny
        self.txor = tid ^ sid
        self.ShinyType = 'None'
        reroll = 6 if Male.language() == Female.language() else 0
        self.ShinyChram = shinycharm
        if shinycharm:
            reroll += 2
        self.PID_REROLL = reroll
        for ii in range(self.PID_REROLL):
            self.PID = r.nextuint()
            self.XOR = (self.PID >> 16) ^ (self.PID & 0xFFFF) ^ self.txor
            if self.XOR < 16:
                self.ShinyType = 'Star' if self.XOR else 'Square'
                break

        # Ball
        self.ball = base.ball()
        if Male.species() == Female.species(): # Same dex number
            self.RandBall = True
            self.BASE_BALL = base.ball()
            self.MALE_BALL = Male.ball()
            if r.quickrand2(100,0x7F) >= 50:
                self.ball =  self.MALE_BALL
        if self.ball == 16 or self.ball == 1:
            self.ball = 4

    def reseed(self, seed):
        # Asssume that parents doesn't change. Quick version
        self.seed = seed
        r = XOROSHIRO(seed)

        # Gender
        if self.NidoType:
            if self.species in [29,32]:
                self.species = 29 if r.quickrand1(0x1) else 32
            if self.species in [313,314]:
                self.species = 314 if r.quickrand1(0x1) else 313
        if self.RandomGender:
            self.Gender = 1 if r.quickrand2(252,0xFF) + 1 < self.GenderRatio else 0

        # Nature
        self.Nature = r.quickrand2(25,0x1F)
        if self.HAS_STONE:
            if self.BOTH_EVERSTONE:
                self.Nature = self.FEMALE_NATURE if r.quickrand1(0x1) else self.MALE_NATURE
            else:
                self.Nature = self.FEMALE_NATURE if self.FEMALE_STONE else self.MALE_NATURE

        # Ability
        self.Ability = Egg.getAbilityNum(self.baseAbility, r.quickrand2(100,0x7F))

        # IVs
        self.InheritIVs = [-1, -1, -1, -1, -1, -1]
        if self.BOTH_POWER:
            if r.quickrand1(0x1):
                self.InheritIVs[self.FEMALE_POWER] = 1
            else:
                self.InheritIVs[self.MALE_POWER] = 0
        elif self.MALE_POWER >= 0:
            self.InheritIVs[self.MALE_POWER] = 0
        elif self.FEMALE_POWER >= 0:
            self.InheritIVs[self.FEMALE_POWER] = 1

        for ii in range(self.InheritIVsCnt):
            tmp = r.quickrand2(6,0x7)
            while self.InheritIVs[tmp] < -1:
                tmp = r.quickrand2(6,0x7)
            self.InheritIVs[tmp] = r.quickrand1(1)

        self.IVs = [-1, -1, -1, -1, -1, -1]
        for j in range(6):
            self.IVs[j] = r.quickrand1(0x1F)
            if self.InheritIVs[j] == 0:
                self.IVs[j] = self.MaleIVs[j]
            elif self.InheritIVs[j] == 1:
                self.IVs[j] = self.FemaleIVs[j]

        # EC
        self.EC = r.nextuint()

        # PID
        for ii in range(self.PID_REROLL):
            self.PID = r.nextuint()
            self.XOR = (self.PID >> 16) ^ (self.PID & 0xFFFF) ^ self.txor
            if self.XOR < 16:
                self.ShinyType = 'Star' if self.XOR else 'Square'
                break

        # Ball
        if self.RandBall:
            self.ball = self.MALE_BALL if r.quickrand2(100,0x7F) >= 50 else self.BASE_BALL
            if self.ball == 16 or self.ball == 1:
                self.ball = 4

class Raid(FrameGenerator):
    toxtricityAmpedNatures = [3, 4, 2, 8, 9, 19, 22, 11, 13, 14, 0, 6, 24]
    toxtricityLowKeyNatures = [1, 5, 7, 10, 12, 15, 16, 17, 18, 20, 21, 23]

    def __init__(self, seed, TID, SID, flawlessiv, shinylock = 0, ability = 4, gender = 0, species = 25, altform = 0):
        from lookups import Util
        pi = Util.PT.getFormeEntry(species,altform)
        self.seed = seed
        r = XOROSHIRO(seed)
        self.EC = r.nextuint()
        OTID = r.nextuint()
        self.PID = r.nextuint()
        TSV = (TID  ^ SID) >> 4

        if shinylock == 0: #random shiny chance
            FTSV = self.getShinyValue(OTID)
            PSV = self.getShinyValue(self.PID)
            if FTSV == PSV: # force shiny
                type = getShinyType(OTID,self.PID)
                if type == 1:
                    self.ShinyType = 'Star'
                else:
                    self.ShinyType = 'Square'
                if PSV != TSV:
                    highPID = (pid & 0xFFFF) ^ TID ^ SID ^ (2 - type)
                    self.PID = (highPID << 16) | (self.PID & 0xFFFF)
            else: #force non-shiny
                self.ShinyType = 'None'
                if PSV == TSV:
                    self.PID ^= 0x10000000
        elif shinylock == 1: #forced non-shiny
            self.ShinyType = 'None'
            PSV = self.getShinyValue(self.PID)
            if PSV == TSV:
                self.PID ^= 0x10000000
        else: #forced shiny
            val = (self.PID >> 16 ) ^ (self.PID & 0xFFFF) ^ TID ^ SID
            if val >= 16:
                highPID = (self.PID & 0xFFFF) ^ TID ^ SID
                self.PID = (highPID << 16) | (self.PID & 0xFFFF)
                self.ShinyType = 'Square'
            else:
                if val == 0:
                    self.ShinyType = 'Square'
                else:
                    self.ShinyType = 'Star'
                    

        i = 0
        self.IVs = [0,0,0,0,0,0]
        while i < flawlessiv:
            stat = r.quickrand2(6,0x7)
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
            else:
                self.Gender = 1 if r.quickrand2(253,0xFF) + 1 < ratio else 0
        else:
            self.Gender = gender - 1

        if species != 849:
            self.Nature = r.quickrand2(25,0x1F)
        elif altform == 0:
            self.Nature = Raid.toxtricityAmpedNatures[r.quickrand2(13,0xF)]
        else:
            self.Nature = Raid.toxtricityLowKeyNatures[r.quickrand2(12,0xF)]
    @staticmethod
    def getShinyValue(PID):
        return ((PID >> 16) ^ (PID & 0xFFFF)) >> 4

    @staticmethod
    def getShinyType(PID,OTID):
        XOR = (OTID ^ PID) >> 16
        if (XOR ^ (OTID & 0xFFFF)) == (PID & 0xFFFF):
            return 2 #'Square'
        return 1 #'Star'

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
