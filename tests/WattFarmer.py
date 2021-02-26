#Watt farmer Bot

import signal
import sys
import json
sys.path.append('../')

from structure import Den
from nxbot import RaidBot

def signal_handler(signal, frame): #CTRL+C handler
    print()
    print("Stop request")
    b.close()

config = json.load(open("../config.json"))
b = RaidBot(config["IP"])

signal.signal(signal.SIGINT, signal_handler)

print("Farming watts...")
while True:
    b.click('R') #R on Luxray "+3" button
    b.pause(0.7)

    for ii in range(RaidBot.DENCOUNT):
        if ii > 189:
                den = Den(b.readDen(ii+32))
        elif ii > 99:
                den = Den(b.readDen(ii+11))
        else:
                den = Den(b.readDen(ii))
        if den.isActive() and den.isWishingPiece():
             if den.hasWatts():
                #print("Den has watts - Getting them...")
                b.getWatts(True,0.5)
                #print(f"Watts: {b.TrainerSave.Watt()}\n")
                break
             else:
                print("No watts in Den")

#    stop = input("Continue farming? (y/n): ")
#    if stop == 'n' or stop == 'N':
#        break

print("Watt farming ended")
print()
b.close()
