from nxbot import SWSHBot

class RaidBot(SWSHBot):
	
	def __init__(self,ip,port = 6000):
		SWSHBot.__init__(self,ip,port)
		from structure import Den,EncounterNest8Archive, NestHoleDistributionEncounter8Archive
		buf = bytearray(open('../resources/bytes/local_raid','rb').read())
		Den.LOCALTABLE = EncounterNest8Archive.GetRootAsEncounterNest8Archive(buf,0)
		buf = self.readEventBlock_RaidEncounter('Event/Current/')
		Den.EVENTTABLE = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf,0x20)