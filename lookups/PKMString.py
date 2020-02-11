import os

class PKMString(object):
	def __init__(self):
		with open(os.path.dirname(os.path.realpath(__file__)) + '/Abilities.txt','r', encoding="utf8") as file: 
			self.abilities = file.read().splitlines()
		with open(os.path.dirname(os.path.realpath(__file__)) + '/Natures.txt','r', encoding="utf8") as file: 
			self.natures = file.read().splitlines()
		with open(os.path.dirname(os.path.realpath(__file__)) + '/Species.txt','r', encoding="utf8") as file: 
			self.species = file.read().splitlines()
		with open(os.path.dirname(os.path.realpath(__file__)) + '/Moves.txt','r', encoding="utf8") as file: 
			self.moves = file.read().splitlines()