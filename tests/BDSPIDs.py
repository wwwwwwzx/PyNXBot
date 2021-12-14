# Go to root/test of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from rng import XORSHIFT,IDs
from nxbot import BDSPBot

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

def signal_handler(signal, advances): #CTRL+C handler
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

usefilters = 1 #set 0 to disable filter

TIDs = [0, 1337, 101] #add here the trainer info you need
SIDs = [0, 1337, 101]
G8TIDs = [0, 100001, 133331]

MaxAdvances = int(input("Input Max Advances: "))
b.pause(0.5)
print()

while True:
    seed = b.getSeed()
    tmpRNG = XORSHIFT(seed)
    print("Initial Seed")
    print(f"S[0]: {seed[0]:08X}\tS[1]: {seed[1]:08X}\nS[2]: {seed[2]:08X}\tS[1]: {seed[3]:08X}")
    print()
    print("Searchig...")
    found = False
    i = 0
    while i < MaxAdvances:
        r = IDs(tmpRNG.state())
        if usefilters:
            if r.G8TID in G8TIDs: #or r.TID in TIDs or r.SID in SIDs
                print(f"\nAdvances: {i}")
                r.printTrainerInfo()
                print()
                if found is not True:
                    found = True
        else:
            print(f"\nAdvances: {i}")
            r.printTrainerInfo()
            print()
            if found is not True:
                found = True
        tmpRNG.next()
        i += 1

    if found:
        b.foundActions()
    else:
        b.notfoundActions(i)

    #game resetting
    print("Resetting...\n")
    b.quitGame()

    b.enterGame()
    print()
    b.pause(4)
