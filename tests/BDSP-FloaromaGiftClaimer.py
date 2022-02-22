# Go to root/test of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from rng import XORSHIFT
from nxbot import BDSPBot

config: dict = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

def signal_handler(signal, advances): #CTRL+C handler
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

r = XORSHIFT(b.getSeed())
seed: list = r.state()
advances: int = 0
print("Initial Seed")
print(f"S[0]: {seed[0]:08X}\tS[1]: {seed[1]:08X}\nS[2]: {seed[2]:08X}\tS[3]: {seed[3]:08X}")
print()
print(f"Advances: {advances}\n\n")

userInput: str = input("Press A at a specific advance? (y/n) ")
if userInput == "y" or userInput == "Y":
    botFlag: bool = True
    userAdvances: str = input("Input the target advances separated by a space: ")
    targetAdvances: list = sorted([int(i) for i in userAdvances.split(' ') if i.isdigit()])
    
    # Variables for conversation timeline
    conversationStarted: bool = False
    remainder: int = divmod(targetAdvances[0], 41)[1]
    startConversation: list = [remainder]
    
    # Identify when to begin the conversation, every possible starting point is generated to start talking to NPC as soon as pokedex advances stop to prevent fidgets. THIS IS CRITICAL.
    for conversationTarget in startConversation:
        if conversationTarget + 41 < targetAdvances[0] - 500:
            startConversation.append(conversationTarget + 41)

    # Variable to handle progression of conversation
    conversationProgressed: bool = False

    # Dexscrolling Variables
    dexOpened: bool = False
    dexScrolled: bool = False
    trainercardOpened: bool = False
    scrolls: int = 0

else:
    botFlag = False
print("\n")

while True:
    currSeed = b.getSeed()

    while r.state() != currSeed:
        r.next()
        advances += 1

        if r.state() == currSeed:
            print("Current Seed")
            print(f"S[0]: {currSeed[0]:08X}\tS[1]: {currSeed[1]:08X}\nS[2]: {currSeed[2]:08X}\tS[3]: {currSeed[3]:08X}")
            print()
            print(f"Advances: {advances}\n\n")

            if botFlag:
                if advances > 60: # Stops pokedex being opened before game loads save file
                    if advances <= targetAdvances[0] - 1500: # Avoid advancing too far with Pokedex
                        if not dexOpened: # Open Pokedex
                            print(f"Opening pokedex to advance...\n\n")
                            b.click("X")
                            b.pause(0.9)
                            b.click("A")
                            b.pause(1.2)
                            b.click("R")
                            b.pause(1.5)
                            dexOpened = True

                        if dexOpened: # Scroll Dex
                            print(f"Pokedex scrolled {scrolls} times\n\n")
                            scrolls += 1
                            b.click("DRIGHT")
                            b.pause(0.1)

                    if advances >= targetAdvances[0] - 1500:
                        if not conversationStarted:
                            if dexOpened: # Close Dex
                                print(f"Closing pokedex...\n\n")
                                b.click("B")
                                b.pause(0.9)
                                b.click("B")
                                b.pause(0.9)
                                dexOpened = False
                                dexScrolled = True

                            if dexScrolled: # Try to start conversation some multiple of 41 before target, MUST HAPPEN ASAP after pokedex closed
                                for conversationTarget in startConversation:
                                    if advances < conversationTarget:
                                        break
                                    if advances == conversationTarget and advances > 30:
                                        b.click("A")
                                        print(f"Conversation started on advance {conversationTarget}!\n\n")
                                        conversationStarted = True
                                    if advances > conversationTarget:
                                        startConversation.remove(conversationTarget)

                        if conversationStarted:
                            if not conversationProgressed: # Progress conversation to generation stage
                                b.pause(1.45)
                                b.click("A")
                                b.pause(1.45)
                                b.click("A")
                                b.pause(1.45)
                                b.click("A")
                                conversationProgressed = True

                            if  conversationProgressed: # Try to hit target
                                if len(targetAdvances) > 0:
                                    for currentTarget in targetAdvances:
                                        if advances < currentTarget:
                                            break
                                        if advances == currentTarget:
                                            for i in range(5):
                                                b.click("A")
                                                b.pause(0.2)
                                            print(f"We hit {currentTarget}!\n\n")
                                            b.close()
                                        if advances > currentTarget:
                                            targetAdvances.remove(currentTarget)

            if len(targetAdvances) == 0 or targetAdvances[-1] < advances:
                print("Missed all potential targets.\n")
                b.close()
