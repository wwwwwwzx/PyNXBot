# Go to root/test of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from rng import XORSHIFT
from nxbot import BDSPBot

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

def signal_handler(signal, advances): #CTRL+C handler
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

r = XORSHIFT(b.getSeed())
seed = r.state()
advances = 0
print("Initial Seed")
print(f"S[0]: {seed[0]:08X}\tS[1]: {seed[1]:08X}\nS[2]: {seed[2]:08X}\tS[1]: {seed[3]:08X}")
print()
print(f"Advances: {advances}\n\n")

targetAdvances = 0
botFlag = input("Press A at a specific advance? (y/n) ")
if botFlag == "y" or botFlag == "Y":
    botFlag = True
    targetAdvances = int(input("Input the target advance: "))
else:
    botFlag = False
print("\n")

while True:
    currSeed = b.getSeed()

    while r.state() != currSeed:
        r.next()
        advances += 1

        if r.state() == currSeed:
            print("Current Seed")
            print(f"S[0]: {currSeed[0]:08X}\tS[1]: {currSeed[1]:08X}\nS[2]: {currSeed[2]:08X}\tS[1]: {currSeed[3]:08X}")
            print()
            print(f"Advances: {advances}\n\n")

            if botFlag and advances == targetAdvances:
                for i in range(5):
                    b.click("A")
                    b.pause(0.2)
