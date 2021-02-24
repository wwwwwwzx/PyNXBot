# Go to root of PyNXBot
import sys
import json
sys.path.append('../')

from structure import PK8
from nxbot import SWSHBot

config = json.load(open("../config.json"))
b = SWSHBot(config["IP"])

while True:
        empty = True
        box = int(input('Which box would you like to check? '))
        print()
        for ii in range(1,31):
                pk8 = PK8(b.readBox(box-1,ii-1))
                if pk8.isValid() and pk8.ec() != 0:
                        print(f"Box: {box} Slot: {ii}")
                        print(pk8.toString())
                        empty = False
        if empty:
                print('Box is empty\n')
        stop = input('Continue? (y/n) ' )
        if stop != 'y' and stop != 'Y':
                break
b.close()
