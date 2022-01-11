from structure.ByteStruct import ByteStruct
from rng import Generator

class BDSPRoamer(ByteStruct):
        def __init__(self,buf,TID,SID):
                self.data = bytearray(buf[:])
                self.TID = TID
                self.SID = SID

        def ec(self, index):
                return self.getuint((0x20 * index) + 0x4)

        def species(self, index):
                return self.getushort((0x20 * index) + 0xC)

        def hp(self, index):
                return self.getbyte((0x20 * index) + 0x14)

        def toString(self):
                from lookups import Util
                for i in range(2):
                        r = Generator(0, self.ec(i), self.TID, self.SID, "r", 3)
                        print(f'Species: {Util.STRINGS.species[self.species(i)]}\tHP: {self.hp(i)}')
                        r.print()
                        print()
