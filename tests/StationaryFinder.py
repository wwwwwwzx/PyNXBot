# Go to root of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from structure import PK8
from nxbot import SWSHBot
from lookups import Util

def signal_handler(signal, frame): #CTRL+C handler
    print("Stop request")
    b.close()

config = json.load(open("../config.json"))
b = SWSHBot(config["IP"])

signal.signal(signal.SIGINT, signal_handler)

while True:
    b.moveStick("LEFT",x=0,y=32767)
    b.pause(2)
    b.moveStick("LEFT",x=0,y=0)
    print("Skipping cutscene...")
    battle = False
    i = 0
    while battle is not True and i <= 240:
        pk8 = PK8(b.readWild())
        if pk8.isValid():
            print("Battle started! - Checking stats...")
            b.pause(0.5)
            print(pk8.toString())
            battle = True
        if battle:
            if Util.STRINGS.natures[pk8.nature()] == 'Timid':
                print("Found timid!")
            break
        b.click("B")
        b.pause(0.5)
        i += 1

    #game closing
    print("Resetting...")
    b.quitGame()
    print()

    print("Starting the game")
    b.skipIntroAnimation() #luxray=True
