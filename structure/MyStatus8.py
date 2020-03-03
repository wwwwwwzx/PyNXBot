from structure.ByteStruct import ByteStruct

class MyStatus8(ByteStruct):

	def TID(self):
		return self.getushort(0xA0)

	def SID(self):
		return self.getushort(0xA2)

	def displayID(self):
		return self.getuint(0xA0) % 1000000

	def Game(self):
		return self.getbyte(0xA4)

	def Language(self):
		return self.getbyte(0xA7)

	def isSword(self):
		return self.Game() == 44

	def isPokemonSave(self):
		return self.Game() == 44 or self.Game() == 45

	def GameVersion(self):
		if self.Game() == 44:
			return "Sword"
		if self.Game() == 45:
			return "Shield"

	def OT(self):
		return self.getstring(0xB0,0x1A)