# Settings
IP = '192.168.0.10'
language = 'ENUS' # to be read
ReadEventFromConsole = True
DumpPath = 'Event/Current/'
LocalPath = 'Event/Index 12/'

# Desired IVs
V6 = [31,31,31,31,31,31]
S0 = [31,31,31,31,31,00]
A0 = [31,00,31,31,31,31]
usefilters = True
MaxResults = 10000

# Go to root of PyNXBot
import sys
sys.path.append('../')

from lookups import PKMString
from structure import Den
from structure import EncounterNest8Archive, NestHoleDistributionEncounter8Archive
from nxbot import SWSHBot
from rng import XOROSHIRO,Raid

pmtext = PKMString()
buf = bytearray(open('../resources/bytes/local_raid','rb').read())
Den.LOCALTABLE = EncounterNest8Archive.GetRootAsEncounterNest8Archive(buf,0)
b = SWSHBot(IP)
b.getEventOffset(language)
if ReadEventFromConsole:
	buf = b.readEventBlock_RaidEncounter(DumpPath)
else:
	buf = bytearray(open(LocalPath + 'normal_encount','rb').read())
Den.EVENTTABLE = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf,0x20)
seed = None
for ii in range(SWSHBot.DENCOUNT):
	den = Den(b.readDen(ii))
	if den.isActive():
		spawn = den.getSpawn(denID = ii, isSword = b.isPlayingSword)
		info = f"denID {ii}:0x{den.seed():X}\t{den.stars()}★\tSpecies: {pmtext.species[spawn.Species()]}\tShiny Frame: {Raid.getNextShinyFrame(den.seed())}\t"
		if den.isEvent():
			info += "Event\t"
		if den.isWishingPiece():
			seed = den.seed()
			info = "!!!\t" + info
		print(info)
		r = Raid(seed = den.seed(), flawlessiv = spawn.FlawlessIVs(), ability = spawn.Ability(), gender = spawn.Gender(), species = spawn.Species(), altform = spawn.AltForm())
		r.print()
		print()

# Choose RNGable den to calculate frames
if seed is not None:
	print('Wishing Piece Den Prediction:')
	i = 0
	while i < MaxResults:
		r = Raid(seed, flawlessiv = 1)
		seed = XOROSHIRO(seed).next()
		if usefilters:
			if r.ShinyType != 'None' or r.IVs == V6 or r.IVs == S0 or r.IVs == A0:
				print(f"Frame:{i}")
				r.print()
		else:
			r.print()
		i += 1