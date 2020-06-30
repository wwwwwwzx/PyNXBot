# Go to root of PyNXBot
import sys
import  json
sys.path.append('../')

from structure import PK8
from nxbot import SWSHBot

config = json.load(open("../config.json"))
b = SWSHBot(config["IP"])

for ii in range(1,7):
        pk8 = PK8(b.readParty(ii))
        print(pk8.toString())
b.close()
