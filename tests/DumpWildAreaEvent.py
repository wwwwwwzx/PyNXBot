# Go to root of PyNXBot
import sys
sys.path.append('../')

from structure import NestHoleDistributionEncounter8Archive, NestHoleCrystalEncounter8Archive, NestHoleDistributionReward8Archive
from lookups import PKMString
from nxbot import SWSHBot

pmtext = PKMString()
b = SWSHBot('192.168.0.10')
buf = b.readEventBlock_RaidEncounter()
# buf = open('normal_encount','rb').read()
# buf = bytearray(buf)

eventencounter = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf,0x20)
if eventencounter.TablesIsNone():
	print('No promoted raid or wrong offset!')
else: 
	for ii in range(eventencounter.TablesLength()):
		table = eventencounter.Tables(ii);
		print(f"Table ID:{table.TableID()}")
		print(f"Game Version:{table.GameVersion()}")
		for jj in range(table.EntriesLength()):
			entry = table.Entries(jj)
			msg = f"{entry.EntryIndex()}:\t{'G-' if entry.IsGigantamax() else ''}{pmtext.species[entry.Species()]}{('-' + str(entry.AltForm())) if entry.AltForm() > 0 else ''}  Lv:{entry.Level()}"
			msg = f"{msg:25}\t"
			msg += f"A:{entry.Ability()} N:{entry.Nature()} G:{entry.Gender()}\t"
			msg += f"{entry.ProbabilitiesAsNumpy()} "
			msg += f"{pmtext.moves[entry.Move0()]} / {pmtext.moves[entry.Move1()]} / {pmtext.moves[entry.Move2()]} / {pmtext.moves[entry.Move3()]}\t"
			print(msg)

buf = b.readEventBlock_CrystalEncounter()
crystalencounter = NestHoleCrystalEncounter8Archive.GetRootAsNestHoleCrystalEncounter8Archive(buf,0x20)
if crystalencounter.TablesIsNone():
	print('Wrong offset!')
else: 
	pass

buf = b.readEventBlock_DropRewards()
dropreward = NestHoleDistributionReward8Archive.GetRootAsNestHoleDistributionReward8Archive(buf,0x20)
if dropreward.TablesIsNone():
	print('Wrong offset!')
else: 
	pass

buf = b.readEventBlock_BonusRewards()
b.close()
