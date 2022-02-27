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
print(f"S[0]: {seed[0]:08X}\tS[1]: {seed[1]:08X}\nS[2]: {seed[2]:08X}\tS[3]: {seed[3]:08X}")
print()
print(f"Advances: {advances}\n")

egg = b.getEggData()
isEggReady = "Yes" if egg.flag() else "No"
eggSeed = egg.seed()
eggSteps = egg.steps()
print(f"Is egg ready? {isEggReady}\nEgg Seed: {eggSeed:08X}\nSteps for next egg: {180 - eggSteps}\n\n")

dexOpened = False
trainercardOpened = False
scrolls = 0
targetAdvances = 0
botFlag = input("Press D-pad Down at a specific advance? (y/n) ")
if botFlag == "y" or botFlag == "Y":
    botFlag = True
    targetAdvances = int(input("Input the target advance: "))
else:
    botFlag = False
print("\n")

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
            print(f"S[0]: {currSeed[0]:08X}\tS[1]: {currSeed[1]:08X}\nS[2]: {currSeed[2]:08X}\tS[3]: {currSeed[3]:08X}")
            print()
            print(f"Advances: {advances}\n")
            print(f"Is egg ready? {currIsEggReady}\nEgg Seed: {currEggSeed:08X}\nSteps for next egg: {180 - currEggSteps}\n\n")

            if not dexOpened and botFlag and advances <= targetAdvances - 300:
                print(f"Opening pokedex to advance...\n\n")
                b.click("X")
                b.pause(0.9)
                b.click("A")
                b.pause(0.9)
                b.click("R")
                b.pause(1.5)
                dexOpened = True

            if dexOpened and botFlag and advances <= targetAdvances - 300:
                print(f"Pokedex scrolled {scrolls} times\n\n")
                scrolls += 1
                b.click("DRIGHT")
                b.pause(0.2)

            if dexOpened and botFlag and advances >= targetAdvances - 300:
                print(f"Closing pokedex...\n\n")
                b.click("B")
                b.pause(0.9)
                b.click("B")
                b.pause(0.9)
                dexOpened = False

            if not trainercardOpened and botFlag and advances >= targetAdvances - 300 and advances <= targetAdvances - 30:
                print(f"Opening trainercard to advance...\n\n")
                b.click("X")
                b.pause(0.9)
                b.click("DLEFT")
                b.pause(0.2)
                b.click("A")
                trainercardOpened = True

            if trainercardOpened and botFlag and advances >= targetAdvances - 30:
                print(f"Closing trainercard...\n\n")
                b.click("B")
                b.pause(0.9)
                b.click("DRIGHT")
                b.pause(0.2)
                b.click("B")
                b.pause(0.9)
                trainercardOpened = False

            if botFlag and advances == targetAdvances:
                for i in range(5):
                    b.click("DDOWN")
                    b.pause(0.1)
