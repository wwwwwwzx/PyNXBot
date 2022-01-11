# Go to root of PyNXBot
import sys
import json
sys.path.append('../')

from nxbot import BDSPBot
from structure import BDSPRoamer

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

while True:
    roamer8 = BDSPRoamer(b.readRoamerBlock(), b.TrainerSave.TID(), b.TrainerSave.SID())
    roamer8.toString()
    stop = input("Check again? (y/n): ")
    print()
    if stop == 'n' or stop == 'N':
        b.close()
