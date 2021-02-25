#Berry Picker Bot

import signal
import sys
import json
sys.path.append('../')

from nxbot import BerryBot

def signal_handler(signal, frame): #CTRL+C handler
    print()
    print("Stop request")
    b.pickBeforeLeaving()
    b.close()

config = json.load(open("../config.json"))
b = BerryBot(config["IP"])

signal.signal(signal.SIGINT, signal_handler)

cycles = input("Do you want a limited number of picking cycles? (y/n): ")
if cycles == 'y' or cycles == 'Y':
    cycles = int(input("Input the max number of picking cycles: "))
else:
    cycles = sys.maxsize

shakes = int(input("How many shakes per cycle? (input the number): "))

b.pause(0.5)
print()

i = 0
while i < cycles:
    b.click('R') #R on Luxray "+1" button
    b.pause(1.2)
    print("Cycle", i+1)
    b.shakeTree()
    b.continueShaking(shakes - 1)
    b.pickEverything()
    b.pause(0.5)
    print()
    i += 1

print(i, "Cycles completed!")
print()
b.close()
