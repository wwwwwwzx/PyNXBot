# Go to root of PyNXBot
import sys
sys.path.append('../')
from lookups import PKMString
from nxbot import SWSHBot
from structure import NestHoleReward8Archive
from structure import NestHoleDistributionEncounter8Archive, NestHoleCrystalEncounter8Archive, NestHoleDistributionReward8Archive
import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

ReadFromConsole = False
DumpPath = 'Event/Current/'
LocalPath = 'Event/Index 14/'
IP = '192.168.0.10'

pmtext = PKMString()
buf = bytearray(open('../resources/bytes/local_drop','rb').read())
drop = NestHoleReward8Archive.GetRootAsNestHoleReward8Archive(buf,0)
buf = bytearray(open('../resources/bytes/local_bonus','rb').read())
bonus = NestHoleReward8Archive.GetRootAsNestHoleReward8Archive(buf,0)

if ReadFromConsole:
	b = SWSHBot(IP)
	buf = b.readEventBlock_RaidEncounter(DumpPath)
else:
	buf = bytearray(open(LocalPath + 'normal_encount','rb').read())
eventencounter = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf,0x20)

if ReadFromConsole:
	buf = b.readEventBlock_DropRewards(DumpPath)
else:
	buf = bytearray(open(LocalPath + 'drop_rewards','rb').read())
dropreward = NestHoleDistributionReward8Archive.GetRootAsNestHoleDistributionReward8Archive(buf,0x20)

if ReadFromConsole:
	buf = b.readEventBlock_BonusRewards(DumpPath)
else:
	buf = bytearray(open(LocalPath + 'Bonus_rewards','rb').read())
bonusreward = NestHoleDistributionReward8Archive.GetRootAsNestHoleDistributionReward8Archive(buf,0x20)

if ReadFromConsole:
	buf = b.readEventBlock_CrystalEncounter(DumpPath)
else:
	buf = bytearray(open(LocalPath + 'dai_encount','rb').read())
crystalencounter = NestHoleCrystalEncounter8Archive.GetRootAsNestHoleCrystalEncounter8Archive(buf,0x20)

def printdrop(dropid, rank):
# look up local drop tables
	for jj in range(drop.TablesLength()):
		ldt = drop.Tables(jj)
		if dropid == ldt.TableID():
			msg = 'Drop: '
			for kk in range(ldt.EntriesLength()):
				ldte = ldt.Entries(kk)
				if ldte.Values(rank) > 0:
					msg += pmtext.items[ldte.ItemID()] + f'({ldte.Values(rank)}%)' + '  \t'
			print(msg)
	# look up event drop tables
	for jj in range(dropreward.TablesLength()):
		edt = dropreward.Tables(jj) # event drop table
		if dropid == edt.TableID():
			msg = 'Drop(E): '
			for kk in range(edt.EntriesLength()):
				edte = edt.Entries(kk)
				if rank == 0:
				 	value = edte.Value0()
				elif rank == 1:
				 	value = edte.Value1()
				elif rank == 2:
					value = edte.Value2()
				elif rank == 3:
					value = edte.Value3()
				else:
					value = edte.Value4()
				if value > 0:
					msg += pmtext.items[edt.Entries(kk).ItemID()] + f'({value}%)' + '  \t'
			print(msg)

def printbonus(bonusid,rank):
# look up local bonus tables
	for jj in range(bonus.TablesLength()):
		lbt = bonus.Tables(jj)
		if bonusid == lbt.TableID():
			msg = 'Bonus: ' 
			for kk in range(lbt.EntriesLength()):
				lbte = lbt.Entries(kk)
				if lbte.Values(rank) > 0:
					msg += f'{lbte.Values(rank)} x ' + pmtext.items[lbte.ItemID()] + '\t\t'
			print(msg)
	# look up event bonus tables
	for jj in range(bonusreward.TablesLength()):
		ebt = bonusreward.Tables(jj) # event bonus table
		if bonusid == ebt.TableID():
			msg = 'Bonus(E): ' 
			for kk in range(ebt.EntriesLength()):
				ebte = ebt.Entries(kk)
				if rank == 0:
				 	value = ebte.Value0()
				elif rank == 1:
				 	value = ebte.Value1()
				elif rank == 2:
					value = ebte.Value2()
				elif rank == 3:
					value = ebte.Value3()
				else:
					value = ebte.Value4()
				if value > 0:
					msg += f'{value} x ' + pmtext.items[ebt.Entries(kk).ItemID()] + '\t\t'
			print(msg)

def getMoves(entry):
	msg = f"{pmtext.moves[entry.Move0()]} / {pmtext.moves[entry.Move1()]} / {pmtext.moves[entry.Move2()]} / {pmtext.moves[entry.Move3()]}  \t"
	if entry.AdditionalMove1Rate() > 0:
		msg += f"({pmtext.moves[entry.AdditionalMove1()]}-{entry.AdditionalMove1Rate()}%-{entry.AdditionalMove1PP()}PP)"
	if entry.AdditionalMove2Rate() > 0:
		msg += f" ({pmtext.moves[entry.AdditionalMove2()]}-{entry.AdditionalMove2Rate()}%-{entry.AdditionalMove2PP()}PP)"
	return msg

print('Raid Encounter Table')
if eventencounter.TablesIsNone():
	print('No promoted raid or wrong offset!')
else: 
	for ii in range(eventencounter.TablesLength()):
		table = eventencounter.Tables(ii);
		print(f"Table ID:{table.TableID()}")
		print(f"Game Version:{table.GameVersion()}")
		for jj in range(table.EntriesLength()):
			entry = table.Entries(jj)
			msg = f"{entry.EntryIndex()}:\tLv{entry.Level()} {'G-' if entry.IsGigantamax() else ''}{pmtext.species[entry.Species()]}{('-' + str(entry.AltForm())) if entry.AltForm() > 0 else ''}"
			msg = f"{msg:25}\t"
			if entry.ShinyFlag() == 1:
				msg += "No Shiny\t"
			elif entry.ShinyFlag() == 2:
				msg += "Forced shiny\t"
			if entry.Field13() > 4:
				msg += "Not catchable\t"
			if entry.Ability() == 4:
				pass # random ability
			elif entry.Ability() == 3:
				msg +=f"A:(1/2) Only\t"
			elif entry.Ability() == 2:
				msg +=f"HA Only\t"
			else:
				msg += f"Ability {entry.Ability() + 1} Only\t"
			if entry.Nature() == 25:
				pass # random nature
			else:
				msg += f"{pmtext.natures[entry.Nature()]}\t"
			   
			msg += f"IVs:{entry.FlawlessIVs()}\t"
			rank = np.nonzero(entry.ProbabilitiesAsNumpy())[0][0]
			msg += f"{entry.ProbabilitiesAsNumpy()}\t"
			# msg += f"Drop:{entry.DropTableID():X} Bonus:{entry.BonusTableID():X}\t"
			msg += getMoves(entry)

			print(msg)
			printdrop(entry.DropTableID(),rank)
			printbonus(entry.BonusTableID(),rank)
			print()

print('\n\nCrystal Encounter Table')
if crystalencounter.TablesIsNone():
	print('Wrong offset!')
else: 
	for ii in range(crystalencounter.TablesLength()):
		table = crystalencounter.Tables(ii);
		print(f"Table ID:{table.TableID():X}")
		print(f"Game Version:{table.GameVersion()}")
		for jj in range(table.EntriesLength()):
			entry = table.Entries(jj)
			if entry.Species() == 0:	# Skip eggs
				continue
			print("Dynamax Crystal:" + pmtext.items[1279+jj])
			msg = f"{entry.EntryIndex()}:\t{'G-' if entry.IsGigantamax() else ''}{pmtext.species[entry.Species()]}{('-' + str(entry.AltForm())) if entry.AltForm() > 0 else ''}  Lv:{entry.Level()}"
			msg = f"{msg:25}\t"
			msg += f"N:{entry.Nature()}\t"
			msg += f"{entry.IVHp()}/{entry.IVAtk()}/{entry.IVDef()}/{entry.IVSpAtk()}/{entry.IVSpDef()}/{entry.IVSpe()}\t"
			msg += getMoves(entry)
			print(msg)

# print('\n\nDropTable')
# if dropreward.TablesIsNone():
# 	print('Wrong offset!')
# else: 
# 	for ii in range(dropreward.TablesLength()):
# 		table = dropreward.Tables(ii);
# 		print(f"Drop Table ID:{table.TableID():X}")
# 		msg = ''
# 		for jj in range(table.EntriesLength()):
# 			msg += pmtext.items[table.Entries(jj).ItemID()] + '\t'
# 		print(msg)

# print('\n\nBonusTable')
# if bonusreward.TablesIsNone():
# 	print('Wrong offset!')
# else: 
# 	for ii in range(bonusreward.TablesLength()):
# 		table = bonusreward.Tables(ii);
# 		print(f"Bonus Table ID:{table.TableID():X}")
# 		msg = ''
# 		for jj in range(table.EntriesLength()):
# 			msg += pmtext.items[table.Entries(jj).ItemID()] + f'({table.Entries(jj).Value4()})' + '\t'
# 		print(msg)

if ReadFromConsole:
	b.close()
