import socket
import binascii
from time import sleep
from enum import Enum

class SystemLanguage(Enum):
        JA = 0
        ENUS = 1
        FR = 2
        DE = 3
        IT = 4
        ES = 5
        ZHCN = 6
        KO = 7
        NL = 8
        PT = 9
        ZHTW = 11
        ENGB = 12
        FRCA = 13
        ES419 = 14
        ZHHANS = 15
        ZHHANT = 16

class NXBot(object):
        def __init__(self,ip,port = 6000):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((ip, port))
                print('Bot Connected')
                self.configure()

        def configure(self):
                self.sendCommand('configure echoCommands 0')

        def sendCommand(self,content):
                content += '\r\n' #important for the parser on the switch side
                self.s.sendall(content.encode())

        def detach(self):
                self.sendCommand('detachController')

        def close(self):
                self.detach()
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                print('Bot Disconnected')

        # A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
        def click(self,button):
                self.sendCommand('click '+ button)

        def press(self,button):
                self.sendCommand('press '+ button)

        def release(self,button):
                self.sendCommand('release '+ button)
        
        def read(self,address,size,filename = None):
                self.sendCommand(f'peek 0x{address:X} 0x{size:X}')
                sleep(size/0x8000)
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

        def getSystemLanguage(self):
                self.sendCommand('getSystemLanguage')
                sleep(0.005)
                buf = self.s.recv(4)
                return SystemLanguage(int(buf[0:-1]))

        def pause(self,duration):
                sleep(duration)

class SWSHBot(NXBot):
        PK8STOREDSIZE = 0x148
        PK8PARTYSIZE = 0x158
        DENCOUNT = 191

        def __init__(self,ip,port = 6000):
                NXBot.__init__(self,ip,port)
                from structure import MyStatus8
                self.TrainerSave = MyStatus8(self.readTrainerBlock())
                self.eventoffset = 0
                if self.TrainerSave.isPokemonSave():
                        print(f"Game:{self.TrainerSave.GameVersion()} OT: {self.TrainerSave.OT()} ID:{self.TrainerSave.displayID()}\n")
                        self.isPlayingSword = self.TrainerSave.isSword()
                        self.getEventOffset(self.getSystemLanguage())
                        self.TID = self.TrainerSave.TID()
                        self.SID = self.TrainerSave.SID()
        
        def getEventOffset(self, language = SystemLanguage.ENUS):
                if language == SystemLanguage.ZHCN or language == SystemLanguage.ZHHANS:
                        self.eventoffset = -0xE00
                elif language == SystemLanguage.ZHTW or language == SystemLanguage.ZHHANT:
                        self.eventoffset = -0xE60
                elif language == SystemLanguage.KO:
                        self.eventoffset = -0xA00
                elif language == SystemLanguage.IT:
                        self.eventoffset = -0x80
                elif language == SystemLanguage.JA:
                        self.eventoffset = +0x160
                elif language == SystemLanguage.FR or language == SystemLanguage.FRCA:
                        self.eventoffset = +0x1F0
                elif language == SystemLanguage.ES or language == SystemLanguage.ES419:
                        self.eventoffset = +0x1C0
                elif language == SystemLanguage.DE:
                        self.eventoffset = +0x2D0 
                else: # English
                        pass
                return self.eventoffset

        def readTrainerBlock(self):
                return self.read(0x45061108, 0x110)

        def readParty(self,slot=1):
                if slot > 6:
                        slot = 6
                address = 0x450BE8C0 + (slot - 1) * self.PK8PARTYSIZE
                return self.read(address,self.PK8STOREDSIZE)

        def readBox(self,box = 0,slot = 0):
                if box > 31:
                        box = 31
                if slot > 29:
                        slot = 29
                address = 0x4506D890 + box * 30 + slot * self.PK8PARTYSIZE
                return self.read(address,self.PK8STOREDSIZE)

        def readTrade(self):
                return self.read(0xAF285F68,self.PK8STOREDSIZE)

        def readWild(self):
                return self.read(0x8FEA3358,self.PK8STOREDSIZE)

        def readRaid(self):
                return self.read(0x886C1BD8,self.PK8STOREDSIZE)

        def readLegend(self):
                return self.read(0x886BC058,self.PK8STOREDSIZE)

        def readEventBlock_RaidEncounter(self,path=''):
                return self.read(0x2F9EB1F0 + self.eventoffset, 0x23D4, path + 'normal_encount')

        def readEventBlock_CrystalEncounter(self,path=''):
                return self.read(0x2F9ED678 + self.eventoffset, 0x1241C, path + 'dai_encount')

        def readEventBlock_DropRewards(self,path=''):
                return self.read(0x2F9FFB48 + self.eventoffset, 0x426C, path + 'drop_rewards')

        def readEventBlock_BonusRewards(self,path=''):
                return self.read(0x2FA03E68 + self.eventoffset, 0x116C4, path + 'bonus_rewards')

        def readDen(self,denID):
                denDataSize = 0x18;
                if denID > SWSHBot.DENCOUNT - 1:
                        denID = SWSHBot.DENCOUNT - 1
                address = 0x450C0A80 + denID * denDataSize
                return self.read(address,denDataSize)

        def readScreenOff(self):
                return self.read(0x6B30F9E0, 8)

        def readOverworldCheck(self):
                return self.read(0x2F770528 + self.eventoffset, 4)

        def readBattleStart(self):
                return self.read(0x69B99418, 8)
