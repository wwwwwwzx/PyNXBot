import os

class PKMString(object):
	def __init__(self,lang = 'en'):
		currentfolder = os.path.dirname(__file__) 
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
		if lang == 'zh':
			with open(currentfolder + f'/text_swsh_40000_{lang}.txt','r', encoding="utf8") as file: 
				self.locations = file.read().splitlines()
			with open(currentfolder + f'/MoveData.txt','r', encoding="utf8") as file: 
				movedata = file.read().splitlines()
				import re
				self.movetypes = []
				self.movecats = []
				for move in movedata:
					m = re.search(r'(\d+)\t(\d)',move)
					self.movetypes.append(self.types[int(m.group(1))])
					self.movecats.append(int(m.group(2)))