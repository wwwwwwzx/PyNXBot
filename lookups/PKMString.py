import os

class PKMString(object):
	def __init__(self):
		currentfolder = os.path.dirname(os.path.realpath(__file__)) 
		with open(currentfolder+ '/Abilities.txt','r', encoding="utf8") as file: 
			self.abilities = file.read().splitlines()
		with open(currentfolder + '/Natures.txt','r', encoding="utf8") as file: 
			self.natures = file.read().splitlines()
		with open(currentfolder + '/Species.txt','r', encoding="utf8") as file: 
			self.species = file.read().splitlines()
		with open(currentfolder + '/Moves.txt','r', encoding="utf8") as file: 
			self.moves = file.read().splitlines()
		with open(currentfolder + '/Items.txt','r', encoding="utf8") as file: 
			self.items = file.read().splitlines()
		with open(currentfolder + '/TRTypes.txt','r', encoding="utf8") as file: 
			self.trtypes = file.read().splitlines()
