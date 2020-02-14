# Go to root of PyNXBot
import sys
sys.path.append('../')
from lookups import PKMString
from nxbot import SWSHBot
from structure import EncounterNest8Archive

pmtext = PKMString()
buf = bytearray(open('local_raid','rb').read())

encounter = EncounterNest8Archive.GetRootAsEncounterNest8Archive(buf,0)
if encounter.TablesIsNone():
	print('Wrong offset!')
else:
	for ii in range(encounter.TablesLength()):
		table = encounter.Tables(ii);
		print(f"Table ID:0x{table.TableID():X}")
		print(f"Game Version:{table.GameVersion()}")
		for jj in range(table.EntriesLength()):
			entry = table.Entries(jj)
			msg = f"{entry.EntryIndex()}:\t{'G-' if entry.IsGigantamax() else ''}{pmtext.species[entry.Species()]}{('-' + str(entry.AltForm())) if entry.AltForm() > 0 else ''}"
			msg = f"{msg:25}\t"
			msg += f"A:{entry.Ability()} G:{entry.Gender()} IV:{entry.FlawlessIVs()}\t"
			msgt = f"{entry.ProbabilitiesAsNumpy()}"
			msg += f"{msgt:18}\t"
			msg += f"Drop:{entry.DropTableID():X} Bonus:{entry.BonusTableID():X}\t"
			print(msg)