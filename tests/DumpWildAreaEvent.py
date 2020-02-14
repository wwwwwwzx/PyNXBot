# Go to root of PyNXBot
import sys
sys.path.append('../')
from lookups import PKMString
from nxbot import SWSHBot
from structure import NestHoleDistributionEncounter8Archive, NestHoleCrystalEncounter8Archive, NestHoleDistributionReward8Archive


ReadFromConsole = True
IP = '192.168.0.10'

pmtext = PKMString()

if ReadFromConsole:
	b = SWSHBot(IP)
	buf = b.readEventBlock_RaidEncounter()
else:
	buf = bytearray(open('normal_encount','rb').read())
print('Raid Encounter Table')
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


print('\n\nCrystal Encounter Table')
if ReadFromConsole:
	buf = b.readEventBlock_CrystalEncounter()
else:
	buf = bytearray(open('dai_encount','rb').read())
crystalencounter = NestHoleCrystalEncounter8Archive.GetRootAsNestHoleCrystalEncounter8Archive(buf,0x20)
if crystalencounter.TablesIsNone():
	print('Wrong offset!')
else: 
	for ii in range(crystalencounter.TablesLength()):
		table = crystalencounter.Tables(ii);
		print(f"Table ID:{table.TableID()}")
		print(f"Game Version:{table.GameVersion()}")
		for jj in range(table.EntriesLength()):
			entry = table.Entries(jj)
			if entry.Species() == 0:	# Skip eggs
				continue
			msg = f"{entry.EntryIndex()}:\t{'G-' if entry.IsGigantamax() else ''}{pmtext.species[entry.Species()]}{('-' + str(entry.AltForm())) if entry.AltForm() > 0 else ''}  Lv:{entry.Level()}"
			msg = f"{msg:25}\t"
			msg += f"N:{entry.Nature()}\t"
			msg += f"{entry.IVHp()}/{entry.IVAtk()}/{entry.IVDef()}/{entry.IVSpAtk()}/{entry.IVSpDef()}/{entry.IVSpe()}\t"
			msg += f"{pmtext.moves[entry.Move0()]} / {pmtext.moves[entry.Move1()]} / {pmtext.moves[entry.Move2()]} / {pmtext.moves[entry.Move3()]}\t"
			print(msg)


print('\n\nDropTable')
if ReadFromConsole:
	buf = b.readEventBlock_DropRewards()
else:
	buf = bytearray(open('drop_rewards','rb').read())
dropreward = NestHoleDistributionReward8Archive.GetRootAsNestHoleDistributionReward8Archive(buf,0x20)
if dropreward.TablesIsNone():
	print('Wrong offset!')
else: 
	for ii in range(dropreward.TablesLength()):
		table = dropreward.Tables(ii);
		print(f"Drop Table ID:{table.TableID()}")
		msg = ''
		for jj in range(table.EntriesLength()):
			msg += pmtext.items[table.Entries(jj).ItemID()] + '\t'
		print(msg)

if ReadFromConsole:
	buf = b.readEventBlock_BonusRewards()
else:
	buf = bytearray(open('Bonus_rewards','rb').read())
b.close()
