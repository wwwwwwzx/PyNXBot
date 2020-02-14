# Go to root of PyNXBot
import sys
sys.path.append('../')

from structure import Den
from nxbot import SWSHBot
from rng import XOROSHIRO,Raid,Toxtricity

usefilters = False
MaxResults = 5
IP = '192.168.0.10'

# Desired IVs
V6 = [31,31,31,31,31,31]
S0 = [31,31,31,31,31,00]
A0 = [31,00,31,31,31,31]

b = SWSHBot(IP)
for ii in range(SWSHBot.DENCOUNT):
	den = Den(b.readDen(ii))
	if den.isActive() and den.isWishingPiece(): # Find the den is wishing pieced
		print(f"{ii}:0x{den.seed():X}")
		seed = den.seed()
		i = 0
		while i < MaxResults:
			r = Raid(seed, flawlessiv = 1, HA = 0, RandomGender = 1, ToxicityType = Toxtricity.NONE)
			seed = XOROSHIRO(seed).next()
			if usefilters:
				if r.ShinyType != 'None' or r.IVs == V6 or r.IVs == S0 or r.IVs == A0:
					print(i)
					r.print()
			else:
				r.print()
			i += 1
