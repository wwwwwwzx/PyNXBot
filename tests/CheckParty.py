# Go to root of PyNXBot
import sys
sys.path.append('../')

from structure import PK8
from nxbot import SWSHBot

b = SWSHBot('192.168.0.10')
pk8 = PK8(b.readParty(1))
print(pk8.toString())