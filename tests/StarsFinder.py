#Connect your Switch to Interet
#Start sys-botbase, ldn_mitm and luxray (the yellow cursor of luxray has to be over "+3" button)
#Go to System Settings, check your Switch IP and write it inside the "config.json" file
#Start the game, save in front of an Den whose beam has been generated through a Wishing Piece and leave the game opened
#Run the script

import signal
import sys
import json 
sys.path.append('../')

from lookups import Util
from structure import Den
from nxbot import RaidBot

def signal_handler(signal, frame): #CTRL+C handler
    print("Stop request")
    b.closeGame()

config = json.load(open("../config.json"))
b = RaidBot(config["IP"])

signal.signal(signal.SIGINT, signal_handler)

species = input("Which Pokémon are you looking for? (e.g.: Gengar) ")
altFormFilter = False
altForm = 0
if species == "Gourgeist":
    altForm = input("Are you looking for a specific size? (y/n) ")
    if altForm == 'y' or altForm == 'Y':
        altFormFilter = True
        altForm = int(input("Which size are you looking for?\n0) Avarage / 1) Small / 2) Large / 3) Super: "))
elif species == "Sinistea" or species == "Polteageist":
    altForm = input("Are you looking for a specific form? (y/n) ")
    if altForm == 'y' or altForm == 'Y':
        altFormFilter = True
        altForm = int(input("Which form are you looking for?\n0) Phony / 1) Antique: "))

gigantamax = input("Are you looking for a Gigantamax form? (y/n) ")
if gigantamax == 'y' or gigantamax == 'Y':
    gigantamax = True
else:
    gigantamax = False

shinyLock = input("Is the Pokémon shiny locked? (y/n) ")
if shinyLock == 'y' or shinyLock == 'Y':
    shinyLock = 1
else:
    shinyLock = input("Is the Pokémon forced shiny? (y/n) ")
    if shinyLock == 'y' or shinyLock == 'Y':
        shinyLock = 2
    else:
        shinyLock = 0

starsMin = int(input("Minimum Star Number (1 to 5): "))
if(starsMin == 5):
    starsMax = 5
else:
    tmp = int(input("Maximum Star Number (min to 5): "))
    if(tmp <= starsMin):
        starsMax = starsMin
    else:
        starsMax = tmp
        
b.pause(0.5)
print()

while True:
    b.click('R') #R on Luxray "+3" button
    b.pause(1.7)

    for ii in range(RaidBot.DENCOUNT):
        if ii > 189:
                den = Den(b.readDen(ii+32))
        elif ii > 99:
                den = Den(b.readDen(ii+11))
        else:
                den = Den(b.readDen(ii))
        if den.isActive() and den.isWishingPiece():
            spawn = den.getSpawn(denID = ii, isSword = b.isPlayingSword)
            if ii > 189:
                        info = f"[CT] denID: {ii-189}"
            elif ii > 99:
                    info = f"[IoA] denID: {ii-99}"
            else:
                    info = f"denID: {ii+1}"
            info += f"    {den.stars()}★    Species: {Util.STRINGS.species[spawn.Species()]} "
            if spawn.IsGigantamax():
                info += "G-Max "
            if den.isEvent():
                if spawn.ShinyFlag() == 1:
                    info += 'Shiny Locked '
                elif spawn.ShinyFlag() == 2:
                    info += '◇ '
                info += "   Event"
            print(info)
            b.pause(0.5)
            break

    if den.isEvent():
        shinyLockCheck = shinyLock == spawn.ShinyFlag()
    else:
        shinyLockCheck = 1

    if altFormFilter:
        altFormCheck = altForm == spawn.AltForm()
    else:
        altFormCheck = 1

    if den.stars() >= starsMin and den.stars() <= starsMax and species == Util.STRINGS.species[spawn.Species()] and gigantamax == spawn.IsGigantamax() and shinyLockCheck and altFormCheck:
        b.foundActions()
    else:
        b.notfoundActions(bot='stars')

    #game resetting
    print("Resetting...")
    b.quitGame()

    b.enterGame()
    b.skipIntroAnimation() #luxray=True
