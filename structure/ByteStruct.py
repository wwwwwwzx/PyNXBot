class ByteStruct(object):

	def __init__(self,buf):
		self.data = bytearray(len(buf))
		self.data[:] = buf

	def getulong(self,offset):
		return int.from_bytes(self.data[offset:offset + 8], byteorder='little') 

	def getuint(self,offset):
		return int.from_bytes(self.data[offset:offset + 4], byteorder='little')

	def getushort(self,offset):
		return int.from_bytes(self.data[offset:offset + 2], byteorder='little')

	def getbyte(self,offset):
		return self.data[offset]

	def getstring(self,offset,size):
		return self.data[offset:offset+size].decode("utf-16").rstrip('\x00')

	def setushort(self,offset,p):
		self.data[offset:offset + 2] = (p).to_bytes(2, byteorder='little')