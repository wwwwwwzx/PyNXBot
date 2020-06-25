#Connect your Switch to Interet
#Start sys-botbase, ldn_mitm and luxray (the yellow cursor of luxray has to be over "+3" button)
#Go to System Settings, check your Switch IP and write it below
#Save in front of an Den whose beam has been generated through Wishing Piece
#Start the script with your game opened

from time import sleep
import signal
import sys
sys.path.append('../')

from lookups import Util
from structure import Den
from nxbot import RaidBot

def signal_handler(signal, frame): #CTRL+C handler
    print("Stop request")
    b.closeGame()
    sys.exit(0)

IP = '10.0.0.54' #write the IP of your Switch here
b = RaidBot(IP)

signal.signal(signal.SIGINT, signal_handler)

reset = 0

species = input("Which Pokémon are you looking for? (e.g.: Gengar) ")
gigantamax = input("Are you looking for a Gigantamax form? (y/n) ")
if gigantamax == 'y' or gigantamax == 'Y':
    gigantamax = True
else:
    gigantamax = False

starsMin = int(input("Minimum Star Number (1-5): "))
if(starsMin == 5):
    starsMax = 5
else:
    tmp = int(input("Maximum Star Number (min-5): "))
    if(tmp <= starsMin):
        starsMax = starsMin
    else:
        starsMax = tmp
        
sleep(0.5)

while True:
    b.click('R') #R on Luxray "+3" button
    sleep(1.7)

    for ii in range(RaidBot.DENCOUNT):
        if ii > 99:
                den = Den(b.readDen(ii + 11))
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
            sleep(0.5)
            break

    if den.stars() <= starsMax and den.stars() >= starsMin and species == Util.STRINGS.species[spawn.Species()] and gigantamax == spawn.IsGigantamax():
        print("Found after", reset, "resets")
        a = input('Continue searching? (y/n): ')
        if a != "y" and a != "Y":
            b.closeGame()
            break
    else:
        reset = reset + 1
        print("Wrong Stars - Resets:", reset)

    #game closing
    print("Resetting...")
    b.quit_app()
    print()

    print("Starting the game")
    b.skipAnimation(luxray = True)
    sleep(0.6)
