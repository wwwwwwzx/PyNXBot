from structure.ByteStruct import ByteStruct

class PK8(ByteStruct):
	STOREDSIZE = 0x148
	BLOCKSIZE = 0x50

	def __init__(self,buf):
		self.data = bytearray(len(buf))
		self.data[:] = buf
		if self.isEncrypted():
		 	self.decrypt()

	def ec(self):
		return self.getuint(0x0)

	def checksum(self):
		return self.getushort(0x6)

	def species(self):
		return self.getushort(0x8)

	def helditem(self):
		return self.getushort(0xA)

	def sidtid(self):
		return self.getuint(0x0C)

	def ability(self):
		return self.getushort(0x14)

	def abilityNum(self):
		return self.getbyte(0x16) & 0x7

	def canGigantamax(self):
		return (self.getbyte(0x16) & 16) != 0

	def pid(self):
		return self.getuint(0x1C)

	def nature(self):
		return self.getbyte(0x20)

	def statnature(self):
		return self.getbyte(0x21)

	def gender(self):
		return (self.getbyte(0x22) >> 2) & 0x3

	def altForm(self):
		return self.getushort(0x24)

	def evs(self):
		return [self.data[0x26],self.data[0x27],self.data[0x28],self.data[0x2A],self.data[0x2B],self.data[0x29]]

	def move1(self):
		return self.getushort(0x72)

	def move2(self):
		return self.getushort(0x74)

	def move3(self):
		return self.getushort(0x76)

	def move4(self):
		return self.getushort(0x78)

	def iv32(self):
		return self.getuint(0x8C)

	def language(self):
		return self.getbyte(0xE2)

	def ball(self):
		return self.getbyte(0x124)

	def homeTracker(self):
		return self.getulong(0x135)

	def isEgg(self):
		return ((self.iv32() >> 31) & 1) == 1

	def ivs(self):
		iv32 = self.iv32()
		return [iv32 & 0x1F, (iv32 >> 5) & 0x1F, (iv32 >> 10) & 0x1F, (iv32 >> 20) & 0x1F, (iv32 >> 25) & 0x1F, (iv32 >> 15) & 0x1F]

	def calChecksum(self):
		chk = 0
		for i in range(8,PK8.STOREDSIZE,2):
			chk += self.getushort(i)
			chk &= 0xFFFF
		return chk

	@staticmethod
	def getShinyType(otid,pid):
		xor = (otid >> 16) ^ (otid & 0xFFFF) ^ (pid >> 16) ^ (pid & 0xFFFF)
		if xor > 15:
			return 0
		else:
			return 2 if xor == 0 else 1

	def shinyType(self):
		return self.getShinyType(self.sidtid(),self.pid())

	def save(self,filename):
		with open(f'{filename}.pk8','wb') as fileOut:
			fileOut.write(self.data)

	def toString(self):
		from lookups import Util
		if self.isValid():
			shinytype = self.shinyType()
			shinyflag = '' if shinytype == 0 else '⋆' if shinytype == 1 else '◇'
			msg = f'EC: {self.ec():X} PID: {self.pid():X} ' + shinyflag
			msg += f"{' G-' if self.canGigantamax() else ''}{Util.STRINGS.species[self.species()]}{('-' + str(self.altForm())) if self.altForm() > 0 else ''}\n"
			msg += f"Nature: {Util.STRINGS.natures[self.nature()]}({Util.STRINGS.natures[self.statnature()]})\t"
			msg += f"Ability: {Util.STRINGS.abilities[self.ability()]}({self.abilityNum() if self.abilityNum() < 4 else 'H'})\t"
			msg += f"Gender: {Util.GenderSymbol[self.gender()]}\n"
			msg += f"IVs: {self.ivs()}\rEVs: {self.evs()}\n"
			msg += f"Moves: {Util.STRINGS.moves[self.move1()]} / {Util.STRINGS.moves[self.move2()]} / {Util.STRINGS.moves[self.move3()]} / {Util.STRINGS.moves[self.move4()]}\n"
			return msg
		else:
			return 'Invalid Data'

	def isValid(self):
	    return self.checksum() == self.calChecksum() and not self.isEncrypted()

	def isEncrypted(self):
		return self.getushort(0x70) != 0 and self.getushort(0xC0) != 0

	def decrypt(self):
		seed = self.ec()
		sv = (seed >> 13) & 0x1F

		# CryptPKM
		i = 8
		size = len(self.data)
		while i < size:
			seed = seed * 0x41C64E6D + 0x00006073
			self.data[i] ^= (seed >> 16) & 0xFF
			i += 1
			self.data[i] ^= (seed >> 24) & 0xFF
			i += 1

		# Shuffle Array
		idx = 4 * sv
		sdata = bytearray(PK8.STOREDSIZE)
		sdata[:] = self.data
		for block in range(4):
			ofs = PK8.BLOCKPOSITION[idx + block]
			self.data[8 + PK8.BLOCKSIZE * block : 8 + PK8.BLOCKSIZE * (block + 1)] = sdata[8 + PK8.BLOCKSIZE * ofs : 8 + PK8.BLOCKSIZE * (ofs + 1)]


	BLOCKPOSITION = [
        0, 1, 2, 3,
        0, 1, 3, 2,
        0, 2, 1, 3,
        0, 3, 1, 2,
        0, 2, 3, 1,
        0, 3, 2, 1,
        1, 0, 2, 3,
        1, 0, 3, 2,
        2, 0, 1, 3,
        3, 0, 1, 2,
        2, 0, 3, 1,
        3, 0, 2, 1,
        1, 2, 0, 3,
        1, 3, 0, 2,
        2, 1, 0, 3,
        3, 1, 0, 2,
        2, 3, 0, 1,
        3, 2, 0, 1,
        1, 2, 3, 0,
        1, 3, 2, 0,
        2, 1, 3, 0,
        3, 1, 2, 0,
        2, 3, 1, 0,
        3, 2, 1, 0,

        # duplicates of 0-7 to eliminate modulus
        0, 1, 2, 3,
        0, 1, 3, 2,
        0, 2, 1, 3,
        0, 3, 1, 2,
        0, 2, 3, 1,
        0, 3, 2, 1,
        1, 0, 2, 3,
        1, 0, 3, 2,
    ];