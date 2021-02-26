#Watts farmer Bot

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

currWatts = b.TrainerSave.Watts()
b.setWatts(currWatts)
print(f"Current Watts: {currWatts}\n")

print("Farming watts...")
while True:
    b.click('R') #R on Luxray "+1" button
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
                b.getWatts(True,0.5)
                break
             else:
                print("No watts in Den")
                break

#    stop = input("Continue farming? (y/n): ")
#    if stop == 'n' or stop == 'N':
#        break

print("Watts farming ended")
print()
b.close()
