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
	
	def read(self,address,size,filename = None):
		self.sendCommand(f'peek 0x{address:X} 0x{size:X}')
		time.sleep(size/0x8000)
		buf = self.s.recv(2 * size + 1)
		buf = binascii.unhexlify(buf[0:-1])
		if filename is not None:
			if filename == '':
				filename = f'dump_heap_0x{address:X}_0x{size:X}.bin'
			with open(filename,'wb') as fileOut:
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

	def readEventBlock_RaidEncounter(self):
		return self.read(0x2E5E58B8,0x23D4,'normal_encount')

	def readEventBlock_CrystalEncounter(self):
		return self.read(0x2E5E7D40,0x1241C,'dai_encount')

	def readEventBlock_DropRewards(self):
		return self.read(0x2E5FA210,0x426C,'drop_rewards')

	def readEventBlock_BonusRewards(self):
		return self.read(0x2E5FE530,0x116C4,'bonus_rewards')

	def readDen(self,denID):
		denDataSize = 0x18;
		if denID > SWSHBot.DENCOUNT - 1:
			denID = SWSHBot.DENCOUNT - 1
		address = 0x4298FA80 + denID * denDataSize
		return self.read(address,denDataSize)