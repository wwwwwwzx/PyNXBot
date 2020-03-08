#Connect your Switch to Interet
#Start sys-botbase and ldn_mitm
#Go to System Settings, check your Switch IP and write it below
#Set game text speed to normal
#Save in front of an empty Den. You must have at least one Wishing Piece in your bag
#Start the script with you game opened
#r.Ability == 1/2/'H'
#r.Nature == 'NATURE'
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
    b.close()
    sys.exit(0)

IP = '192.168.1.4' #write the IP of your Switch here
b = RaidBot(IP)

signal.signal(signal.SIGINT, signal_handler)

ivfilter = 1 #set 0 to disable filter

V6 = [31,31,31,31,31,31] #add here the spreads you need
A0 = [31,0,31,31,31,31]
S0 = [31,31,31,31,31,0]
TRA0 = [31,0,31,31,31,0]

reset = 0

denId = int(input("Den Id: "))
b.setTargetDen(denId)

rb_research = input("Are you looking for a Rare Beam Raid? (y/n) ")
if rb_research == "y":
    rb_research = 1
    ev_research = 0
else:
    rb_research = 0
    ev_research = input("Are you looking for an Event Raid? (y/n) ")
    if ev_research == "y":
        ev_research = 1
    else:
        ev_research = 0

flawlessiv = int(input("How many fixed IVs will the Pokemon have? (1 to 5) "))

ability = input("Is Hidden Ability possible? (y/n) ")
if ability == 'y':
    ability = 4
else:
    ability = 3
    
species = input("Are you looking for Toxtricity? (y/n) ")
if species == 'y':
    species = 849
    gender = 0
else:
    species = 25
    gender = input("Are you looking for a Random Gender Pokémon? (y/n) ")
    if gender == 'y':
        gender = 0
    else:
        gender = input("Is it male, female or genderless? (m/f/-)")
        if gender == 'm':
            gender = 1
        elif gender == 'f':
            gender = 2
        else:
            gender = 3

altform = 0
isSword = b.TrainerSave.isSword()
if species == 849 and isSword == False:
    altform = 1

Maxresults = int(input("Input Max Results: "))
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
    j = 0
    found = 0
    do_research = 1
    
    if rb_research == 1 and rb_research != den.isRare(): #rare beam/event check
        do_research = 0
    elif ev_research == 1 and ev_research != den.isEvent():
        do_research = 0
    elif rb_research == 0 and ev_research == 0:
        if rb_research != den.isRare() or ev_research != den.isEvent():
            do_research = 0
    
    while j < Maxresults and do_research:        
        if j < 1:
            print("Searching...")

        r = Raid(seed,flawlessiv,ability,gender,species,altform)
        seed = XOROSHIRO(seed).next()
        if ivfilter:
            if r.ShinyType != 'None' and PKMString().natures[r.Nature] == 'Bold' and r.Ability == 'H': #and (r.IVs == V6 or r.IVs == A0 or r.IVs == S0):
                print("Frame:", j)
                r.print()
                if found != 1:
                    found = 1
        else:
            if found != 1:
                found = 1
            print("Frame:", j)
            r.print()
        j += 1

    if found:
        print("Found after", reset, "resets")
        a = input("Continue searching? (y/n): ")
        if a != "y" or a != "Y":
            b.closeGame()
            print("Exiting...")
            b.close()
            break
    else:
        if j == 0:
            print("Research skipped")
        reset = reset + 1
        print("Nothing found - Resets:", reset)

    #game closing
    print("Resetting...")
    b.quit_app(need_home = False)
    sleep(2.5) 
    print()

    print("Starting the game")
    b.skipAnimation()
