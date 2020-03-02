import os

class PKMString(object):
	def __init__(self,lang = 'en'):
		currentfolder = os.path.dirname(os.path.realpath(__file__)) 
		with open(currentfolder+ f'/text_Abilities_{lang}.txt','r', encoding="utf8") as file: 
			self.abilities = file.read().splitlines()
		with open(currentfolder + f'/text_Natures_{lang}.txt','r', encoding="utf8") as file: 
			self.natures = file.read().splitlines()
		with open(currentfolder + f'/text_Species_{lang}.txt','r', encoding="utf8") as file: 
			self.species = file.read().splitlines()
		with open(currentfolder + f'/text_Moves_{lang}.txt','r', encoding="utf8") as file: 
			self.moves = file.read().splitlines()
		with open(currentfolder + f'/text_Items_{lang}.txt','r', encoding="utf8") as file: 
			self.items = file.read().splitlines()
		with open(currentfolder + f'/text_Types_{lang}.txt','r', encoding="utf8") as file: 
			self.types = file.read().splitlines()
		with open(currentfolder + f'/text_Forms_{lang}.txt','r', encoding="utf16") as file:
		 	self.forms = file.read().splitlines()
		if lang == 'zh' or lang == 'en': # for table
			with open(currentfolder + f'/text_TRTypes_{lang}.txt','r', encoding="utf8") as file: 
				self.trtypes = file.read().splitlines()
			with open(currentfolder + f'/text_TRMoves_{lang}.txt','r', encoding="utf8") as file: 
				self.trmoves = file.read().splitlines()