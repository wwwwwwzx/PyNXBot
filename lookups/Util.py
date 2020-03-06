from lookups import PKMString
from structure import PersonalTable

class Util():
	STRINGS = PKMString()
	PT = PersonalTable(bytearray(open('../resources/bytes/personal_swsh','rb').read()))
	GenderSymbol = ['♂','♀','-']

	@staticmethod
	def translate(lang):
		Util.STRINGS = PKMString(lang)