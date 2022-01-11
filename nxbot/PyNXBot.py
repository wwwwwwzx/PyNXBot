import sys
import socket
import binascii
from time import sleep
from enum import Enum
from structure import Screen

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
        self.s.settimeout(1)
        self.s.connect((ip, port))
        print('Bot Connected')
        self.configure()
        self.moveLeftStick(0,0)
        self.moveRightStick(0,0)
        self.resets = 0

    def configure(self):
        self.sendCommand('configure echoCommands 0')

    def sendCommand(self,content):
        content += '\r\n' #important for the parser on the switch side
        self.s.sendall(content.encode())

    def detach(self):
        self.sendCommand('detachController')

    def close(self,exitapp = True):
        print("Exiting...")
        self.pause(0.5)
        self.detach()
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        print('Bot Disconnected')
        if exitapp:
            sys.exit(0)

    # A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
    def click(self,button):
        self.sendCommand('click '+ button)

    def press(self,button):
        self.sendCommand('press '+ button)

    def release(self,button):
        self.sendCommand('release '+ button)

    # setStick LEFT/RIGHT <xVal from -0x8000 to 0x7FFF> <yVal from -0x8000 to 0x7FFF
    def moveStick(self,button,x,y):
        self.sendCommand('setStick ' + button + ' ' + hex(x) + ' ' + hex(y))

    def moveLeftStick(self,x = None, y = None):
        if x is not None:
            self.ls_lastx = x
        if y is not None:
            self.ls_lasty = y
        self.moveStick('LEFT',self.ls_lastx,self.ls_lasty)

    def moveRightStick(self,x = None, y = None):
        if x is not None:
            self.rs_lastx = x
        if y is not None:
            self.rs_lasty = y
        self.moveStick('RIGHT',self.rs_lastx,self.rs_lasty)

    #peek <address in hex, prefaced by 0x> <amount of bytes, dec or hex with 0x>
    #poke <address in hex, prefaced by 0x> <data, if in hex prefaced with 0x>       
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
        self.sendCommand(f'poke 0x{address:X} 0x{data}')

    def read_pointer(self,pointer,size,filename = None):
        jumps = pointer.replace("[","").replace("main","").split("]")
        self.sendCommand(f'pointerPeek 0x{size:X} 0x{" 0x".join(jump.replace("+","") for jump in jumps)}')
        sleep(size/0x8000)
        buf = self.s.recv(2 * size + 1)
        buf = binascii.unhexlify(buf[0:-1])
        if filename is not None:
            if filename == '':
                filename = f'dump_heap_{pointer}_0x{size:X}.bin'
            with open(filename,'wb') as fileOut:
                fileOut.write(buf)
        return buf

    def getSystemLanguage(self):
        self.sendCommand('getSystemLanguage')
        sleep(0.005)
        buf = self.s.recv(4)
        return SystemLanguage(int(buf[0:-1]))

    def pause(self,duration):
        sleep(duration)

    def increaseResets(self):
        self.resets += 1

    def quitGame(self,needHome=True):
        if needHome:
            self.click("HOME")
            self.pause(0.8)
        self.click("X")
        self.pause(0.2)
        self.click("X")
        self.pause(0.4)
        self.click("A")
        self.pause(0.2)
        self.click("A")
        self.pause(1.3)

    def enterGame(self):
        print("\nStarting the game")
        self.click("A")
        self.pause(0.2)
        self.click("A")
        self.pause(1.3)
        self.click("A")
        self.pause(0.2)
        self.click("A")

    def skipIntroAnimation(self): #luxray = False
        skip = False
        self.pause(14.7)
        while skip is not True:
            self.pause(0.3)
            currScreen = Screen(self.readScreenOff())
            if currScreen.isIntroAnimationSkippable():
                skip = True
            else:
                self.click("A")
        #self.pause(20.5)
        #currScreen.isIntroAnimationSkippable()
        #if luxray:
            #self.pause(1.3)
        print("Skip animation")
        for i in range(10):
            self.click("A") #A to skip anim
            self.pause(0.5)
        #self.pause(8)
        skipped = False
        while skipped is not True:
            currScreen = Screen(self.readOverworldCheck())
            if currScreen.overworldCheck():
                skipped = True
            self.pause(0.5)

    def saveGame(self):
        print("Saving...")
        self.click("X")
        self.pause(1.2)
        self.click("R")
        self.pause(1.5)
        self.click("A")
        self.pause(4)

    def closeGame(self):
        c = input("Close the game? (y/n): ")
        if c == 'y' or c == 'Y':
            h = input("Need HOME button pressing? (y/n): ")
            if h == 'y' or h == 'Y':
                needHome = True
            else:
                needHome = False
            print("Closing game...")
            self.quitGame(needHome)
        print()
        self.close()

    def foundActions(self):
        print("Found after", self.resets, "resets")
        print()
        a = input("Continue searching? (y/n): ")
        if a != "y" and a != "Y":
            self.closeGame()
        else:
            self.increaseResets()
            print("Resets:", self.resets)

    def notfoundActions(self,i=0,bot='raid'):
        if i == 0 and bot == 'raid':
            print("Research skipped")
        self.increaseResets()
        if bot == 'raid':
            print("Nothing found - Resets:", self.resets)
        else:
            print("Wrong Species/Stars - Resets:", self.resets)

class SWSHBot(NXBot):
    PK8STOREDSIZE = 0x148
    PK8PARTYSIZE = 0x158
    DENCOUNT = 276

    def __init__(self,ip,port = 6000):
        NXBot.__init__(self,ip,port)
        from structure import MyStatus8
        self.TrainerSave = MyStatus8(self.readTrainerBlock())
        self.eventoffset = 0
        if self.TrainerSave.isPokemonSave():
            print(f"Game: {self.TrainerSave.GameVersion()}    OT: {self.TrainerSave.OT()}    ID: {self.TrainerSave.displayID()}\n")
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
        return self.read(0x45068F18, 0x110) + self.read(0x45072DF4, 0x3)

    def readParty(self,slot=1):
        if slot > 6:
            slot = 6
        address = 0x450C68B0 + (slot - 1) * self.PK8PARTYSIZE
        return self.read(address,self.PK8PARTYSIZE)

    def readBox(self,box = 1,slot = 1):
        if box > 31:
            box = 31
        if slot > 29:
            slot = 29
        address = 0x45075880 + ((box - 1) * 30 * self.PK8PARTYSIZE) + ((slot - 1) * self.PK8PARTYSIZE)
        return self.read(address,self.PK8PARTYSIZE)

    def readTrade(self):
        return self.read(0xAF286078,self.PK8STOREDSIZE)

    def readWild(self):
        return self.read(0x8FEA3648,self.PK8STOREDSIZE)

    def readRaid(self):
        return self.read(0x886C1EC8,self.PK8STOREDSIZE)

    def readLegend(self):
        return self.read(0x886BC348,self.PK8STOREDSIZE)

    def readEventBlock_RaidEncounter(self,path=''):
        return self.read(0x2F9EB300 + self.eventoffset, 0x23D4, path + 'normal_encount')

    def readEventBlock_CrystalEncounter(self,path=''):
        return self.read(0x2F9ED788 + self.eventoffset, 0x1241C, path + 'dai_encount')

    def readEventBlock_DropRewards(self,path=''):
        return self.read(0x2F9FFC58 + self.eventoffset, 0x426C, path + 'drop_rewards')

    def readEventBlock_BonusRewards(self,path=''):
        return self.read(0x2FA03F78 + self.eventoffset, 0x116C4, path + 'bonus_rewards')

    def readEventBlock_RaidEncounter_IoA(self,path=''):
        return self.read(0x2FA156F0 + self.eventoffset, 0x23D4, path + 'normal_encount_rigel1')

    def readEventBlock_RaidEncounter_CT(self,path=''):
        return self.read(0x2FA17B78 + self.eventoffset, 0x23D4, path + 'normal_encount_rigel2')

    def readDen(self,denID):
        denDataSize = 0x18;
        if denID > SWSHBot.DENCOUNT + 31:
            denID = SWSHBot.DENCOUNT + 31
        address = 0x450C8A70 + denID * denDataSize
        return self.read(address,denDataSize)

    def readScreenOff(self):
        return self.read(0x6B30FA00, 8)

    def readOverworldCheck(self):
        return self.read(0x2F770638 + self.eventoffset, 4)

    def readBattleStart(self):
        return self.read(0x6B578EDC, 8)

class BDSPBot(NXBot):
    PK8STOREDSIZE = 0x148

    def __init__(self,ip,port = 6000):
        NXBot.__init__(self,ip,port)
        from structure import MyStatusBDSP
        self.TrainerSave = MyStatusBDSP(self.readTrainerBlock())
        print(f"G8TID: {self.TrainerSave.displayID()}    TID: {self.TrainerSave.TID()}    SID: {self.TrainerSave.SID()}\n")
        self.TID = self.TrainerSave.TID()
        self.SID = self.TrainerSave.SID()

    def getSeed(self):
        seed = self.read_pointer("[main+4FB2050]",16)
        s0 = int.from_bytes(seed[:4], "little")
        s1 = int.from_bytes(seed[4:8], "little")
        s2 = int.from_bytes(seed[8:12], "little")
        s3 = int.from_bytes(seed[12:], "little")
        return [s0, s1, s2, s3]

    def readTrainerBlock(self):
        trainerBlockPointer = "[[[[[[main+4E853F0]+18]+C0]+28]+B8]]+E8"
        return self.read_pointer(trainerBlockPointer, 8)
