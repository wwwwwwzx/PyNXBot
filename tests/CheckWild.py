# Go to root of PyNXBot
import sys
import json
sys.path.append('../')

from structure import PK8
from nxbot import SWSHBot

config = json.load(open("../config.json"))
b = SWSHBot(config["IP"])

while True:
    pk8 = PK8(b.readWild())
    if pk8.isValid() and pk8.ec() != 0:
        print(pk8.toString())
    else:
        print("No battle started\n")
    stop = input("Check again? (y/n): ")
    print()
    if stop == 'n' or stop == 'N':
        b.close()
