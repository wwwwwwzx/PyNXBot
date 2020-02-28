Path = 'event/Index 12/'
import sys
sys.path.append('../')
from lookups import PKMString
from structure import NestHoleDistributionEncounter8Archive
from structure import PersonalTable
import flatbuffers
from flatbuffers.compat import import_numpy

pmtext = PKMString()

buf = bytearray(open(Path + 'normal_encount','rb').read())
eventencounter = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf,0x20)
buf = bytearray(open('../resources/bytes/personal_swsh','rb').read())
pt = PersonalTable(buf)

def getspecies(species, isgmax = False, formid = 0):
	if species == 849:
		t = f'{species:03}' +('GM' if isgmax else '') + '|' + pmtext.species[species]
	else:
		t = f'{species:03}' + '|' + pmtext.species[species]
	return t

def getform(species, isgmax = False, formid = 0, isShiny = False):
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

def gettype(species, formid = 0):
	pi = pt.getFormeEntry(species,formid)
	type1 = pmtext.types[pi.Type1()]
	type2 = pmtext.types[pi.Type2()]
	if type1 == type2:
		return "type1=" + type1
	else:
		return "type1=" + type1 + "|type2=" + type2

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
			if entry1.Species() == entry2.Species() and entry1.AltForm() == entry2.AltForm() and entry1.IsGigantamax() == entry2.IsGigantamax() and entry1.Field12() == entry2.Field12():
				# Same entry
				msg = header + getspecies(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm())
				msg += f'|yes|yes|团体战|{entry1.Level()}|{entry1.Probabilities(star)}%|'
				msg += gettype(entry1.Species(),entry1.AltForm())
				msg += getform(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm(),entry1.Field12() == 2) + "}}"
				print(msg)
			else:
				msg = header + getspecies(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm())
				msg += f'|yes|no|团体战|{entry1.Level()}|{entry1.Probabilities(star)}%|'
				msg += gettype(entry1.Species(),entry1.AltForm())
				msg += getform(entry1.Species(),entry1.IsGigantamax(),entry1.AltForm(),entry1.Field12() == 2) + "}}"
				print(msg)
				msg = header + getspecies(entry2.Species(),entry2.IsGigantamax(),entry2.AltForm())
				msg += f'|no|yes|团体战|{entry2.Level()}|{entry2.Probabilities(star)}%|'
				msg += gettype(entry2.Species(),entry2.AltForm())
				msg += getform(entry2.Species(),entry2.IsGigantamax(),entry2.AltForm(),entry2.Field12() == 2) + "}}"
				print(msg)
print('{{捕捉/footer|红}}')