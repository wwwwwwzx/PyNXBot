# Go to root of PyNXBot
import sys
sys.path.append('../')
from lookups import PKMString
from nxbot import SWSHBot
from structure import EncounterNest8Archive
from structure import NestHoleReward8Archive

pmtext = PKMString()
buf = bytearray(open('../resources/bytes/local_raid','rb').read())
encounter = EncounterNest8Archive.GetRootAsEncounterNest8Archive(buf,0)

buf = bytearray(open('../resources/bytes/local_drop','rb').read())
drop = NestHoleReward8Archive.GetRootAsNestHoleReward8Archive(buf,0)

buf = bytearray(open('../resources/bytes/local_bonus','rb').read())
bonus = NestHoleReward8Archive.GetRootAsNestHoleReward8Archive(buf,0)

if encounter.TablesIsNone():
	print('Wrong offset!')
else:
	for ii in range(encounter.TablesLength()):
		table = encounter.Tables(ii);
		print(f"Table ID:0x{table.TableID():X}")
		print(f"Game Version:{table.GameVersion()}")
		for jj in range(table.EntriesLength()):
			entry = table.Entries(jj)
			msg = f"{entry.EntryIndex()}: {'G-' if entry.IsGigantamax() else ''}{pmtext.species[entry.Species()]}{('-' + str(entry.AltForm())) if entry.AltForm() > 0 else ''}"
			msg = f"{msg:25}\t"
			if entry.Ability() == 4:
				msg +=f"HA allowed\t"
			elif entry.Ability() == 3:
				msg +=f"no HA\t"
			elif entry.Ability() == 2:
				msg +=f"HA Only\t"
			else:
				msg += f"Ability {entry.Ability() + 1} Only\t"
			msg += f"G:{entry.Gender()} IV:{entry.FlawlessIVs()}\t"
			msgt = f"{entry.ProbabilitiesAsNumpy()}"
			msg += f"{msgt:18}\t"
			# msg += f"Drop:{entry.DropTableID():X} Bonus:{entry.BonusTableID():X}\t"
			print(msg)
			rank = entry.FlawlessIVs() - 1
			dropid = entry.DropTableID()
			for jj in range(drop.TablesLength()):
				ldt = drop.Tables(jj)
				if dropid == ldt.TableID():
					msg = 'Drop: '
					for kk in range(ldt.EntriesLength()):
						ldte = ldt.Entries(kk)
						if ldte.Values(rank) > 0:
							msg += pmtext.items[ldte.ItemID()] + f'({ldte.Values(rank)}%)' + '  \t'
					print(msg)

			bonusid = entry.BonusTableID()
			for jj in range(bonus.TablesLength()):
				lbt = bonus.Tables(jj)
				if bonusid == lbt.TableID():
					msg = 'Bonus: ' 
					for kk in range(lbt.EntriesLength()):
						lbte = lbt.Entries(kk)
						if lbte.Values(rank) > 0:
							msg += f'{lbte.Values(rank)} x ' + pmtext.items[lbte.ItemID()] + '\t\t'
					print(msg)
			print('')