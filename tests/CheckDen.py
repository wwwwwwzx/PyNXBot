# Go to root of PyNXBot
import sys
sys.path.append('../')

from structure import Den
from nxbot import SWSHBot

b = SWSHBot('192.168.0.10')
for ii in range(SWSHBot.DENCOUNT):
	den = Den(b.readDen(ii))
	if den.isActive():
		print(f"{ii}:0x{den.seed():X}")