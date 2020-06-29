#Connect your Switch to Interet
#Start sys-botbase, ldn_mitm and luxray (the yellow cursor of luxray has to be over "+3" button)
#Go to System Settings, check your Switch IP and write it below
#Save in front of an Den whose beam has been generated through Wishing Piece
#Start the script with your game opened

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
    sys.exit(0)

config = json.load(open("../config.json"))

b = RaidBot(config["IP"])

signal.signal(signal.SIGINT, signal_handler)

species = input("Which Pokémon are you looking for? (e.g.: Gengar) ")
gigantamax = input("Are you looking for a Gigantamax form? (y/n) ")
if gigantamax == 'y' or gigantamax == 'Y':
    gigantamax = True
else:
    gigantamax = False

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
        if ii > 99:
                den = Den(b.readDen(ii+11))
        else:
                den = Den(b.readDen(ii))
        if den.isActive() and den.isWishingPiece():
            spawn = den.getSpawn(denID = ii, isSword = b.isPlayingSword)
            if ii > 99:
                    info = f"[IoA] denID {ii-99}"
            else:
                    info = f"denID {ii+1}"
            info += f":0x{den.seed():X}\t{den.stars()}★\tSpecies: {Util.STRINGS.species[spawn.Species()]}\t"
            if spawn.IsGigantamax():
                info += "G-Max\t"
            print(info)
            b.pause(0.5)
            break

    if den.stars() >= starsMin and den.stars() <= starsMax and species == Util.STRINGS.species[spawn.Species()] and gigantamax == spawn.IsGigantamax():
        b.foundActions()
    else:
        b.notfoundActions(bot='stars')

    #game closing
    print("Resetting...")
    b.quitGame()
    print()

    print("Starting the game")
    b.skipAnimation() #luxray=True
    b.pause(0.6)
