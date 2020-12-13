#Connect your Switch to Interet
#Start sys-botbase and ldn_mitm
#Go to System Settings, check your Switch IP and write it in the "config.json" file
#Save in front of a stationary
#Start the script with your game opened
#pk8.getAbilityString() == 1/2/'H'
#Util.STRINGS.natures[pk8.nature()] == 'Nature'
#pk8.shinyString() == 'None'/'Star'/'Square' (!= 'None' for both star/square)
#pk8.IVs == spread_name (spread_name = [x,x,x,x,x,x])

# Go to root of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from structure import PK8
from nxbot import SWSHBot
from lookups import Util

def signal_handler(signal, frame): #CTRL+C handler
    print()
    print("Stop request")
    b.close()

config = json.load(open("../config.json"))
b = SWSHBot(config["IP"])

signal.signal(signal.SIGINT, signal_handler)

V6 = [31,31,31,31,31,31] #add here the spreads you need
A0 = [31,0,31,31,31,31]
S0 = [31,31,31,31,31,0]
TRA0 = [31,0,31,31,31,0]

print("Modes:\n1) Ethernatus\n2)Registeel/Registeel/Regirock/Regice/Regidrago/Regieleki\n")

mode = int(input("Input the desired mode: (1/2) "))

while True:
    found = False
    if mode == 1:
        b.moveStick("LEFT",x=0,y=32767)
        b.pause(2)
        b.moveStick("LEFT",x=0,y=0)
        print("Skipping cutscene...")
    else:
        print("Starting battle...")
    battle = False
    i = 0
    while battle is not True and i <= 90:
        pk8 = PK8(b.readWild())
        if pk8.isValid() and pk8.ec() != 0:
            battle = True
            print("Battle started! - Checking stats...")
            b.pause(0.5)
            print(pk8.toString())
            if Util.STRINGS.natures[pk8.nature()] == 'Timid' or pk8.shinyString() != 'None':
                found = True
            break
        if mode == 2:
            b.click("A")
        else:
            b.click("B")
        b.pause(0.5)
        i += 1

    if found:
        b.foundActions()
    else:
        b.notfoundActions(i)

    #game closing
    print("Resetting...")
    b.quitGame()
    print()

    print("Starting the game")
    b.skipIntroAnimation() #luxray=True
