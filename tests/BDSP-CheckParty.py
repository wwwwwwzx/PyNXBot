# Go to root of PyNXBot
import sys
import json
sys.path.append('../')

from structure import PK8
from nxbot import BDSPBot

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

for ii in range(1,7):
    print(f"Slot: {ii}")
    pk8 = PK8(b.readParty(ii))
    if pk8.isValid() and pk8.ec() != 0:
        print(pk8.toString())
    else:
        print('Empty')

print()
b.close()
