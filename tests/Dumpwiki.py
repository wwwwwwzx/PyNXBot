# Go to root of PyNXBot

Path = 'Event/Index 12/'
ShortVersion = False
import sys
sys.path.append('../')
from lookups import PKMString
from structure import NestHoleReward8Archive
from structure import NestHoleDistributionEncounter8Archive, NestHoleCrystalEncounter8Archive, NestHoleDistributionReward8Archive
from structure import PersonalTable
import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

def getitem(itemid):
	if itemid >= 1130 and itemid <= 1229:
		tr = itemid - 1130
		return "{{Bag|TR " + pmtext.trtypes[tr] + "}}{{TR|" + f'{tr}' + "|8}}"
	else:
		return "{{Bag|" + pmtext.items[itemid] + "}}{{i|" + pmtext.items[itemid] + "}}"

def getspecies(species, isgmax = False, formid = 0, isShiny = False):
	if species == 849:
		t = '{{MSP|' + f'{species:03}' +('GM' if isgmax else 'L' if formid == 1 else '') + '}}<br>[[' + pmtext.species[species] + ']]<br><small>' + ('高调的样子' if formid == 0 else '低调的样子') + '</small>'
	elif species == 868:
		t = '{{MSP|' + f'{species:03}' + '}}<br>[[' + pmtext.species[species] + ']]' + ('<br />[[File:极巨化 Sprite.png|link=极巨化]]' if isgmax else '')
	else:
		t = '{{MSP|' + f'{species:03}' +('GM' if isgmax else '') + '}}<br>[[' + pmtext.species[species] + ']]' + (f'<br>形态数:{formid}' if formid > 0 else '')
	if isShiny:
		t+= '<br>[[File:ShinySWSHStar.png]]'
	return t

def getspecies_short(species, isgmax = False, formid = 0):
	if species == 849:
		t = f'{species:03}' +('GM' if isgmax else '') + '|' + pmtext.species[species]
	else:
		t = f'{species:03}' + '|' + pmtext.species[species]
	return t

def getform_short(species, isgmax = False, formid = 0, isShiny = False):
	t = ''
	if species == 849:
		t = "|form=高调的样子" if formid == 0 else "|form=低调的样子"
	elif species == 868:
		t = f'{species:03}' + '|' + pmtext.species[species]
	if isgmax:
		t = "|form=超极巨化" if t == '' else (t + '<br>超极巨化')
	if isShiny:
		t = "|form=异色" if t == '' else (t + '<br>异色')
	return t

def gettype_short(species, formid = 0):
	pi = pt.getFormeEntry(species,formid)
	type1 = pmtext.types[pi.Type1()]
	type2 = pmtext.types[pi.Type2()]
	if type1 == type2:
		return "type1=" + type1
	else:
		return "type1=" + type1 + "|type2=" + type2

pmtext = PKMString('zh')
buf = bytearray(open('../resources/bytes/local_drop','rb').read())
drop = NestHoleReward8Archive.GetRootAsNestHoleReward8Archive(buf,0)
buf = bytearray(open('../resources/bytes/local_bonus','rb').read())
bonus = NestHoleReward8Archive.GetRootAsNestHoleReward8Archive(buf,0)
buf = bytearray(open('../resources/bytes/personal_swsh','rb').read())
pt = PersonalTable(buf)

buf = bytearray(open(Path + 'normal_encount','rb').read())
eventencounter = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf,0x20)
buf = bytearray(open(Path + 'drop_rewards','rb').read())
dropreward = NestHoleDistributionReward8Archive.GetRootAsNestHoleDistributionReward8Archive(buf,0x20)
buf = bytearray(open(Path + 'bonus_rewards','rb').read())
bonusreward = NestHoleDistributionReward8Archive.GetRootAsNestHoleDistributionReward8Archive(buf,0x20)

if ShortVersion:
	tablenum = eventencounter.TablesLength()
	if tablenum != 2:
		print('Not standard')
	tablelength = eventencounter.Tables(0).EntriesLength()
	print('{{捕捉/header|红|no}}')
	header = '{{捕捉/entry8|'
	for star in range(5):
		stars = '★'
		for pp in range(star):
			stars += '★'
		print('{{捕捉/div|红|'+ stars +'}}')
		for ii in range(tablelength):
			entry1 = eventencounter.Tables(0).Entries(ii)
			if entry1.Probabilities(star) > 0:
				entry2 = eventencounter.Tables(1).Entries(ii)
				if entry1.Species() == entry2.Species() and entry1.AltForm() == entry2.AltForm() and entry1.IsGigantamax() == entry2.IsGigantamax() and entry1.ShinyFlag() == entry2.ShinyFlag():
					# Same entry
					msg = header + getspecies_short(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm())
					msg += f'|yes|yes|团体战|{entry1.Level()}|{entry1.Probabilities(star)}%|'
					msg += gettype_short(entry1.Species(),entry1.AltForm())
					msg += getform_short(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm(),entry1.ShinyFlag() == 2) + "}}"
					print(msg)
				else:
					msg = header + getspecies_short(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm())
					msg += f'|yes|no|团体战|{entry1.Level()}|{entry1.Probabilities(star)}%|'
					msg += gettype_short(entry1.Species(),entry1.AltForm())
					msg += getform_short(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm(),entry1.ShinyFlag() == 2) + "}}"
					print(msg)
					msg = header + getspecies_short(entry2.Species(),entry2.IsGigantamax(),entry2.AltForm())
					msg += f'|no|yes|团体战|{entry2.Level()}|{entry2.Probabilities(star)}%|'
					msg += gettype_short(entry2.Species(),entry2.AltForm())
					msg += getform_short(entry2.Species(),entry2.IsGigantamax(),entry2.AltForm(),entry2.ShinyFlag() == 2) + "}}"
					print(msg)
	print('{{捕捉/footer|红}}')
else: # Full version
	print('__TOC__')
	for ii in range(eventencounter.TablesLength()):
		table = eventencounter.Tables(ii)
		ver = '剑' if table.GameVersion() == 1 else '盾'
		ver2 = 'SW' if table.GameVersion() == 1 else 'SH'
		print('=={{game|'+ ver2 +'}}==') 
		print('{| class="bg-'+ ver +' bd-'+ ver +' roundy at-c eplist"')
		print('|- class="bgl-'+ ver +'"')
		print('! ★(几率) !! 宝可梦 !! 等级 !! 完美个体数 !! 护盾数 !! 极巨化等级 !! 极巨化提升 !! 招式  !! 可能获得的奖励道具  !! 奖励糖果 !! 备注')
		print('|- style="background:white"')
		print(f'! colspan="11" | Nest ID：{table.TableID()}')
		for jj in range(table.EntriesLength()):
			entry = table.Entries(table.EntriesLength() - jj - 1)
			pi = pt.getFormeEntry(entry.Species(),entry.AltForm())
			rank = np.nonzero(entry.ProbabilitiesAsNumpy())[0]
			print('|- style="background:white"')
			msg = '| '
			for r in rank:
				stars = '★'
				for pp in range(r):
					stars += '★'
				msg += stars + '<br>(' + f'{entry.Probabilities(r)}%)<br>'
			msg =  msg[:-4] + ' || ' 
			msg += getspecies(entry.Species(),entry.IsGigantamax(),entry.AltForm(),entry.ShinyFlag() == 2) + ' || '
			msg += f'{entry.Level()}' + ' || '
			msg += f'{entry.FlawlessIVs()}' + ' || '
			msg += f'{entry.Shield()}' + ' || '
			msg += f'{entry.DynamaxLevel()}' + ' || '
			msg += f'{entry.DynamaxBoost():0.1f}' + 'x || '
			Sep = '}}<br>{{m|'
			msg += '{{m|'
			if entry.Move3() > 0:
				msg += f"{pmtext.moves[entry.Move0()]}{Sep}{pmtext.moves[entry.Move1()]}{Sep}{pmtext.moves[entry.Move2()]}{Sep}{pmtext.moves[entry.Move3()]}"
			elif entry.Move2() > 0:
				msg += f"{pmtext.moves[entry.Move0()]}{Sep}{pmtext.moves[entry.Move1()]}{Sep}{pmtext.moves[entry.Move2()]}"
			elif entry.Move1() > 0:
				msg += f"{pmtext.moves[entry.Move0()]}{Sep}{pmtext.moves[entry.Move1()]}"
			else:
				msg += f"{pmtext.moves[entry.Move0()]}"
			msg += "}}"
			if entry.AdditionalMove1Rate() > 0:
				msg += "<br><br>{{m|" + f"{pmtext.moves[entry.AdditionalMove1()]}" + "}}<br>" + f"({entry.AdditionalMove1Rate()}% - {entry.AdditionalMove1PP()})"
			if entry.AdditionalMove2Rate() > 0:
				msg += "<br>{{m|" + f"{pmtext.moves[entry.AdditionalMove2()]}" + "}}<br>" + f"({entry.AdditionalMove2Rate()}% - {entry.AdditionalMove2PP()})"
			msg += ' || '

			dropid = entry.DropTableID()
			# look up local drop tables
			for jj in range(drop.TablesLength()):
				ldt = drop.Tables(jj)
				if dropid == ldt.TableID():
					for kk in range(ldt.EntriesLength()):
						ldte = ldt.Entries(kk)
						if ldte.Values(rank) > 0:
							msg += f'{ldte.Values(rank)}% ' + getitem(ldte.ItemID()) + "<br>"
			# look up event drop tables
			for jj in range(dropreward.TablesLength()):
				edt = dropreward.Tables(jj) # event drop table
				if dropid == edt.TableID():
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
							msg += f'{value}% ' + getitem(edte.ItemID()) + "<br>"
			msg = msg[:-4] + ' || '


			bonusid = entry.BonusTableID()
			# look up local bonus tables
			for jj in range(bonus.TablesLength()):
				lbt = bonus.Tables(jj)
				if bonusid == lbt.TableID():
					for kk in range(lbt.EntriesLength()):
						lbte = lbt.Entries(kk)
						if lbte.Values(rank) > 0:
							msg += f'{lbte.Values(rank)}x ' + getitem(lbte.ItemID()) + "<br>"
			# look up event bonus tables
			for jj in range(bonusreward.TablesLength()):
				ebt = bonusreward.Tables(jj) # event bonus table
				if bonusid == ebt.TableID():
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
							msg += f'{value}x ' + getitem(ebte.ItemID()) + "<br>"
			msg = msg[:-4] + ' || '

			comment = ''
			if entry.ShinyFlag() == 1:
				comment += "必定非异色<br>"
			elif entry.ShinyFlag() == 2:
				pass # comment += "必定异色<br>"
			if entry.Ability() == 4:
				pass # comment +=f"特性:随机可梦特<br>"
			elif entry.Ability() == 3:
				comment +=f"特性:随机普特<br>"
			elif entry.Ability() == 2:
				comment +=f"固定[[{pmtext.abilities[pi.AbilityH()]}]]<br>"
			elif entry.Ability() == 1:
				comment +=f"固定[[{pmtext.abilities[pi.Ability2()]}]]<br>"
			else:
				comment +=f"固定[[{pmtext.abilities[pi.Ability1()]}]]<br>"
			if entry.Nature() == 25:
				pass # random nature
			else:
				comment += f"性格:{pmtext.natures[entry.Nature()]}<br>"
			if entry.Field13() > 4:
				comment += f"无法捕捉<br>"
			# if entry.AltForm() > 0:
			# 	comment += f"形态数:{entry.AltForm()}<br>"
			msg += ('-' if comment == '' else comment[:-4])
			print(msg)
		print('|}\n\n\n')