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

from time import sleep
import signal
import sys
sys.path.append('../')

from lookups import PKMString
from structure import Den
from nxbot import RaidBot
from rng import XOROSHIRO,Raid

def signal_handler(signal, frame): #CTRL+C handler
    print("Stop request")
    b.closeGame()
    sys.exit(0)

IP = '10.0.0.54' #write the IP of your Switch here
b = RaidBot(IP)

signal.signal(signal.SIGINT, signal_handler)

usefilters = 1 #set 0 to disable filter

V6 = [31,31,31,31,31,31] #add here the spreads you need
A0 = [31,0,31,31,31,31]
S0 = [31,31,31,31,31,0]
TRA0 = [31,0,31,31,31,0]

altform = 0
isSword = b.isPlayingSword

reset = 0

denId = int(input("Den Id: "))

IoA_check = (input("Is your den in the Isle of Armor? (y/n) "))
if IoA_check == "y" or IoA_check == "Y":
    denId += 111

b.setTargetDen(denId)

den_type = input("Are you looking for a Rare Beam, Event or Normal Raid? (r/e/n) ")
if den_type == "r" or den_type == "R":
    rb_research = 1
    ev_research = 0
elif den_type == "e" or den_type == "E":
    rb_research = 0
    ev_research = 1
else:
    rb_research = 0
    ev_research = 0

flawlessiv = int(input("How many fixed IVs will the Pokémon have? (1 to 5) "))

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
    ability = input("Is it Hidden Ability possible? (y/n) ")
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

if species == 849 and isSword == False:
    altform = 1

MaxFrame = int(input("Input Max Frame: "))
sleep(0.5)
print()

while True:
    den = b.getDenData()
    if den.hasWatts():
        print("Den has watts - Getting them...")
        b.getWatts()
    else:
        print("No watts in Den")

    sleep(0.5)
    b.throwPiece()

    den = b.getDenData()
    print(f"Seed: {den.seed():X}")
    seed = den.seed()

    if den.isRare():
        print("Rare beam")
    else:
        print("No rare beam")

    if den.isEvent():
        print("Event Raid")
    else:
        print("No event Raid")
        
    #spreads research
    i = 0
    found = 0
    do_research = 1
    
    if rb_research == 1 and rb_research != den.isRare(): #rare beam/event check
        do_research = 0
    elif ev_research == 1 and ev_research != den.isEvent():
        do_research = 0
    elif rb_research == 0 and ev_research == 0:
        if rb_research != den.isRare() or ev_research != den.isEvent():
            do_research = 0
    else:
        print("Searching...")

    if do_research:
        while i < MaxFrame:
            r = Raid(seed,b.TrainerSave.TID(),b.TrainerSave.SID(),flawlessiv,shinylock,ability,gender,species,altform)
            seed = XOROSHIRO(seed).next()
            if usefilters:
                if r.ShinyType != 'None': #and (r.IVs == V6 or  or r.IVs == S0):
                    print(f"Frame:{i}")
                    r.print()
                    if found != 1:
                        found = 1
            else:
                print(f"Frame:{i}")
                r.print()
                if found != 1:
                    found = 1
            i += 1

    if found:
        print("Found after", reset, "resets")
        a = input("Continue searching? (y/n): ")
        if a != "y" and a != "Y":
            b.closeGame()
            break
    else:
        if i == 0:
            print("Research skipped")
        reset = reset + 1
        print("Nothing found - Resets:", reset)

    #game closing
    print("Resetting...")
    b.quit_app(need_home = False)
    print()

    print("Starting the game")
    b.skipAnimation()
