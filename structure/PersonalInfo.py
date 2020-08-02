from structure.ByteStruct import ByteStruct
from enum import Enum

class GameVersion(Enum):
	SWSH = 0

class PersonalInfo(ByteStruct):

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
	SIZE = 0xB0

	def __init__(self,buf):
		self.data = bytearray(PersonalInfoSWSH.SIZE)
		self.data[:] = buf

	def Type1(self):
		return self.getbyte(0x06)

	def Type2(self):
		return self.getbyte(0x07)

	def Gender(self):
		return self.getbyte(0x12)

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

	def BaseSpecies(self):
		return self.getushort(0x56)

	def BaseSpeciesForm(self):
		return self.getushort(0x58)

class PersonalTable(object):
	Galarlist = [52,77,78,79,80,83,110,122,144,145,146,199,222,263,264,554,555,562,618]
	Alolalist = [19,20,26,27,28,37,38,50,51,52,53,74,75,76,88,89,103,105]
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

	def getFormeNameIndex(self, species, forme):
		if species == 678 or species == 876:
			return 1004 if forme else 678
		if species in self.Alolalist and forme <= 1: # Skip Galarian Meowth
			return 810 if forme else 1
		if species in self.Galarlist:
			return 1068 if forme else 1
		if forme == 0:
			return species
		if species == 849 and forme == 1:
			return 1072
		if species == 869:
			return 1072 + forme
		if species == 479:
			return 916 + forme
		if species in [422,423]:
			return 911
		return -1
