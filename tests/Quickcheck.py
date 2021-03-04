# Go to root of PyNXBot
Path = 'Event/PersonalDump/'
Island = 0

import sys
sys.path.append('../')
from lookups import PKMString
from nxbot import SWSHBot
from structure import NestHoleReward8Archive
from structure import NestHoleDistributionEncounter8Archive, NestHoleCrystalEncounter8Archive, NestHoleDistributionReward8Archive
import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

pmtext = PKMString()
buf = bytearray(open('../resources/bytes/local_drop','rb').read())
drop = NestHoleReward8Archive.GetRootAsNestHoleReward8Archive(buf,0)
buf = bytearray(open('../resources/bytes/local_bonus','rb').read())
bonus = NestHoleReward8Archive.GetRootAsNestHoleReward8Archive(buf,0)

buf = bytearray(open(Path + 'normal_encount','rb').read()) if Island == 0 else bytearray(open(Path + f'normal_encount_rigel{Island}','rb').read())
eventencounter = NestHoleDistributionEncounter8Archive.GetRootAsNestHoleDistributionEncounter8Archive(buf,0x20)
buf = bytearray(open(Path + 'drop_rewards','rb').read())
dropreward = NestHoleDistributionReward8Archive.GetRootAsNestHoleDistributionReward8Archive(buf,0x20)
buf = bytearray(open(Path + 'bonus_rewards','rb').read())
bonusreward = NestHoleDistributionReward8Archive.GetRootAsNestHoleDistributionReward8Archive(buf,0x20)

for ii in range(eventencounter.TablesLength()):
	table = eventencounter.Tables(ii)
	for jj in range(table.EntriesLength()):
		entry = table.Entries(jj)
		rank = np.nonzero(entry.ProbabilitiesAsNumpy())[0]
		print(f'{entry.Nature()}-{pmtext.species[entry.Species()]}-{rank[0]+1}-{entry.Field09()}')


