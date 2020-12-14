#Connect your Switch to Interet
#Start sys-botbase and ldn_mitm
#Go to System Settings, check your Switch IP and write it below
#Set game text speed to normal
#Save in front of an empty Den. You must have at least one Wishing Piece in your bag
#Start the script with your game opened
#r.Ability == 1/2/'H'
#r.Nature == 'Nature'
#r.ShinyType == 'None'/'Star'/'Square' (!= 'None' for both square/star)
#r.IVs == spread_name (spread_name = [x,x,x,x,x,x])

import signal
import sys
sys.path.append('../')

from lookups import Util
from structure import Den
from nxbot import RaidBot
from rng import XOROSHIRO,Raid
import json

def signal_handler(signal, frame): #CTRL+C handler
    print()
    print("Stop request")
    b.closeGame()

config = json.load(open("../config.json"))
b = RaidBot(config["IP"])

signal.signal(signal.SIGINT, signal_handler)

usefilters = 1 #set 0 to disable filter

V6 = [31,31,31,31,31,31] #add here the spreads you need
A0 = [31,0,31,31,31,31]
S0 = [31,31,31,31,31,0]
TRA0 = [31,0,31,31,31,0]

altform = 0

denId = int(input("Den Id: "))

IoA_CT_check = (input("Is your den in the Isle of Armor or in the Crown Tundra? (y/n) "))
if IoA_CT_check == "y" or IoA_CT_check == "Y":
    IoA_CT_check = (input("1 - Isle of Armor / 2 - Crown Tundra? (1/2): "))
    if IoA_CT_check == 1:
        denId += 111
    else:
        denID += 132

b.setTargetDen(denId)

den_type = input("Are you looking for a Rare Beam, Event or Normal Raid? (r/e/n) ")
if den_type == "r" or den_type == "R":
    rb_research = True
    ev_research = False
elif den_type == "e" or den_type == "E":
    rb_research = False
    ev_research = True
else:
    rb_research = False
    ev_research = False

flawlessiv = int(input("How many fixed IVs will the Pokémon have? (1 to 6) "))

ability = input("Is it Ability locked? (y/n) ")
if ability == 'y' or ability == 'Y':
    ability = input("Ability 1, 2 or H? (1/2/h) ")
    if ability == '1':
        ability = 0
    elif ability == '2':
        ability = 1
    elif ability == 'h' or ability == 'H':
        ability = 2
else:
    ability = input("Is Hidden Ability possible? (y/n) ")
    if ability == 'y' or ability == 'Y':
        ability = 4
    else:
        ability = 3
    
species = input("Are you looking for Toxtricity? (y/n) ")
if species == 'y' or species == 'Y':
    species = 849
    gender = 0
else:
    species = 25
    gender = input("Are you looking for a random gender Pokémon? (y/n) ")
    if gender == 'y' or gender == 'Y':
        gender = 0
    else:
        gender = input("Is it male, female or genderless? (m/f/-) ")
        if gender == 'm' or gender == 'M':
            gender = 1
        elif gender == 'f' or gender == 'F':
            gender = 2
        else:
            gender = 3

shinylock = input("Is the Pokémon shiny locked? (y/n) ")
if shinylock == 'y' or shinylock == 'Y':
    shinylock = 1
else:
    shinylock = input("Is the Pokémon forced shiny? (y/n) ")
    if shinylock == 'y' or shinylock == 'Y':
        shinylock = 2
    else:
        shinylock = 0

if species == 849 and b.isPlayingSword == False:
    altform = 1

MaxFrame = int(input("Input Max Frame: "))

b.pause(0.5)
print()

while True:
    den = b.getDenData()
    if den.hasWatts():
        print("Den has watts - Getting them...")
        b.getWatts()
    else:
        print("No watts in Den")

    b.pause(0.5)
    b.throwPiece()

    den = b.getDenData()
    print(f"Seed: {den.seed():X}")
    seed = den.seed()

    if den.isRare():
        print("Rare beam Raid")
    elif den.isEvent():
        print("Event Raid")
    else:
        print("Normal Raid")
        
    #spreads research
    do_research = 1

    #rare beam/event check
    if rb_research and rb_research != den.isRare():
        do_research = False
    elif ev_research and ev_research != den.isEvent():
        do_research = False
    elif rb_research is not True and ev_research is not True:
        if rb_research != den.isRare() or ev_research != den.isEvent():
            do_research = False
    else:
        print("Searching...")

    i = 0
    found = False
    if do_research:
        while i < MaxFrame:
            r = Raid(seed,b.TID,b.SID,flawlessiv,shinylock,ability,gender,species,altform)
            seed = XOROSHIRO(seed).next()
            if usefilters:
                if r.ShinyType != 'None' and Util.STRINGS.natures[r.Nature] == 'Adamant' and Util.GenderSymbol[r.Gender] === '' and r.Ability == 'H' and r.IVs == V6: #and (r.IVs == V6 or  or r.IVs == S0):
                    print(f"Frame:{i}")
                    r.print()
                    if found is not True:
                        found = True
            else:
                print(f"Frame:{i}")
                r.print()
                if found is not True:
                    found = True
            i += 1

    if found:
        b.foundActions()
    else:
        b.notfoundActions(i)

    #game closing
    print("Resetting...")
    b.quitGame(needHome=False)
    print()

    print("Starting the game")
    b.skipIntroAnimation()
