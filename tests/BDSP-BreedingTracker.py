# Go to root/test of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from rng import XORSHIFT
from nxbot import BDSPEggBot

config = json.load(open("../config.json"))
b = BDSPEggBot(config["IP"])

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
print(f"Advances: {advances}\n")

egg = b.getEggData()
isEggReady = "Yes" if egg.flag() else "No"
eggSeed = egg.seed()
eggSteps = egg.steps()
print(f"Is egg ready? {isEggReady}\nEgg Seed: {eggSeed:08X}\nSteps for next egg: {180 - eggSteps}\n\n")

while True:
    currSeed = b.getSeed()
    currEgg = b.getEggData()
    currIsEggReady = "Yes" if currEgg.flag() else "No"
    currEggSeed = currEgg.seed()
    currEggSteps = currEgg.steps()

    while r.state() != currSeed:
        r.next()
        advances += 1

        if r.state() == currSeed:
            print("Current Seed")
            print(f"S[0]: {currSeed[0]:08X}\tS[1]: {currSeed[1]:08X}\nS[2]: {currSeed[2]:08X}\tS[1]: {currSeed[3]:08X}")
            print()
            print(f"Advances: {advances}\n")
            print(f"Is egg ready? {currIsEggReady}\nEgg Seed: {currEggSeed:08X}\nSteps for next egg: {180 - currEggSteps}\n\n")
