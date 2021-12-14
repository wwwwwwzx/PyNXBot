from structure.ByteStruct import ByteStruct

class BDSPEgg(ByteStruct):
    SIZE = 0x10
    def __init__(self,buf):
        self.data = bytearray(BDSPEgg.SIZE)
        self.data[:] = buf

    def flag(self):
        return self.getbyte(0x0)

    def seed(self):
        return self.getuint(0x8)

    def steps(self):
        return self.getbyte(0x10)
