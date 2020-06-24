# Go to root of PyNXBot
import sys
sys.path.append('../')

from structure import PK8
from nxbot import SWSHBot

b = SWSHBot('192.168.1.6')
for ii in range(1,7):
        pk8 = PK8(b.readParty(ii))
        print(pk8.toString())
