# Go to root of PyNXBot
import sys
sys.path.append('../')
from lookups import PKMString
from structure import PersonalTable

pmtext = PKMString()

buf = bytearray(open('../resources/bytes/personal_swsh','rb').read())
pt = PersonalTable(buf)
print(pmtext.abilities[pt.getFormeEntry(869,2).Ability1()])