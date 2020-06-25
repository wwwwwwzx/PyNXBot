from nxbot import SWSHBot
from structure import Den
from time import sleep

class RaidBot(SWSHBot):
        
        def __init__(self,ip,port = 6000):
                SWSHBot.__init__(self,ip,port)
                from structure import EncounterNest8Archive, NestHoleDistributionEncounter8Archive
                buf = bytearray(open('../resources/bytes/local_raid','rb').read())
                Den.LOCALTABLE = EncounterNest8Archive.GetRootAsEncounterNest8Archive(buf,0)
                buf = self.readEventBlock_RaidEncounter('Event/Current/')
                Den.EVENTTABLE = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf,0x20)

        def setTargetDen(self, denId):
                self.denID = denId - 1

        def getDenData(self):
                return Den(self.readDen(self.denID))

        def closeGame(self):
                c = input("Close the game? (y/n): ")
                if c == 'y' or c == 'Y':
                        h = input("Need HOME button pressing? (y/n): ")
                        if h == 'y' or h == 'Y':
                                need_home = True
                        else:
                                need_home = False
                        print("Closing game...")
                        self.quit_app(need_home)
                print("Exiting...")
                sleep(0.5)
                self.close()
                        
        def skipAnimation(self, luxray = False):
                self.enter_app()
                sleep(19.5)
                if luxray:
                        sleep(1.3)
                print("Skip animation")
                self.click("A") #A to skip anim
                sleep(0.5)
                self.click("A")
                sleep(0.5)
                self.click("A")
                sleep(8)

        def saveGame(self):
                print("Saving...")
                self.click("X")
                sleep(1.2)
                self.click("R")
                sleep(1.5)
                self.click("A")
                sleep(4)

        def getWatts(self):
                self.click("A")
                sleep(1.5)
                self.click("A")
                sleep(1.2)
                self.click("A")
                sleep(1.2)
                self.saveGame()

        def throwPiece(self):
                self.click("A") #A on den
                print("A on den")
                sleep(0.5)
                self.click("A")
                sleep(1.3)
                self.click("A") #A to throw whishing piece
                print("Throw Wishing Piece in den")
                sleep(1.4)
                self.click("A") #A to save
                print("Saving...")
                sleep(1)
                self.click("HOME") #Home
                print("HOME clicked")
                sleep(0.5)
                
