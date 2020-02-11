# Go to root of PyNXBot
import sys
sys.path.append('../')

from structure import NestHoleDistributionEncounter8Archive
from lookups import PKMString
from nxbot import SWSHBot

pmtext = PKMString()
b = SWSHBot('192.168.0.10')
buf = b.readEventBlock()
b.close()
# buf = open('dump_heap_0x2E5E58B8_0x23D4','rb').read()
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
			msg = f"{entry.EntryIndex()}:\t{'G-' if entry.IsGigantamax() else ''}{pmtext.species[entry.Species()]}{('-' + str(entry.AltForm())) if entry.AltForm() > 0 else ''}  Lv:{entry.Level()}\t\t"
			msg += f"A:{entry.Ability()} N:{entry.Nature()} G:{entry.Gender()}\t"
			for p in entry.ProbabilitiesAsNumpy():
				msg += f"{p} "
			msg += f"{pmtext.moves[entry.Move0()]} / {pmtext.moves[entry.Move1()]} / {pmtext.moves[entry.Move2()]} / {pmtext.moves[entry.Move3()]}\t"
			print(msg)