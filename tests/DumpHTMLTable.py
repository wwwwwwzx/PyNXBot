Path = 'Event/Index 12/'
lang = 'en'
useLargeImage = True

import sys
sys.path.append('../')
from lookups import PKMString
from structure import NestHoleReward8Archive
from structure import NestHoleDistributionEncounter8Archive, NestHoleCrystalEncounter8Archive, NestHoleDistributionReward8Archive
from structure import PersonalTable
import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

def tr(c):
	return "\t<tr>\n"  + c + "\t</tr>"

def th(c):
	return "\t\t<th>"  + c + "</th>\n"

def td(c,style=''):
	return f"\t\t<td {style}>"  + c + "</td>\n"

def isthesame(entry1, entry2):
	if entry1.Species() != entry2.Species() or entry1.AltForm() != entry2.AltForm():
		return False
	if entry1.IsGigantamax() != entry2.IsGigantamax():
		return False
	if entry1.ShinyFlag() != entry2.ShinyFlag():
		return False
	return True

def getpmimage(species,forme,cangmax,isShiny):
	filename = f"{species:03}"
	if species == 849 and forme == 1 and not cangmax:
		filename += "-l"
	if cangmax and species != 868:
		filename += "-gi"
	if useLargeImage:
		if isShiny:
			url = f"https://www.serebii.net/Shiny/SWSH/{filename}.png"
		else:
			url = f"https://www.serebii.net/swordshield/pokemon/{filename}.png"
		return f'<img src="{url}" alt="{filename}" width="100" height="100">'
	else:
		url = f"https://www.serebii.net/pokedex-swsh/icon/{filename}.png"
		return f'<img src="{url}" alt="{filename}">'

GMAXSTR = "Gigantamax" if lang == "en" else "超极巨化"
SHINYSTR = "Shiny" if lang == "en" else "异色"
def getpmname(species,forme,cangmax,isShiny):
	formtext = pmtext.forms[pt.getFormeNameIndex(species,forme)]
	t = pmtext.species[species]
	if species == 849 or species == 869:
		t += '<br><small>' + formtext + '</small>'
	if cangmax:
		t += f'<br><small>{GMAXSTR}</small>'
	if isShiny:
		t += f'<br><small>{SHINYSTR}</small>'
	return t

pmtexten = PKMString('en')
def getitemimage(itemid):
	filename = pmtexten.items[itemid].replace(" ","").lower()
	url = f"https://www.serebii.net/itemdex/sprites/{filename}.png"
	return f'<img src="{url}" alt="{filename}">'

def getitemname(itemid):
	txt = getitemimage(itemid) + pmtext.items[itemid]
	if itemid >= 1130 and itemid <= 1229:
		tr = itemid - 1130
		return txt + " (" + pmtext.trmoves[tr] + ")"
	else:
		return txt

def getmsg1(entry, rank):
	return td(getpmimage(entry.Species(),entry.AltForm(),entry.IsGigantamax(),entry.ShinyFlag() == 2)) + td(getpmname(entry.Species(),entry.AltForm(),entry.IsGigantamax(),entry.ShinyFlag() == 2)) + td(f"{entry.Probabilities(rank)}%")

def getmsg2(entry, rank):
	pi = pt.getFormeEntry(entry.Species(),entry.AltForm())
	txt = td(f'{entry.Level()}')
	txt += td(f'{entry.FlawlessIVs()}')
	txt += td(f'{entry.Shield()}')
	txt += td(f'{entry.DynamaxLevel()}')
	txt += td(f'{entry.DynamaxBoost():0.1f}')
	Sep = '<br>'
	if entry.Move3() > 0:
		movetxt = f"{pmtext.moves[entry.Move0()]}{Sep}{pmtext.moves[entry.Move1()]}{Sep}{pmtext.moves[entry.Move2()]}{Sep}{pmtext.moves[entry.Move3()]}"
	elif entry.Move2() > 0:
		movetxt = f"{pmtext.moves[entry.Move0()]}{Sep}{pmtext.moves[entry.Move1()]}{Sep}{pmtext.moves[entry.Move2()]}"
	elif entry.Move1() > 0:
		movetxt = f"{pmtext.moves[entry.Move0()]}{Sep}{pmtext.moves[entry.Move1()]}"
	else:
		movetxt = f"{pmtext.moves[entry.Move0()]}"
	if entry.AdditionalMove1Rate() > 0:
		movetxt += "<br><br>" + f"{pmtext.moves[entry.AdditionalMove1()]}" + f" ({entry.AdditionalMove1Rate()}% - {entry.AdditionalMove1PP()}PP)"
	if entry.AdditionalMove2Rate() > 0:
		movetxt += "<br>" + f"{pmtext.moves[entry.AdditionalMove2()]}" + f" ({entry.AdditionalMove2Rate()}% - {entry.AdditionalMove2PP()}PP)"
	txt += td(movetxt)

	dropid = entry.DropTableID()
	dropmsg = ''
	# look up local drop tables
	for jj in range(drop.TablesLength()):
		ldt = drop.Tables(jj)
		if dropid == ldt.TableID():
			style = ''
			for kk in range(ldt.EntriesLength()):
				ldte = ldt.Entries(kk)
				if ldte.Values(rank) > 0:
					dropmsg += f'{ldte.Values(rank)}% ' + getitemname(ldte.ItemID()) + "<br>"
	# look up event drop tables
	for jj in range(dropreward.TablesLength()):
		edt = dropreward.Tables(jj) # event drop table
		if dropid == edt.TableID():
			style = 'style = "background-color:#ffe4c3"'
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
					dropmsg += f'{value}% ' + getitemname(edte.ItemID()) + "<br>"
	txt += td(dropmsg[:-4],style)


	bonusid = entry.BonusTableID()
	bonustxt = ''
	# look up local bonus tables
	for jj in range(bonus.TablesLength()):
		lbt = bonus.Tables(jj)
		if bonusid == lbt.TableID():
			style = ''
			for kk in range(lbt.EntriesLength()):
				lbte = lbt.Entries(kk)
				if lbte.Values(rank) > 0:
					bonustxt += f'{lbte.Values(rank)}x' + getitemname(lbte.ItemID()) + "<br>"
	# look up event bonus tables
	for jj in range(bonusreward.TablesLength()):
		ebt = bonusreward.Tables(jj) # event bonus table
		if bonusid == ebt.TableID():
			style = 'style = "background-color:#ffe4c3"'
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
					bonustxt += f'{value}x' + getitemname(ebte.ItemID()) + "<br>"
	txt += td(bonustxt[:-4],style)

	comment = ''
	AbilityStr = 'Ability' if lang == 'en' else '特性'
	NatureStr = 'Nature' if lang == 'en' else '性格'

	if entry.Ability() == 4:
		pass # comment += "can be HA<br>"
	elif entry.Ability() == 3:
		comment += ("No Hidden Ability" if lang == 'en' else '随机无梦特') + "<br>"
	elif entry.Ability() == 2:
		comment += AbilityStr + ": H-" + pmtext.abilities[pi.AbilityH()] + "<br>"
	elif entry.Ability() == 1:
		comment += AbilityStr + ": 2-" + pmtext.abilities[pi.Ability2()] + "<br>"
	else:
		comment += AbilityStr + ": 1-" + pmtext.abilities[pi.Ability1()] + "<br>"
	if entry.Nature() == 25:
		pass # random nature
	else:
		comment += f"{NatureStr}: {pmtext.natures[entry.Nature()]}<br>"
	if entry.ShinyFlag() == 1:
		comment += ("Cannot be shiny" if lang == 'en' else '必定不闪') + "<br>"
	elif entry.ShinyFlag() == 2:
		pass # comment += SHINYSTR + "<br>"
	if entry.Field13() > 4:
		comment += ("Cannot be captured" if lang == 'en' else '不能捕获') + "<br>"
	txt += td('-' if comment == '' else comment[:-4])
	return txt

pmtext = PKMString(lang)
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

print('<table border="1" class="table table-striped table-bordered table-condensed" style="text-align:center; margin:auto">')
print('<tbody>')
if lang == "en":
	tableheader = th("") + th("Pokemon") + th("Chance") + th("Games") + th("Level") + th("Perfect<br>IVs") + th("Shield")
	tableheader += th("Dynamax<br>Level") + th("Dynamax<br>Boost") + th("Moves") + th("Drop") + th("Bonus") + th("Comment")
elif lang == "zh":
	tableheader = th("") + th("宝可梦") + th("几率") + th("游戏") + th("等级") + th("完美<br>个体数") + th("护盾数")
	tableheader += th("极巨化<br>等级") + th("极巨化<br>提升") + th("招式") + th("道具掉落") + th("经验糖果") + th("备注")
print(tr(tableheader))
for star in range(5):
	star = 4 - star
	stars = '★'
	for pp in range(star):
		stars += '★'
	print('\t\t<td colspan="13">'+ stars +'</td>')
	for ii in range(tablelength):
		ii = tablelength - ii - 1
		entry1 = eventencounter.Tables(0).Entries(ii)
		if entry1.Probabilities(star) > 0:
			entry2 = eventencounter.Tables(1).Entries(ii)
			if isthesame(entry1,entry2):
				# Same entry
				msg = getmsg1(entry1,star)
				msg += td("SHSW" if lang == 'en' else '剑盾') 
				msg += getmsg2(entry1,star)
				print(tr(msg))
			else:
				msg = getmsg1(entry1,star)
				msg += td("SH" if lang == 'en' else '剑')
				msg += getmsg2(entry1,star)
				print(tr(msg))
				msg = getmsg1(entry2,star)
				msg += td("SW" if lang == 'en' else '盾')
				msg += getmsg2(entry2,star)
				print(tr(msg))
print('</tbody>')
print('</table>')