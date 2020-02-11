import socket
import time
import binascii

class NXBot(object):
	def __init__(self,ip,port = 6000):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((ip, port))
		print('Bot Connected')

	def sendCommand(self,content):
		content += '\r\n' #important for the parser on the switch side
		self.s.sendall(content.encode())

	def close(self):
		self.s.shutdown(socket.SHUT_RDWR)
		self.s.close()
		print('Bot Disconnected')

	def click(self,button):
		self.sendCommand('click '+ button)

	def press(self,button):
		self.sendCommand('press '+ button)

	def release(self,button):
		self.sendCommand('release '+ button)
	
	def read(self,address,size,save2file = False):
		self.sendCommand(f'peek 0x{address:X} 0x{size:X}')
		time.sleep(0.05)
		buf = self.s.recv(2 * size + 1)
		buf = binascii.unhexlify(buf[0:-1])
		if save2file:
			with open(f'dump_heap_0x{address:X}_0x{size:X}.bin','wb') as fileOut:
				fileOut.write(buf)
		return buf

	def write(self,address,data):
		self.sendCommand(f'poke 0x{address:X} {data}')

class SWSHBot(NXBot):
	PK8STOREDSIZE = 0x148
	PK8PARTYSIZE = 0x158
	DENCOUNT = 111

	def readParty(self,slot=0):
		if slot > 5:
			slot = 5
		address = 0x4298E8E0 + slot * self.PK8PARTYSIZE
		return self.read(address,self.PK8STOREDSIZE)

	def readBox(self,box = 0,slot = 0):
		if box > 31:
			box = 31
		if slot > 29:
			slot = 29
		address = 0x4293D8B0 + box * 30 + slot * self.PK8PARTYSIZE
		return self.read(address,self.PK8STOREDSIZE)

	def readWild(self):
		return self.read(0x8D45C648,self.PK8STOREDSIZE)

	def readRaid(self):
		return self.read(0x85C7AB08,self.PK8STOREDSIZE)

	def readLegend(self):
		return self.read(0x85C74F88,self.PK8STOREDSIZE)

	def readEventBlock(self):
		return self.read(0x2E5E58B8,0x23D4,True)

	def readDen(self,denID):
		denDataSize = 0x18;
		if denID > SWSHBot.DENCOUNT - 1:
			denID = SWSHBot.DENCOUNT - 1
		address = 0x4298FA80 + denID * denDataSize
		return self.read(address,denDataSize)