from structure.ByteStruct import ByteStruct
from enum import Enum

class GameVersion(Enum):
	SWSH = 0

class PersonalInfo(ByteStruct):
	SIZE = 0x0
	def __init__(self,buf):
		self.data = bytearray(PersonalInfo.SIZE)
		self.data[:] = buf

	def FormStatsIndex(self):
		return 0

	def FormeCount(self):
		return 0

	def FormeIndex(self,species,forme):
		if forme <= 0:
			return species
		if self.FormStatsIndex() <= 0:
			return species
		if forme >= self.FormeCount():
			return species
		return self.FormStatsIndex() + forme - 1

class PersonalInfoSWSH(PersonalInfo):
	SIZE = 0xA8

	def __init__(self,buf):
		self.data = bytearray(PersonalInfoSWSH.SIZE)
		self.data[:] = buf

	def Type1(self):
		return self.getbyte(0x06)

	def Type2(self):
		return self.getbyte(0x07)

	def Ability1(self):
		return self.getushort(0x18)

	def Ability2(self):
		return self.getushort(0x1A)

	def AbilityH(self):
		return self.getushort(0x1C)

	def FormStatsIndex(self):
		return self.getushort(0x1E)

	def FormeCount(self):
		return self.getbyte(0x20)

class PersonalTable(object):
	def __init__(self,buf,ver = GameVersion.SWSH):
		length = len(buf)
		self.table = []
		if ver == GameVersion.SWSH:
			size = PersonalInfoSWSH.SIZE
			for ind in range(0,length,size):
				self.table.append(PersonalInfoSWSH(buf[ind:ind + size]))

	def getFormeIndex(self, species, forme):
		if species >= len(self.table):
			species = 0
		return self.table[species].FormeIndex(species,forme)

	def getFormeEntry(self, species, forme):
		return self.table[self.getFormeIndex(species,forme)]