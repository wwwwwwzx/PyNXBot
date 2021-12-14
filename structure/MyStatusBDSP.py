from structure.ByteStruct import ByteStruct

class MyStatusBDSP(ByteStruct):
	def TID(self):
		return self.getushort(0x0)

	def SID(self):
		return self.getushort(0x2)

	def TSV(self):
		return (self.TID() ^ self.SID()) >> 4

	def displayID(self):
		return ((((self.SID()) << 16) | self.TID()) & 0xFFFFFFFF) % 1000000

	def Money(self):
		return self.getuint(0x4)
