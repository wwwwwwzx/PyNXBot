# Go to root of PyNXBot
import sys
import json
sys.path.append('../')

from structure import PK8
from nxbot import SWSHBot

config = json.load(open("../config.json"))
b = SWSHBot((config["IP"]))

while True:
        pk8 = PK8(b.readWild())
        print(pk8.toString())
        stop = input("Check again? (y/n): ")
        if stop == 'n' or stop == 'N':
                break
