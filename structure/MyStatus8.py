from structure.ByteStruct import ByteStruct

class MyStatus8(ByteStruct):

	def TID(self):
		return self.getushort(0xA0)

	def SID(self):
		return self.getushort(0xA2)

	def TSV(self):
		return (self.TID() ^ self.SID()) >> 4

	def displayID(self):
		return self.getuint(0xA0) % 1000000

	def Game(self):
		return self.getbyte(0xA4)

	def Language(self):
		return self.getbyte(0xA7)

	def getLangName(self):
                langNames = {1:'Japanese', 2:'English', 3:'French', 4:'Italian', 5:'German', 7:'Spanish', 8:'Korean', 9:'Simpl. Chinese', 10:'Tradit. Chinese'}
                return langNames[self.Language()]

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

	def Watt(self):
		return self.getCustomInt(0xD0,0x3)

	def Money(self):
		return self.getCustomInt(0x110,0x3)
