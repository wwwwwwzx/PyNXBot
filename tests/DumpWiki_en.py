Path = 'Event/Index 16/'
ShortVersion = True

# Go to root of PyNXBot
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
		return "{{Bag|TR " + pmtext.trtypes[tr] + "}}{{TR|" + f'{tr:02}|' + pmtext.trmoves[tr] + "}}"
	else:
		return "{{Bag|" + pmtext.items[itemid] + "}}[[" + pmtext.items[itemid] + "]]"

def getspecies(species, isgmax = False, formid = 0, isShiny = False):
	formtext = pmtext.forms[pt.getFormeNameIndex(species,formid)]
	if species == 849:
		t = '{{MSP|' + f'{species:03}' +('Gi' if isgmax else 'L' if formid == 1 else '') + '}}<br>{{p|' + pmtext.species[species] + '}}<br><small>' + formtext + '</small>'
	elif species == 868:
		t = '{{MSP|' + f'{species:03}' + '}}<br>{{p|' + pmtext.species[species] + '}}' + ('<br />[[File:Dynamax icon.png|link=Gigantamax]]' if isgmax else '')
	elif species == 869:
		t = '{{MSP|' + f'{species:03}' +('Gi' if isgmax else '') + '}}<br>{{p|' + pmtext.species[species] + '}}<br><small>' + formtext + '</small>'
	elif species == 678 or species == 876:
		t = '{{MSP|' + f'{species:03}' +('F' if formid else '') + '}}<br>{{p|' + pmtext.species[species] + '}}<br><small>' + formtext + '</small>'
	elif species in PersonalTable.Alolalist and formid == 1:
		t = '{{MSP|' + f'{species:03}' + 'A}}<br>{{p|' + pmtext.species[species] + '}}<br><small>' + formtext + '</small>'
	elif species in PersonalTable.Galarlist and formid:
		t = '{{MSP|' + f'{species:03}' + 'G}}<br>{{p|' + pmtext.species[species] + '}}<br><small>' + formtext + '</small>'
	else:
		t = '{{MSP|' + f'{species:03}' +('Gi' if isgmax else '') + '}}<br>{{p|' + pmtext.species[species] + '}}' + (f'<br>FormeID:{formid}' if formid > 0 else '')
	if isShiny:
		t+= '<br>{{Shiny}}'
	return t

def getspecies_short(species, isgmax = False, formid = 0):
	if species == 849:
		t = f'{species:03}' + ('Gi' if isgmax else ('L' if formid == 1 else '')) + '|' + pmtext.species[species]
	elif species == 868:
		t = f'{species:03}' + '|' + pmtext.species[species]
	elif species == 678 or species == 876:
		t = f'{species:03}' + ('F' if formid else '') +'|' + pmtext.species[species]
	elif species in PersonalTable.Alolalist and formid <= 1:
		t = f'{species:03}' + ('A' if formid else '') +'|' + pmtext.species[species]
	elif species in PersonalTable.Galarlist:
		t = f'{species:03}' + ('G' if formid else '') +'|' + pmtext.species[species]
	else:
		t = f'{species:03}' + ('Gi' if isgmax else '') +'|' + pmtext.species[species]
	return t

def getform_short(species, isgmax = False, formid = 0, isShiny = False):
	t = ''
	formtext = pmtext.forms[pt.getFormeNameIndex(species,formid)]
	if species == 849 or species == 869 or species == 678 or species == 876 or ((species in pt.Galarlist or species in pt.Alolalist) and formid):
		t = f"|form={formtext}"
	elif species == 868 and isgmax:
		t = '|form=Gigantamax Factor'
	if isgmax and species != 868:
		t = "|form=Gigantamax" if t == '' else (t + '<br>Gigantamax|formlink=Gigantamax')
	if isShiny:
		t = "|form=Shiny" if t == '' else (t + '<br>Shiny')
	return t

def gettype_short(species, formid = 0):
	pi = pt.getFormeEntry(species,formid)
	type1 = pmtext.types[pi.Type1()]
	type2 = pmtext.types[pi.Type2()]
	if type1 == type2:
		return "type1=" + type1
	else:
		return "type1=" + type1 + "|type2=" + type2

def getmsg1(entry, rank):
	return '| ' + getspecies(entry.Species(),entry.IsGigantamax(),entry.AltForm(),entry.ShinyFlag() == 2) + f' || {entry.Probabilities(rank)}% || '

def getmsg2(entry, rank):
	pi = pt.getFormeEntry(entry.Species(),entry.AltForm())
	msg = f'{entry.Level()}' + ' || '
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
	if entry.AdditionalMove1Rate() > 0 and entry.AdditionalMove1PP() > 0:
		msg += "<br><br>{{m|" + f"{pmtext.moves[entry.AdditionalMove1()]}" + "}}<br>" + f"({entry.AdditionalMove1Rate()}% - {entry.AdditionalMove1PP()}PP)"
	if entry.AdditionalMove2Rate() > 0 and entry.AdditionalMove2PP() > 0:
		msg += "<br>{{m|" + f"{pmtext.moves[entry.AdditionalMove2()]}" + "}}<br>" + f"({entry.AdditionalMove2Rate()}% - {entry.AdditionalMove2PP()}PP)"
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
					msg += f'{lbte.Values(rank)}x' + getitem(lbte.ItemID()) + "<br>"
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
	if entry.Ability() == 4:
		pass # comment +=f"can be HA<br>"
	elif entry.Ability() == 3:
		comment +=f"No Hidden Ability<br>"
	elif entry.Ability() == 2:
		comment += "Ability: {{a|" + pmtext.abilities[pi.AbilityH()] + "}}<br>"
	elif entry.Ability() == 1:
		comment += "Ability: {{a|" + pmtext.abilities[pi.Ability2()] + "}}<br>"
	else:
		comment += "Ability: {{a|" + pmtext.abilities[pi.Ability1()] + "}}<br>"
	if entry.Nature() == 25:
		pass # random nature
	else:
		comment += f"Nature: [[{pmtext.natures[entry.Nature()]}]]<br>"
	if entry.ShinyFlag() == 1:
		comment += "Cannot be shiny<br>"
	elif entry.ShinyFlag() == 2:
		pass # comment += "Shiny<br>"
	if entry.Field13() > 4:
		comment += f"Cannot be captured<br>"
	# if entry.AltForm() > 0:
	# 	comment += f"Forme:{entry.AltForm()}<br>"
	msg += ('-' if comment == '' else comment[:-4])
	return msg

def getmsg2_short(entry, rank):
	msg = f'|Raid|{entry.Level()}|{entry.Probabilities(rank)}%|'
	msg += gettype_short(entry.Species(),entry.AltForm())
	msg += getform_short(entry.Species(),entry.IsGigantamax(),entry.AltForm(),entry.ShinyFlag() == 2) + "}}"
	return msg

pmtext = PKMString('en')
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

tablenum = eventencounter.TablesLength()
tablelength = eventencounter.Tables(0).EntriesLength()
if tablenum != 2 or eventencounter.Tables(1).EntriesLength() != tablelength:
	print('Not a standard table')

if ShortVersion:
	print('{{catch/header/8|red|no}}')
	header = '{{catch/entry8|'
	for star in range(5):
		stars = '★'
		for pp in range(star):
			stars += '★'
		print('{{catch/div|red|'+ stars +'}}')
		for ii in range(tablelength):
			entry1 = eventencounter.Tables(0).Entries(ii)
			if entry1.Probabilities(star) > 0:
				entry2 = eventencounter.Tables(1).Entries(ii)
				if entry1.Species() == entry2.Species() and entry1.AltForm() == entry2.AltForm() and entry1.IsGigantamax() == entry2.IsGigantamax() and entry1.ShinyFlag() == entry2.ShinyFlag():
					# Same entry
					msg = header + getspecies_short(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm())
					msg += '|yes|yes'
					msg += getmsg2_short(entry1,star)
					print(msg)
				else:
					msg = header + getspecies_short(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm())
					msg += '|yes|no'
					msg += getmsg2_short(entry1,star)
					print(msg)
					msg = header + getspecies_short(entry2.Species(),entry2.IsGigantamax(),entry2.AltForm())
					msg += '|no|yes'
					msg += getmsg2_short(entry2,star)
					print(msg)
	print('{{catch/footer|red}}')
else:
	print('{| class="roundy" style="text-align:center; margin:auto; background:#{{sword color}}; border:3px solid #{{shield color}}')
	print('! Pokémon !! Rate !! colspan="2" | Games !! Level !! Flawless<br>IVs !! Shield !! Dynamax<br>Level !! Dynamax<br>Boost !! Moves  !! Drop  !! Bonus !! Comment')
	header = '|- style="background:white"\n'
	for star in range(5):
		star = 4 - star
		stars = '★'
		for pp in range(star):
			stars += '★'
		print('|- style="background:#7dd6ea"\n! colspan="13" | ' + stars)
		for ii in range(tablelength):
			ii = tablelength - 1 - ii
			entry1 = eventencounter.Tables(0).Entries(ii)
			if entry1.Probabilities(star) > 0:
				entry2 = eventencounter.Tables(1).Entries(ii)
				if entry1.Species() == entry2.Species() and entry1.AltForm() == entry2.AltForm() and entry1.IsGigantamax() == entry2.IsGigantamax() and entry1.ShinyFlag() == entry2.ShinyFlag():
					# Same entry
					msg = header + getmsg1(entry1,star)
					msg += 'style="background:#{{sword color}}" | Sw || '
					msg += 'style="background:#{{shield color}}" | Sh || '
					msg += getmsg2(entry1,star)
					print(msg)
				else:
					msg = header + getmsg1(entry1,star)
					msg += 'style="background:#{{sword color}}" | Sw || '
					msg += 'Sh ||'
					msg += getmsg2(entry1,star)
					print(msg)
					msg = header + getmsg1(entry2,star)
					msg += 'Sw || '
					msg += 'style="background:#{{shield color}}" | Sh || '
					msg += getmsg2(entry2,star)
					print(msg)
	print('|}\n\n\n')