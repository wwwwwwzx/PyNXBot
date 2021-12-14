# Go to root/test of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from rng import XORSHIFT,Stationary
from nxbot import BDSPBot

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

def signal_handler(signal, advances): #CTRL+C handler
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

usefilters = 1 #set 0 to disable filter

V6 = [31,31,31,31,31,31] #add here the spreads you need
A0 = [31,0,31,31,31,31]
S0 = [31,31,31,31,31,0]
TRA0 = [31,0,31,31,31,0]

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
        r = Stationary(tmpRNG.state(), b.TrainerSave.TID(), b.TrainerSave.SID(), 3)
        if usefilters:
            if r.ShinyType != 'None' and (r.IVs == A0 or r.IVs == V6): #and Util.STRINGS.natures[r.Nature] == 'Adamant' and (r.IVs == V6 or  or r.IVs == S0):
                print(f"\nAdvances: {i}")
                r.print()
                print()
                if found is not True:
                    found = True
        else:
            print(f"\nAdvances: {i}")
            r.print()
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
