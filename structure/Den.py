from structure.ByteStruct import ByteStruct
from enum import Enum

class DenType(Enum):
	EMPTY = 0
	COMMON = 1
	RARE = 2
	COMMON_WISH = 3
	RARE_WISH = 4
	EVENT = 5


class Den(ByteStruct):
	SIZE = 0x18

	def __init__(self,buf):
		self.data = bytearray(Den.SIZE)
		self.data[:] = buf

	def hash(self):
		return self.getulong(0x0)

	def seed(self):
		return self.getulong(0x8)

	def stars(self):
		return self.getbyte(0x10) + 1

	def randroll(self):
		return self.getbyte(0x11)

	def denType(self):
		return DenType(self.getbyte(0x12))

	def flagByte(self):
		return self.getbyte(0x13)

	def isActive(self):
		return self.denType() != DenType.EMPTY

	def isRare(self):
		return self.denType() == DenType.RARE or self.denType() == DenType.RARE_WISH

	def isWishingPiece(self):
		return self.denType() == DenType.COMMON_WISH or self.denType() == DenType.RARE_WISH

	def isEvent(self):
		return (self.flagByte() & 2) == 1
